"""Build the standalone, file:// compatible handbook and source starter archives."""
from pathlib import Path
import json, zipfile, re
import markdown

ROOT=Path(__file__).resolve().parents[1]
def main():
    labs=json.loads((ROOT/'course.json').read_text(encoding='utf-8'))
    for lab in labs:
        source=(ROOT/'labs'/lab['folder']/'HANDOUT.md').read_text(encoding='utf-8')
        lab['body']=markdown.markdown(source,extensions=['tables','fenced_code','md_in_html'])
        # Markdown nested inside native details should still be rendered.
        lab['body']=re.sub(r'(<details><summary>.*?</summary>)(.*?)(</details>)',lambda m:m[1]+markdown.markdown(m[2])+m[3],lab['body'],flags=re.S)
    docs=[]
    for filename,title in [('SELF-STUDY.md','自学与核验'),('TOOLS.md','工具与编译'),('AI-WORKFLOW.md','智能体协作'),('QUICKREF.md','故障速查'),('TEMPLATE-TRANSFER.md','模板迁移'),('COVERAGE.md','知识覆盖'),('../sources/README.md','资料来源')]:
        docs.append({'id':'sources' if filename.startswith('../') else Path(filename).stem.lower(),'title':title,'body':markdown.markdown((ROOT/'docs'/filename).read_text(encoding='utf-8'),extensions=['tables','fenced_code'])})
    study=json.loads((ROOT/'selfstudy.json').read_text(encoding='utf-8'))
    data=json.dumps({'labs':labs,'docs':docs,'study':study},ensure_ascii=False).replace('</',r'<\/')
    template=(ROOT/'tools/handbook.template.html').read_text(encoding='utf-8')
    js=(ROOT/'tools/handbook.js').read_text(encoding='utf-8')
    (ROOT/'开始学习.html').write_text(template.replace('__COURSE_DATA__',data).replace('__HANDBOOK_JS__',js),encoding='utf-8')
    downloads=ROOT/'downloads';downloads.mkdir(exist_ok=True)
    for lab in labs:
        src=ROOT/'labs'/lab['folder']/'starter'
        with zipfile.ZipFile(downloads/(lab['folder']+'.zip'),'w',zipfile.ZIP_DEFLATED) as z:
            for f in src.rglob('*'):
                if f.is_file():z.write(f,f.relative_to(src))
    print('Built offline handbook and 8 independent starter archives.')

if __name__=='__main__':main()
