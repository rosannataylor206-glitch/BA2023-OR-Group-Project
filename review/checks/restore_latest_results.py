"""Restore the exact current-model large result JSON files; never overwrite a different result."""
from pathlib import Path
import hashlib,json,zipfile,tempfile,os
ROOT=Path(__file__).resolve().parents[2]
CONTRACT={'phases_v9.json': {'bytes': 45532268, 'sha256': 'eda270d2650f3e653089850ca17dc3c33f2dd7f430554c37a4c8415963bb586e'}, 'sensitivity_v9.json': {'bytes': 28258364, 'sha256': 'ce05fb9ae4d5a180abe6ab1e116d1594b384db04f5efcfcbea897f93c7588bd4'}, 'sensitivity_phases_v9.json': {'bytes': 12767498, 'sha256': '1c634c83ceec2a8cf09e743f418fcb18cda8027515d41ab358cf1f0286340ead'}, 'joint_v9.json': {'bytes': 67332577, 'sha256': '1623a6a2955e85feb824dc3e2a293788391bc94b0f21842c96fc05bcea0694c2'}}
base=ROOT/'MCM_B_v9/results'
with zipfile.ZipFile(base/'research_results_revision.zip') as z:
 assert set(z.namelist())==set(CONTRACT) and z.testzip() is None
 for name,item in CONTRACT.items():
  raw=z.read(name);assert len(raw)==item['bytes'] and hashlib.sha256(raw).hexdigest()==item['sha256']
  p=base/name
  if p.exists():
   assert hashlib.sha256(p.read_bytes()).hexdigest()==item['sha256'],f'Existing result differs: {p}'
  else:
   with tempfile.NamedTemporaryFile(dir=base,delete=False) as f:f.write(raw);temp=f.name
   os.replace(temp,p)
  print('verified',name)
