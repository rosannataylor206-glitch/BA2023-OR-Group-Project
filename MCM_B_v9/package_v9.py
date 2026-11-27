"""Package a complete, audited v9 handoff with streaming integrity checks.

Third-party papers are referenced by URL.  The original competition problem
is included, and every saved numerical certificate is retained.
"""
from pathlib import Path
import hashlib
import json
import os
import shutil
import zipfile


ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'deliverables'
STAGE = ROOT / 'release/MCM_B_v9'
REPORT_NAME = 'MCM_B_v9_建模修订与独立验证说明.docx'
ARCHIVE_NAME = 'MCM_B_v9_模型代码与验证复现包.zip'
ORIGINAL_PROBLEM = '2026_MCM_Problem_B.pdf'
NUMERICAL_SOURCES = ['physics_v9.py', 'water_v9.py', 'joint_v9.py',
    'sensitivity_v9.py', 'verify_v9.py', 'construction_v9.py',
    'cost_environment_v9.py', 'registry_v9.py', 'phase_audit_v9.py', 'reference/physics_v8.py',
    'reference/water_v8.py', 'reference/__init__.py']


def stream_sha256(handle):
    digest = hashlib.sha256()
    for block in iter(lambda: handle.read(1024 * 1024), b''):
        digest.update(block)
    return digest.hexdigest()


def sha256(path):
    with path.open('rb') as handle:
        return stream_sha256(handle)


def clean_evidence(value):
    if isinstance(value, dict):
        return {key: ('Original paper is not included; use its source URL.'
                      if key in ['local_pdf', 'local_pdf_path', 'downloaded_pdf']
                      else clean_evidence(item)) for key, item in value.items()}
    if isinstance(value, list):
        return [clean_evidence(item) for item in value]
    return value


def audited_sources():
    audit = json.loads((ROOT / 'results/independent_v9.json').read_text(encoding='utf-8'))
    if audit.get('all_implemented_checks_pass') is not True:
        raise RuntimeError('Cannot package an incomplete independent audit.')
    run = json.loads((ROOT / 'results/run_record.json').read_text(encoding='utf-8'))
    if run.get('independent_checks_pass') is not True:
        raise RuntimeError('A complete successful run_v9.py record is required before packaging.')
    recorded = run.get('producer_code_sha256', {})
    for name in NUMERICAL_SOURCES:
        if recorded.get(name) != sha256(ROOT / name):
            raise RuntimeError('Source changed after the successful run: ' + name)


def copy_tree(dirname):
    source = ROOT / dirname
    if not source.exists():
        return
    for path in sorted(source.rglob('*')):
        if (not path.is_file() or '__pycache__' in path.parts or
                any(part.startswith('.') for part in path.relative_to(source).parts)):
            continue
        if dirname == 'report_assets' and path.suffix.lower() not in ['.png', '.svg', '.jpg', '.jpeg']:
            continue
        target = STAGE / dirname / path.relative_to(source)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)


def main():
    audited_sources()
    report = OUT / REPORT_NAME
    if not report.is_file():
        report = ROOT / REPORT_NAME
    if not report.is_file():
        raise RuntimeError('Missing final v9 report: ' + REPORT_NAME)
    if STAGE.exists():
        shutil.rmtree(STAGE)
    STAGE.mkdir(parents=True)
    OUT.mkdir(exist_ok=True)
    for path in sorted(ROOT.glob('*.py')):
        shutil.copy2(path, STAGE / path.name)
    for name in ['README_v9.txt', 'requirements.txt']:
        path = ROOT / name
        if not path.is_file():
            raise RuntimeError('Missing handoff file: ' + name)
        shutil.copy2(path, STAGE / name)
    for dirname in ['reference', 'proofs', 'results', 'report_assets']:
        copy_tree(dirname)
    evidence = STAGE / 'evidence'
    evidence.mkdir()
    for path in sorted((ROOT / 'evidence').iterdir()):
        if not path.is_file():
            continue
        target = evidence / path.name
        if path.suffix.lower() == '.json':
            target.write_text(json.dumps(clean_evidence(json.loads(path.read_text(encoding='utf-8'))),
                ensure_ascii=False, indent=2), encoding='utf-8')
        elif path.name == ORIGINAL_PROBLEM:
            shutil.copy2(path, target)
    if not (evidence / ORIGINAL_PROBLEM).is_file():
        raise RuntimeError('Missing original competition problem PDF.')
    shutil.copy2(report, STAGE / REPORT_NAME)
    # Logs aid diagnosis but are not a substitute for the numerical artifacts.
    for name in ['run_stdout.txt', 'joint_stdout.txt', 'sensitivity_stdout.txt']:
        path = ROOT / name
        if path.is_file() and path.stat().st_size <= 2 * 1024 * 1024:
            shutil.copy2(path, STAGE / 'results' / name)
    manifest = {str(path.relative_to(STAGE)): sha256(path)
                for path in sorted(STAGE.rglob('*')) if path.is_file()}
    (STAGE / 'SHA256SUMS.json').write_text(json.dumps(manifest,
        ensure_ascii=False, indent=2), encoding='utf-8')
    archive = OUT / ARCHIVE_NAME
    temporary = archive.with_suffix('.tmp')
    with temporary.open('wb') as handle:
        with zipfile.ZipFile(handle, 'w', zipfile.ZIP_DEFLATED,
                             compresslevel=9, allowZip64=True) as bundle:
            for path in sorted(STAGE.rglob('*')):
                if path.is_file():
                    bundle.write(path, 'MCM_B_v9/' + str(path.relative_to(STAGE)))
        handle.flush()
        os.fsync(handle.fileno())
    with zipfile.ZipFile(temporary) as bundle:
        bad = bundle.testzip()
        if bad is not None:
            raise RuntimeError('Archive CRC failure: ' + bad)
        for name, expected in manifest.items():
            with bundle.open('MCM_B_v9/' + name) as handle:
                if stream_sha256(handle) != expected:
                    raise RuntimeError('Archive member hash mismatch: ' + name)
    os.replace(temporary, archive)
    print(json.dumps(dict(path=str(archive), files=len(manifest) + 1,
        bytes=archive.stat().st_size, sha256=sha256(archive)), ensure_ascii=False))


if __name__ == '__main__':
    main()
