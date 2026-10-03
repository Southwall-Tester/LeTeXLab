"""Maintainer validation: compile reference projects and intentionally flawed starters."""
from pathlib import Path
import concurrent.futures, json, datetime, sys, importlib.util, argparse
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from lab import build_project, source_files
from selfcheck import make_report, write_report

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--labs',nargs='*');args=parser.parse_args()
    stamp=datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    target=ROOT/'_build'/('validation-'+stamp);target.mkdir(parents=True)
    labs=json.loads((ROOT/'course.json').read_text(encoding='utf-8'))
    jobs=[(l,k,'main.tex') for l in labs if not args.labs or l['id'] in args.labs for k in ['solution','starter']]
    if not args.labs or '05' in args.labs:jobs.append((labs[5],'solution','legacy/main.tex'))
    if not args.labs or '06' in args.labs:jobs.append((labs[6],'solution','thesis/main.tex'))
    def one(job):
        l,kind,entry=job
        src=ROOT/('instructor/solutions' if kind=='solution' else 'labs')/l['folder']
        if kind=='starter':src=src/'starter'
        dest=target/(l['id']+'-'+kind+'-'+entry.replace('/','-'))
        try:
            b=build_project(src,dest,entry)
            report=make_report(l,src,b,entry,ROOT,source_files)
            write_report(report,ROOT,update_latest=False)
            checks=report['checks']
            result={'lab':l['id'],'kind':kind,'entry':entry,**b,'checks':checks}
            if kind=='solution' and b['compiled'] and entry=='main.tex':
                import shutil
                p=ROOT/'instructor/previews';p.mkdir(exist_ok=True)
                shutil.copy2(b['pdf'],p/(l['folder']+'.pdf'))
            return result
        except Exception as e:return {'lab':l['id'],'kind':kind,'entry':entry,'error':str(e)}
    results=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        for r in pool.map(one,jobs):
            results.append(r)
            print(json.dumps({k:r.get(k) for k in ['lab','kind','entry','compiled','exit_code','error']},ensure_ascii=False),flush=True)
    (target/'results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
    print('REPORT',target/'results.json')

if __name__=='__main__':main()
