"""Read the verified v9 baseline and write supplemental tables safely."""

import csv
from pathlib import Path
from tempfile import NamedTemporaryFile

from programming_handoff import RESULTS, read_json


SUPPLEMENTAL = RESULTS / "supplemental"


def load_verified_study():
    record = read_json(RESULTS, "run_record.json")
    audit = read_json(RESULTS, "independent_v9.json")
    if not (record.get("independent_checks_pass") is True
            and audit.get("all_implemented_checks_pass") is True):
        raise ValueError("Run python run_v9.py and pass verification before adding supplemental results")
    return read_json(RESULTS, "joint_v9.json")


def write_result_table(path, rows):
    path = Path(path).resolve()
    if path.suffix.lower() != ".csv":
        raise ValueError("The supplemental output path must end in .csv")
    if path.parent == RESULTS.resolve():
        raise ValueError("Write supplemental output to a separate directory")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with NamedTemporaryFile(mode="w", encoding="utf-8-sig", newline="",
                                dir=path.parent, prefix=f".{path.stem}-", delete=False) as stream:
            temporary = Path(stream.name)
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        temporary.replace(path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    return path
