"""Focused integration evidence for six faults and relocatable source delivery."""
from pathlib import Path
import sys, json, datetime, subprocess, zipfile, shutil
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'))
from lab import build_project, source_files

def main():
    base=ROOT/'_build'/('targeted-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S'));base.mkdir(parents=True)
    src=base/'rescue-source';shutil.copytree(ROOT/'labs/02-rescue/starter',src)
    main=src/'main.tex';steps=[]
    fixes=[('命令拼写',r'\sectoin{',r'\section{'),('正文特殊字符','A&B',r'A\&B'),('环境闭合',r'\end{enumerate}',r'\end{itemize}'),('缺宏包','graphicx,array','graphicx,booktabs,array'),('引用键',r'\ref{tab:result}',r'\ref{tab:results}'),('溢出尺寸',r'1.35\linewidth',r'0.9\linewidth')]
    for i in range(7):
        r=build_project(src,base/f'phase-{i}')
        steps.append({'phase':i,'last_fix':'未修复' if not i else fixes[i-1][0],'compiled':r['compiled'],'errors':r['errors'],'warnings':r['warnings']})
        if i<6:
            _,a,b=fixes[i];s=main.read_text(encoding='utf-8');assert a in s,(i,a);main.write_text(s.replace(a,b),encoding='utf-8')
    assert all(not s['compiled'] for s in steps[:4])
    assert all(s['compiled'] for s in steps[4:])
    assert any('undefined' in w.lower() for w in steps[4]['warnings'])
    assert any('Overfull' in w for w in steps[5]['warnings'])
    assert not steps[6]['warnings']
    print('Six-fault progression verified.',flush=True)
    archive=base/'submission.zip';original=ROOT/'instructor/solutions/07-submission'
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
        for p in source_files(original):z.write(p,p.relative_to(original))
    extracted=base/'moved project';extracted.mkdir()
    with zipfile.ZipFile(archive) as z:
        assert 'main.tex' in z.namelist() and 'figures/baseline.pdf' in z.namelist()
        assert not any(n.endswith('.aux') for n in z.namelist());z.extractall(extracted)
    moved=build_project(extracted,base/'relocated-build');assert moved['compiled'] and not moved['warnings']
    recipe=subprocess.run(['latexmk','-xelatex','-interaction=nonstopmode','-halt-on-error','-file-line-error','main.tex'],cwd=base/'relocated-build',stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
    (base/'latexmk-transcript.txt').write_bytes(recipe.stdout)
    assert recipe.returncode==0,recipe.stdout.decode(errors='replace')[-2000:]
    result={'fault_progression':steps,'zip_relocation_compiled':True,'latexmk_recipe_exit':recipe.returncode,'relocated_pdf':moved['pdf']}
    (base/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Package extraction, relocation and latexmk verified. REPORT',base/'results.json')
if __name__=='__main__':main()
