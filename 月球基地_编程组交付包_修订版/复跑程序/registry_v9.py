"""Lossless shared transport-certificate storage; mathematical content unchanged."""
from pathlib import Path
import hashlib,json


def save_phase_registry(path,phases):
    unique={};object_ids={};compact={}
    for key,phase in phases.items():
        p=dict(phase)
        if 'entries' in p:
            entries=[]
            for entry in p['entries']:
                e=dict(entry)
                if 'transport' in e:
                    t=e.pop('transport');oid=id(t)
                    tid=object_ids.get(oid)
                    if tid is None:
                        tid=hashlib.sha256(json.dumps(t,sort_keys=True,separators=(',',':')).encode()).hexdigest()
                        object_ids[oid]=tid;unique[tid]=t
                    e['transport_ref']=tid
                entries.append(e)
            p['entries']=entries
        compact[key]=p
    payload=dict(schema='v9_lossless_shared_transport_registry',phases=compact,transports=unique)
    Path(path).write_text(json.dumps(payload,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
    return dict(phases=len(phases),unique_transport_certificates=len(unique))


def load_phase_registry(path):
    raw=json.loads(Path(path).read_text(encoding='utf-8'))
    if raw.get('schema')!='v9_lossless_shared_transport_registry':return raw
    ts=raw['transports']
    for tid,t in ts.items():
        actual=hashlib.sha256(json.dumps(t,sort_keys=True,separators=(',',':')).encode()).hexdigest()
        if actual!=tid:raise ValueError('Transport-certificate content hash mismatch')
    phases=raw['phases']
    for p in phases.values():
        for e in p.get('entries',[]):
            if 'transport_ref' in e:e['transport']=ts[e.pop('transport_ref')]
    return phases
