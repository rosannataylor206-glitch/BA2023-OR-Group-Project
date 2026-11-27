from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

import pymupdf as fitz

sys.dont_write_bytecode = True
from scan_handbook import page_spans


BOUNDS = [(69, 97), (98, 133), (134, 160), (161, 187), (188, 215),
          (216, 243), (244, 274), (275, 350), (351, 390), (391, 413), (414, 441)]
STARTS = ["The consumer", "PDMS thin", "The implementation", "The unit commitment",
          "The high cost", "This problem", "This study", "The integration",
          "In order", "In this study", "This paper"]
PARAGRAPHS = [5, 5, 7, 6, 6, 5, 6, 5, 6, 6, 6]


def measure(spans):
    counts = Counter()
    sizes = Counter()
    fonts = Counter()
    records = []
    for span in spans:
        chars = len(re.sub(r"\s", "", span["text"]))
        name_bold = span["bold_name_hint"]
        flag_bold = bool(span["flags"] & 16)
        bold = name_bold or flag_bold
        counts["characters"] += chars
        counts["bold_characters"] += chars if bold else 0
        counts["name_bold_characters"] += chars if name_bold else 0
        counts["flag_bold_characters"] += chars if flag_bold else 0
        counts["disagreement_characters"] += chars if name_bold != flag_bold else 0
        sizes[str(span["size"])] += chars
        fonts[span["font"]] += chars
        records.append({key: span[key] for key in ("font", "size", "flags", "bbox")})
        records[-1].update(characters=chars, bold=bold,
                           text_sha256=hashlib.sha256(span["text"].encode()).hexdigest())
    text = " ".join(span["text"] for span in spans)
    tokens = re.findall(r"[A-Za-z0-9]+(?:['’.-][A-Za-z0-9]+)*", text)
    return {**counts, "english_numeric_tokens": len(tokens),
            "bold_ratio": counts["bold_characters"] / counts["characters"],
            "sizes_pt_by_characters": dict(sizes), "fonts_by_characters": dict(fonts),
            "spans": records}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    folder = root / "research/handbook"
    cache_path = folder / "handbook_scan.json"
    cache = json.loads(cache_path.read_text()) if cache_path.exists() else None
    document = fitz.open(args.pdf)
    assert len(document) == 441
    papers = []
    for index, ((start, end), prefix) in enumerate(zip(BOUNDS, STARTS), 1):
        page = document[start - 1]
        spans = page_spans(page)
        if cache is not None:
            cached = next(paper for paper in cache["papers"] if paper["summary_page"] == start)
            assert spans == cached["summary_spans"], (index, "cache differs from source")
        first = next(offset for offset, span in enumerate(spans) if span["text"].startswith(prefix))
        last = next(offset for offset in range(first + 1, len(spans))
                    if re.match(r"key\s*words\s*:", spans[offset]["text"], re.I))
        selected = spans[first:last]
        assert not any(re.search(r"[\u4e00-\u9fff]", span["text"]) for span in selected)
        assert len(selected) > 10
        result = measure(selected)
        body_top = min(span["bbox"][1] for span in selected)
        body_bottom = max(span["bbox"][3] for span in selected)
        sheet_heading = next(span for span in spans[:first]
                             if re.search(r"summary\s*sheet", span["text"], re.I))
        assert 0 <= result["bold_ratio"] <= 1
        papers.append({"id": f"HB{index:02d}", "physical_bounds": [start, end],
                       "abstract_page": start, "span_slice": [first, last],
                       "visual_content_paragraphs": PARAGRAPHS[index - 1],
                       "visual_internal_headings": 3 if index == 3 else 0,
                       "render": f"abstract_pages/paper-{index:02d}-page-{start:03d}.png",
                       "body_vertical_fraction": round((body_bottom - body_top) / page.rect.height, 4),
                       "sheet_heading_pt": sheet_heading["size"],
                       **result})
    result = {"source_sha256": hashlib.sha256(args.pdf.read_bytes()).hexdigest(),
              "pymupdf_version": fitz.VersionBind, "page_count": len(document),
              "scope": "abstract body including internal headings; excluding keywords and page metadata",
              "papers": papers}
    target = folder / "ABSTRACT_METRICS.json"
    if args.check:
        assert json.loads(target.read_text()) == result
    else:
        target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    for paper in papers:
        print(paper["id"], paper["abstract_page"], paper["english_numeric_tokens"],
              paper["characters"], paper["bold_characters"],
              f'{paper["bold_ratio"]:.2%}', paper["sizes_pt_by_characters"],
              "font disagreements", paper["disagreement_characters"])
    print("PASS: 11 bounded abstract bodies with reproducible font and layout metrics")


if __name__ == "__main__":
    main()