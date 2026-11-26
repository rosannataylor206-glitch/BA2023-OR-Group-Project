"""Restore two exact v9 JSON certificates from the private baseline archive.

Run from any directory: python3 review/baseline/restore_large_results.py
Existing files are only accepted when their SHA-256 already matches the archive contract.
"""
from pathlib import Path
import hashlib
import os
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / 'MCM_B_v9_编程组'
ARCHIVE = PACKAGE / 'results/core_certificates_v9.zip'
EXPECTED = {
    'joint_v9.json': ('f94736110437dc152f44eb33c770c37dfd652262afa9c60b7ca7e835d67cbd6f', 64582105),
    'phases_v9.json': ('eda270d2650f3e653089850ca17dc3c33f2dd7f430554c37a4c8415963bb586e', 45532268),
}

def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):
            h.update(chunk)
    return h.hexdigest()

with zipfile.ZipFile(ARCHIVE) as z:
    assert set(z.namelist()) == set(EXPECTED), 'Unexpected archive members'
    assert z.testzip() is None, 'Corrupt archive member'
    for name,(sha,size) in EXPECTED.items():
        target=PACKAGE/'results'/name
        if target.exists():
            assert target.stat().st_size==size and digest(target)==sha, f'Existing file differs: {target}'
            print('already verified',target)
            continue
        with tempfile.NamedTemporaryFile(dir=target.parent,prefix='.restore-',delete=False) as out:
            tmp=Path(out.name)
            try:
                with z.open(name) as src:
                    for chunk in iter(lambda:src.read(1024*1024),b''):
                        out.write(chunk)
            except Exception:
                tmp.unlink(missing_ok=True)
                raise
        if tmp.stat().st_size!=size or digest(tmp)!=sha:
            tmp.unlink(missing_ok=True)
            raise ValueError(f'Archive SHA-256 mismatch: {name}')
        os.replace(tmp,target)
        print('restored and verified',target)
