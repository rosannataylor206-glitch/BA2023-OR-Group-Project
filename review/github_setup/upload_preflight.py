"""Read-only sharing preflight; never prints matched secret/contact values."""
from pathlib import Path
import hashlib,json,re,zipfile,collections,sys
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'review/github_setup'
BASE=json.loads((ROOT/'review/00_skill_checks.json').read_text())['original_files_sha256']
files=[p for p in ROOT.rglob('*') if p.is_file() and not any(x in p.relative_to(ROOT).parts for x in ['.git','.tools','__pycache__']) and not p.is_symlink()]
changes=[]
for name,h in BASE.items():
 p=ROOT/name
 if not p.exists():changes.append({'path':name,'status':'missing'})
 elif hashlib.sha256(p.read_bytes()).hexdigest()!=h:changes.append({'path':name,'status':'changed'})
patterns={
 'private_key':r'-----BEGIN (?:RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----',
 'github_token':r'\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})\b',
 'openai_key':r'\bsk-(?:proj-)?[A-Za-z0-9_-]{25,}\b',
 'aws_access_key':r'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b',
 'credential_assignment':r'''(?im)(?:api[_-]?key|secret|password|access[_-]?token|auth[_-]?token)\s*[=:]\s*["'][^"'\n]{8,}["']''',
 'credential_url':r'https?://[^\s/@:]+:[^\s/@]+@',
 'email':r'(?<![\w.-])[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',
 'china_mobile':r'(?<!\d)1[3-9]\d{9}(?!\d)',
 'local_user_path':r'(?:/Users/[^/\s]+/|C:\\Users\\[^\\\s]+\\)',
}
findings=[];errors=[];large=[];archives=[];metadata=[];types=collections.Counter();nested=[];symlinks=[]
for p in ROOT.rglob('*'):
 if '.tools' in p.relative_to(ROOT).parts:continue
 if (p.name=='.git' and p.parent!=ROOT) or p.name=='.gitmodules':nested.append(str(p.relative_to(ROOT)))
 if p.is_symlink():symlinks.append(str(p.relative_to(ROOT)))
for p in files:
 name=p.relative_to(ROOT).as_posix();types[p.suffix.lower()]+=1
 if name.startswith('review/github_setup/'):continue
 size=p.stat().st_size
 if size>=10*1024*1024:large.append({'path':name,'bytes':size})
 chunks=[]
 try:
  if p.suffix.lower() in ['.docx','.xlsx']:
   with zipfile.ZipFile(p) as z:
    for item in z.namelist():
     if item.endswith('.xml') and (item.startswith(('word/','xl/')) or item=='docProps/core.xml'):
      raw=z.read(item).decode('utf-8','replace')
      if item=='docProps/core.xml':
       tags=re.findall(r'<(?:dc:creator|cp:lastModifiedBy)>(.*?)</',raw)
       if any(t.strip() for t in tags):metadata.append({'path':name,'part':item,'nonempty_author_fields':True})
      chunks.append((item,re.sub(r'<[^>]+>',' ',raw)))
  elif p.suffix.lower()=='.pdf':
   from pypdf import PdfReader
   pdf=PdfReader(p)
   if pdf.metadata and pdf.metadata.get('/Author'):metadata.append({'path':name,'part':'PDF metadata','nonempty_author_fields':True})
   chunks.extend((f'page {i+1}',page.extract_text() or '') for i,page in enumerate(pdf.pages))
  elif p.suffix.lower() in ['.zip','.rar','.7z']:
   if p.suffix.lower()=='.zip':
    with zipfile.ZipFile(p) as z:archives.append({'path':name,'entries':len(z.namelist()),'uncompressed_bytes':sum(x.file_size for x in z.infolist()),'content_scan':'NOT_SCANNED; exclude archive'})
   continue
  else:
   raw=p.read_bytes()
   if b'\0' not in raw[:4096]:chunks=[('text',raw.decode('utf-8','replace'))]
  for loc,text in chunks:
   for kind,regex in patterns.items():
    hits=list(re.finditer(regex,text))
    if hits:findings.append({'path':name,'location':loc,'kind':kind,'matches':len(hits),'line':text.count('\n',0,hits[0].start())+1,'value':'OMITTED'})
 except Exception as e:errors.append({'path':name,'error_type':type(e).__name__})
report={'original_files':len(BASE),'original_hash_changes':changes,'nested_git':nested,'symlinks':symlinks,'large_files_internal_threshold_10MiB':large,'findings':findings,'author_metadata':metadata,'archives':archives,'extraction_errors':errors,'extensions':dict(types),'limitations':['Regex scan is not a guarantee of absence of secrets or personal information.','PDF scans cover extractable text, not OCR or image content.','Author metadata and identifiers require human sharing consent.','Rights and third-party redistribution cannot be inferred from file names.','Archives were inventoried, not recursively scanned; excluded from upload.']}
(OUT/'preflight.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'original_files':len(BASE),'hash_changes':len(changes),'nested_git':nested,'large_files':large,'finding_kinds':dict(collections.Counter(f['kind'] for f in findings)),'metadata_files':len(metadata),'archives':len(archives),'extraction_errors':errors},ensure_ascii=False))
