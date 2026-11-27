from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

import pymupdf as fitz

from scan_handbook import normalized, page_spans


RANGES = [(69, 97), (98, 133), (134, 160), (161, 187), (188, 215),
          (216, 243), (244, 274), (275, 350), (351, 390), (391, 413), (414, 441)]
LEADER = re.compile(r"(?:\.\s*){3,}")
NUMBER = re.compile(r"^(\d+(?:\s*\.\s*\d+)*\s*[.．、]?\s*|(?:[ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩⅪⅫ]+|[IVX]+|[A-Z])(?:\s*[.．、]\s*|\s+))([A-Za-z].*)$")
CAPTION = re.compile(r"^(?:Figure|Fig\.?|Table|Figuer)\s*(?:\d+|[IVX]+(?=\s|$))", re.I)
EVIDENCE = re.compile(r"validat|sensitiv|robust|RMSE|MAPE|R.squared|PSNR|SSIM|accuracy|error|comparison", re.I)


def clean_lines(text):
    return [normalized(line) for line in text.splitlines()
            if normalized(line) and not re.search(r"[\u4e00-\u9fff]|^Team\s*#|^(?:Page\s*|P)\d+\s+of|^-\d+-$", normalized(line))]


def key(text):
    return re.sub(r"[^a-z0-9]", "", text.lower())


def toc_entries(pages):
    entries = []
    pending = ""
    origin = None
    for page in pages:
        lines = clean_lines(page["text"])
        for index, line in enumerate(lines):
            if line.lower() in {"contents", "content", "directory", "table of contents"}:
                continue
            if not pending:
                origin = page["physical_page"]
            pending = normalized(pending + " " + line)
            pending = LEADER.sub("   ", pending)
            match = re.search(r"\s(\d+)\s*$", pending)
            next_is_page = index + 1 < len(lines) and lines[index + 1].isdigit()
            if match and (line.isdigit() or not next_is_page):
                title = normalized(pending[:match.start()])
                number = NUMBER.match(title)
                entries.append({"title": title, "number": re.sub(r"\s", "", number.group(1)).rstrip(".．、") if number else None,
                                "printed_page": int(match.group(1)), "toc_physical_page": origin})
                pending = ""
    return entries, pending


def assign_levels(entries):
    mixed = any(re.fullmatch(r"[ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩⅪⅫ]+", entry["number"] or "") for entry in entries)
    stack = {}
    numeric = {}
    roman = {value: str(index) for index, value in enumerate(
        ("I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"), 1)}
    for index, entry in enumerate(entries, 1):
        number = entry["number"]
        level, parent, status = None, None, "unresolved_unnumbered"
        if mixed and number:
            if re.fullmatch(r"[ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩⅪⅫ]+", number):
                level = 1
            elif re.fullmatch(r"[A-Z]", number):
                level = 2
            elif number.isdigit():
                level = 3
            if level:
                parent = stack.get(level - 1)
                status = "mixed_numbering_inferred" if level == 1 or parent else "unresolved_parent"
        elif number in roman:
            level, status = 1, "explicit_roman_numbering"
            numeric[roman[number]] = index
        elif number and re.fullmatch(r"\d+(?:\.\d+)*", number):
            level = number.count(".") + 1
            parent = numeric.get(number.rsplit(".", 1)[0]) if level > 1 else None
            status = "explicit_numbering" if level == 1 or parent else "unresolved_parent"
            numeric[number] = index
        entry.update(level=level, parent_entry=parent, hierarchy_status=status)
        if level:
            stack = {depth: value for depth, value in stack.items() if depth < level}
            stack[level] = index


