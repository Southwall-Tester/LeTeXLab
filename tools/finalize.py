"""Collect final validation metadata and produce a portable course archive."""
from pathlib import Path
import json, zipfile, shutil, hashlib, sys
ROOT=Path(__file__).resolve().parents[1]
def main():
    latest={}
    for p in sorted((ROOT/'_build').glob('validation-*/results.json')):
        for r in json.loads(p.read_text(encoding='utf-8')):latest[(r['lab'],r['kind'],r['entry'])]=r
    references=[r for r in latest.values() if r['kind']=='solution']
    assert len(references)==10
    assert all(r['compiled'] and all(x['pass'] for x in r['checks']) and not r['warnings'] for r in references)
    out=ROOT/'docs/validation';out.mkdir(exist_ok=True)
    # Keep portable evidence rather than embedding local absolute paths in the archive.
    def portable(v):
        if isinstance(v,str):return v.replace(str(ROOT),'${PROJECT_ROOT}')
        if isinstance(v,list):return [portable(x) for x in v]
        if isinstance(v,dict):return {k:portable(x) for k,x in v.items()}
        return v
    (out/'compile-results.json').write_text(json.dumps(portable(list(latest.values())),ensure_ascii=False,indent=2),encoding='utf-8')
    summaries=sorted((ROOT/'_build').glob('validation-*/selfcheck-v2-summary.json'))
    if summaries:(out/'selfcheck-v2-summary.json').write_text(json.dumps(portable(json.loads(summaries[-1].read_text(encoding='utf-8'))),ensure_ascii=False,indent=2),encoding='utf-8')
    for r in references:
        logdir=Path(r['build_dir']);label=r['lab']+'-'+r['entry'].replace('/','-')
        dest=out/'logs'/label;dest.mkdir(parents=True,exist_ok=True)
        for p in [logdir/'build-transcript.txt',logdir/Path(r['entry']).with_suffix('.log')]:
            if p.exists():(dest/p.name).write_text(p.read_text(encoding='utf-8',errors='replace').replace(str(ROOT),'${PROJECT_ROOT}'),encoding='utf-8')
    targeted=sorted((ROOT/'_build').glob('targeted-*/results.json'))[-1]
    (out/'targeted-results.json').write_text(json.dumps(portable(json.loads(targeted.read_text(encoding='utf-8'))),ensure_ascii=False,indent=2),encoding='utf-8')
    labs=json.loads((ROOT/'course.json').read_text(encoding='utf-8'))
    for l in labs:
        with zipfile.ZipFile(ROOT/'downloads'/(l['folder']+'.zip')) as z:
            assert z.testzip() is None
            assert {'main.tex','REPORT.md'}<=set(z.namelist())
            for name in z.namelist():assert z.read(name)==(ROOT/'labs'/l['folder']/'starter'/name).read_bytes()
        assert (ROOT/'instructor/previews'/(l['folder']+'.pdf')).exists()
    bundle=ROOT/'dist/LaTeXLab-course.zip';bundle.parent.mkdir(exist_ok=True)
    excludes={'_build','work','reports','dist','.git','__pycache__'}
    with zipfile.ZipFile(bundle,'w',zipfile.ZIP_DEFLATED) as z:
        for p in ROOT.rglob('*'):
            if not p.is_file() or any(x in excludes for x in p.relative_to(ROOT).parts):continue
            z.write(p,Path('LaTeXLab')/p.relative_to(ROOT))
    with zipfile.ZipFile(bundle) as z:assert z.testzip() is None
    print('10 reference entrypoints verified; 8 starter archives verified; bundle:',bundle,'bytes:',bundle.stat().st_size)
if __name__=='__main__':main()
