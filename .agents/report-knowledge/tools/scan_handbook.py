from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import pymupdf as fitz


def normalized(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def page_spans(page: fitz.Page) -> list[dict[str, object]]:
    records = []
    data = page.get_text("dict")
    for block in data["blocks"]:
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                text = normalized(span["text"])
                if text:
                    records.append(
                        {
                            "text": text,
                            "font": span["font"],
                            "size": round(span["size"], 2),
                            "flags": span["flags"],
                            "bbox": [round(value, 2) for value in span["bbox"]],
                            "bold_name_hint": bool(
                                re.search(r"bold|black|heavy|demi|semibold", span["font"], re.I)
                            ),
                        }
                    )
    return records


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    render_dir = args.output / "abstract_pages"
    render_dir.mkdir(exist_ok=True)

    document = fitz.open(args.pdf)
    summary_pages = [
        index
        for index, page in enumerate(document)
        if re.search(r"summary\s*sheet", page.get_text(), re.I)
    ]
    papers = []
    for paper_number, start in enumerate(summary_pages, 1):
        end = summary_pages[paper_number] if paper_number < len(summary_pages) else len(document)
        summary_page = document[start]
        text_pages = []
        for index in range(start, end):
            text_pages.append(
                {
                    "physical_page": index + 1,
                    "text": document[index].get_text(),
                }
            )
        page_text = summary_page.get_text()
        team_match = re.search(r"apmcm\d+", page_text, re.I)
        chosen_match = re.search(r"Problem\s+Chosen\s*:\s*([A-D])", page_text, re.I)
        title_lines = [
            normalized(line)
            for line in page_text.splitlines()
            if normalized(line)
            and not re.search(r"team\s*(number|#)|problem\s*chosen|summary\s*sheet|apmcm\d+", line, re.I)
        ]
        image_path = render_dir / f"paper-{paper_number:02d}-page-{start + 1:03d}.png"
        summary_page.get_pixmap(matrix=fitz.Matrix(1.7, 1.7), alpha=False).save(image_path)
        spans = page_spans(summary_page)
        papers.append(
            {
                "paper_id": f"HB-{paper_number:02d}",
                "physical_start_page": start + 1,
                "physical_end_page": end,
                "summary_page": start + 1,
                "team": team_match.group(0) if team_match else None,
                "problem": chosen_match.group(1).upper() if chosen_match else None,
                "title_candidates": title_lines[:8],
                "summary_text": page_text,
                "summary_spans": spans,
                "bold_font_spans": [
                    span for span in spans if span["bold_name_hint"]
                ],
                "render": str(image_path),
                "pages": text_pages,
            }
        )
    result = {
        "source": str(args.pdf),
        "physical_page_count": len(document),
        "summary_marker_count": len(summary_pages),
        "papers": papers,
    }
    (args.output / "handbook_scan.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (args.output / "handbook_scan.md").write_text(
        "\n".join(
            [
                "# Handbook first-pass paper index",
                "",
                f"Physical pages: {len(document)}; summary markers: {len(summary_pages)}.",
                "",
                *[
                    f"- {paper['paper_id']}: pp. {paper['physical_start_page']}–{paper['physical_end_page']}; "
                    f"team={paper['team']}; problem={paper['problem']}; "
                    f"title candidates={'; '.join(paper['title_candidates'][:4])}; "
                    f"summary render={paper['render']}"
                    for paper in papers
                ],
                "",
            ]
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()