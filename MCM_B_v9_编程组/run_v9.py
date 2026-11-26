"""Rebuild the v9 conditional study and all independently implemented checks.

This entry point works from any current working directory.  A failed stage
cannot leave a successful run record from an older invocation in place.
"""
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import hashlib
import json
import platform
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parent
STAGES = ['physics_v9.py', 'water_v9.py', 'joint_v9.py',
          'sensitivity_v9.py', 'verify_v9.py']
PRODUCERS = STAGES + ['construction_v9.py', 'cost_environment_v9.py',
                     'registry_v9.py', 'phase_audit_v9.py',
                     'reference/physics_v8.py', 'reference/water_v8.py',
                     'reference/__init__.py']


def file_sha256(path):
    digest = hashlib.sha256()
    with path.open('rb') as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def producer_hashes():
    return {name: file_sha256(ROOT / name) for name in PRODUCERS}


def main():
    results = ROOT / 'results'
    results.mkdir(exist_ok=True)
    for name in ['independent_v9.json', 'run_record.json']:
        (results / name).unlink(missing_ok=True)
    before = producer_hashes()
    started = time.monotonic()
    stage_seconds = {}
    for name in STAGES:
        print('Running ' + name, flush=True)
        tic = time.monotonic()
        subprocess.run([sys.executable, str(ROOT / name)], cwd=ROOT, check=True)
        stage_seconds[name] = time.monotonic() - tic
    after = producer_hashes()
    if after != before:
        raise RuntimeError('Numerical producer/check sources changed during the run; rerun the frozen files.')
    audit = json.loads((results / 'independent_v9.json').read_text(encoding='utf-8'))
    if audit.get('all_implemented_checks_pass') is not True:
        raise RuntimeError('The independent audit has not passed every implemented required check.')
    import numpy
    import scipy
    import matplotlib
    record = dict(
        version='v9_complete_numerical_run',
        completed_at=datetime.now(ZoneInfo('Asia/Shanghai')).isoformat(),
        timezone='Asia/Shanghai',
        python=sys.version, platform=platform.platform(),
        dependencies=dict(numpy=numpy.__version__, scipy=scipy.__version__,
                          matplotlib=matplotlib.__version__),
        stage_seconds=stage_seconds,
        total_seconds=time.monotonic() - started,
        independent_checks_pass=True,
        producer_sources_unchanged=True,
        producer_code_sha256=after,
        root_code_sha256={p.name: file_sha256(p) for p in sorted(ROOT.glob('*.py'))},
        scope='Reproducibility and checks of explicitly stated model supports. Not empirical lunar reliability, actual future prices, unrestricted optimality or engineering certification.')
    (results / 'run_record.json').write_text(
        json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')
    print('V9 numerical producers and independent checks passed.', flush=True)


if __name__ == '__main__':
    main()