def audit(scan, document):
    assert scan["physical_page_count"] == len(document) == 441
    assert len(scan["papers"]) == len(RANGES)
    papers = []
    for source, (start, end) in zip(scan["papers"], RANGES):
        assert (source["physical_start_page"], source["physical_end_page"]) == (start, end)
        pages = source["pages"]
        assert [page["physical_page"] for page in pages] == list(range(start, end + 1))
        toc_pages = [page for page in pages[1:5] if len(LEADER.findall(page["text"])) >= 5]
        entries, remainder = toc_entries(toc_pages)
        assign_levels(entries)
        toc_numbers = {page["physical_page"] for page in toc_pages}
        body = [page for page in pages[1:] if page["physical_page"] not in toc_numbers]
        body_keys = {page["physical_page"]: key(page["text"]) for page in body}
        printed_map = {}
        for page in body:
            header = re.search(r"(?:Page\s*|P)(\d+)\s+of\s+(\d+)", page["text"][:240], re.I)
            if header:
                actual_header = re.search(r"(?:Page\s*|P)(\d+)\s+of\s+(\d+)",
                                          document[page["physical_page"] - 1].get_text()[:240], re.I)
                assert actual_header and actual_header.groups() == header.groups(), page["physical_page"]
                assert int(header.group(1)) not in printed_map, page["physical_page"]
                printed_map[int(header.group(1))] = page["physical_page"]
        for entry in entries:
            title = NUMBER.sub(lambda match: match.group(2), entry["title"])
            target = key(title)
            entry["body_matches"] = [page for page, text in body_keys.items() if target and target in text]
            entry["physical_page"] = printed_map.get(entry["printed_page"])
            entry["status"] = "printed_header_mapped" if entry["physical_page"] else "toc_only"
            entry["page_evidence"] = "pdf_header_verified" if entry["physical_page"] else "no_matching_body_header"
            entry["title_on_mapped_page"] = entry["physical_page"] in entry["body_matches"]
        for entry in entries:
            locator = (source["paper_id"], entry["title"])
            if locator == ("HB-01", "6.1 Strength And Weakness") and entry["physical_page"] == 94:
                parent = next(i for i, item in enumerate(entries, 1) if item["number"] == "VII")
                entry.update(level=2, parent_entry=parent, hierarchy_status="visual_heading_number_conflict")
            elif locator in {
                ("HB-01", "Report on Use of AI Tools"),
                ("HB-06", "References"),
                ("HB-06", "Appendix"),
            }:
                entry.update(level=1, parent_entry=None, hierarchy_status="visual_top_level")
        captions, evidence, headings, notation = [], [], [], []
        for page in body:
            physical = page["physical_page"]
            lines = clean_lines(page["text"])
            for index, line in enumerate(lines):
                if CAPTION.match(line):
                    caption = line if not re.fullmatch(r"(?:Figure|Fig\.?|Table)\s*\d+", line, re.I) else normalized(" ".join(lines[index:index+2]))
                    captions.append({"physical_page": physical, "caption": caption, "status": "candidate_including_mentions"})
                if EVIDENCE.search(line):
                    evidence.append({"physical_page": physical, "excerpt": normalized(" ".join(lines[max(0, index-1):index+2]))[:380], "status": "text_located"})
                if re.search(r"notation|symbol|nomenclature|terms.*definitions", line, re.I) and len(line) < 100:
                    notation.append({"physical_page": physical, "text": line, "status": "text_located"})
            for span in page_spans(document[physical - 1]):
                if span["bold_name_hint"] and NUMBER.match(span["text"]) and len(span["text"]) < 180:
                    headings.append({"physical_page": physical, "text": span["text"], "bbox": span["bbox"]})
        papers.append({"paper_id": source["paper_id"], "physical_start_page": start, "physical_end_page": end,
                       "team": source["team"], "title_candidates": source["title_candidates"][:2],
                       "toc_pages": sorted(toc_numbers), "toc_entries": entries, "toc_unparsed_tail": remainder,
                       "printed_page_map": printed_map,
                       "body_heading_candidates": headings, "captions": captions, "notation_candidates": notation,
                       "validation_candidates": evidence})
    return {"physical_page_count": len(document), "covered_pages": sum(end-start+1 for start, end in RANGES),
            "scope": "locators only; neither visual review nor model reproduction", "papers": papers}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--scan", type=Path, default=Path("research/handbook/handbook_scan.json"))
    parser.add_argument("--output", type=Path, default=Path("research/paper_reports/handbook_structure_evidence.json"))
    parser.add_argument("--render-dir", type=Path)
    parser.add_argument("--pages", type=int, nargs="*", default=[])
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    if args.render_dir and (args.render_dir.resolve() == root or root in args.render_dir.resolve().parents):
        parser.error("Render directory must be outside the repository")
    scan_bytes = args.scan.read_bytes()
    with fitz.open(args.pdf) as document:
        result = audit(json.loads(scan_bytes), document)
        result["pdf_sha256"] = hashlib.sha256(args.pdf.read_bytes()).hexdigest()
        result["scan_sha256"] = hashlib.sha256(scan_bytes).hexdigest()
        result["source_filename"] = args.pdf.name
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        if args.render_dir:
            args.render_dir.mkdir(parents=True, exist_ok=True)
            for physical in args.pages:
                assert 69 <= physical <= 441
                document[physical - 1].get_pixmap(matrix=fitz.Matrix(1.4, 1.4), alpha=False).save(args.render_dir / f"page-{physical:03d}.png")
    for paper in result["papers"]:
        print(paper["paper_id"], "TOC", paper["toc_pages"], "entries", len(paper["toc_entries"]),
              "unmatched", sum(entry["physical_page"] is None for entry in paper["toc_entries"]),
              "captions", len(paper["captions"]), "notations", paper["notation_candidates"][:2])


if __name__ == "__main__":
    main()