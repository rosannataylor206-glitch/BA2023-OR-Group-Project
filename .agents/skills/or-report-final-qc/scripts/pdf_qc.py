"""Read-only PDF structural/text/font diagnostics; visual judgment is separate."""
from pathlib import Path
import argparse,json,hashlib
import pymupdf as fitz
p=argparse.ArgumentParser();p.add_argument('pdf',type=Path);p.add_argument('--output',type=Path);a=p.parse_args()
doc=fitz.open(a.pdf);pages=[];font_info={}
for i,page in enumerate(doc):
 rect=page.rect;text=page.get_text();outside=[]
 for block in page.get_text('dict')['blocks']:
  for line in block.get('lines',[]):
   for span in line.get('spans',[]):
    box=fitz.Rect(span['bbox'])
    if not rect.contains(box):outside.append({'text':span['text'][:60],'bbox':list(box)})
 for font in page.get_fonts(full=True):
  xref=font[0]
  if xref not in font_info:
   try:name,ext,kind,content=doc.extract_font(xref);font_info[xref]={'name':name,'format':ext,'embedded_bytes':len(content)}
   except Exception:font_info[xref]={'name':font[3],'status':'UNVERIFIED'}
 pages.append({'page':i+1,'width_pt':rect.width,'height_pt':rect.height,'text_chars':len(text.strip()),'outside_text_candidates':outside})
result={'pdf_sha256':hashlib.sha256(a.pdf.read_bytes()).hexdigest(),'page_count':len(doc),'encrypted':doc.is_encrypted,'pages':pages,'fonts':list(font_info.values()),'scope':'PDF parse/text/geometry/font diagnostics only; empty text and box candidates require human interpretation; no submission-ready verdict'}
if a.output:a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False))
