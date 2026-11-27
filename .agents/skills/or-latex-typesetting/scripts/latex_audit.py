"""Static label/citation and final-log diagnostics; this does not compile TeX."""
from pathlib import Path
import argparse,json,re,hashlib,collections
p=argparse.ArgumentParser()
p.add_argument('source',type=Path);p.add_argument('--bib',type=Path)
p.add_argument('--log',type=Path);p.add_argument('--output',type=Path)
a=p.parse_args()
bs=re.escape(chr(92))
text=re.sub('(?<!'+bs+')[%][^'+chr(10)+']*','',a.source.read_text())
labels=re.findall(bs+r'label[{]([^}]+)[}]',text)
refs=re.findall(bs+r'(?:eqref|[cC]ref|ref|autoref)[{]([^}]+)[}]',text)
cites=[k.strip() for group in re.findall(bs+r'cite[A-Za-z]*[*]?[^{}]*[{]([^}]+)[}]',text) for k in group.split(',')]
keys=re.findall(r'@[A-Za-z]+[ ]*[{][ ]*([^, }]+)',a.bib.read_text()) if a.bib else []
issues=[]
for label,count in collections.Counter(labels).items():
    if count>1:issues.append({'kind':'duplicate_label','key':label})
for key in sorted(set(refs)-set(labels)):issues.append({'kind':'undefined_ref','key':key})
for key,count in collections.Counter(keys).items():
    if count>1:issues.append({'kind':'duplicate_bib_key','key':key})
for key in sorted(set(cites)-set(keys)):issues.append({'kind':'undefined_citation','key':key})
log_status='NOT_RUN'
if a.log:
    log_status='READ';log=a.log.read_text(errors='replace')
    patterns={'tex_error':r'^! ', 'undefined_ref':r'(?:Reference|Citation).*undefined|There were undefined', 'font_or_glyph':r'Missing character:|Font shape.*undefined|font.*not found', 'overfull':'Overfull '+bs+'[hv]box', 'underfull':'Underfull '+bs+'[hv]box', 'latex_warning':r'^LaTeX Warning:|^Package .* Warning:'}
    for kind,pattern in patterns.items():
        for match in re.finditer(pattern,log,re.M|re.I):issues.append({'kind':kind,'line':log.count(chr(10),0,match.start())+1})
result={'source_sha256':hashlib.sha256(a.source.read_bytes()).hexdigest(),'labels':len(labels),'cites':len(cites),'log_status':log_status,'issues':issues,'scope':'One TeX entry and explicit bib/log only; no input/include expansion or mathematical proof','pass':not issues}
if a.output:a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+chr(10))
print(json.dumps(result,ensure_ascii=False));raise SystemExit(0 if not issues else 1)
