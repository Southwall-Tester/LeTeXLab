"""Offline UI integration tests; report fixtures exercise UI states only."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json
ROOT=Path(__file__).resolve().parents[1]

def report(lab='00',status='passed',fingerprint='a'*64):
    cs='pass' if status=='passed' else 'fail' if status=='needs_work' else 'unavailable'
    return {'schema':'latexlab.check.v2','lab':lab,'check_scope':'lab','entry':'main.tex','generated_at':'2026-10-03T00:00:00Z',
        'project_fingerprint':fingerprint,'status':status,'summary':'UI fixture, not a real build.',
        'checks':[{'id':'test-build','name':'测试条目','status':cs,'pass':cs=='pass',
            'evidence':'<img src=x onerror=alert(1)>','detail':'测试证据','next_action':'检查 main.tex。'}]}

def main():
    study=json.loads((ROOT/'selfstudy.json').read_text(encoding='utf-8'))
    with sync_playwright() as p:
        browser=p.chromium.launch(channel='msedge',headless=True)
        page=browser.new_page(viewport={'width':1440,'height':1080})
        errors=[];network=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.on('request',lambda r:network.append(r.url) if r.url.startswith(('http:','https:')) else None)
        url=(ROOT/'开始学习.html').as_uri();page.goto(url)
        assert page.locator('#labnav button').count()==8
        assert 'Boot Lab' in page.locator('#article h1').inner_text()
        assert page.locator('.statrow').count()==0
        page.locator('#tool').select_option('overleaf');page.reload()
        assert page.locator('#tool').input_value()=='overleaf'
        page.locator('#search').fill('文献');assert 0<page.locator('#labnav button').count()<8
        page.locator('#search').fill('not-a-real-keyword-xyz');assert '没有匹配' in page.locator('#labnav').inner_text()
        page.locator('#search').fill('')
        def upload_report(value):
            page.locator('#report-file').set_input_files({'name':'check-report.json','mimeType':'application/json','buffer':json.dumps(value).encode()})
            page.wait_for_timeout(100)
        upload_report(report(status='needs_work'))
        assert page.locator('#verify-pane').is_visible()
        assert page.locator('.result-item.fail').count()==1
        assert page.locator('#report-results img').count()==0
        assert '<img src=x onerror=alert(1)>' in page.locator('#report-results').inner_text()
        invalid=report();invalid['checks'][0]['status']='fail';invalid['checks'][0]['pass']=False
        upload_report(invalid);assert '未导入' in page.locator('#toast').inner_text()
        assert page.locator('.result-item.fail').count()==1
        for entry in ['main.tex','thesis/main.tex']:
            build_only=report();build_only.update(check_scope='build',entry=entry)
            upload_report(build_only);assert '仅验证了入口编译' in page.locator('#toast').inner_text()
            assert page.locator('.result-item.fail').count()==1
        page.locator('#tab-quiz').click();qs=study['00']['questions']
        for q in qs:page.locator(f'input[name="{q["id"]}"][value="{(q["answer"]+1)%3}"]').check()
        page.locator('#submit-quiz').click();assert page.locator('.feedback.retry').count()==2
        for q in qs:page.locator(f'input[name="{q["id"]}"][value="{q["answer"]}"]').check()
        assert page.locator('.feedback').count()==0
        page.locator('#submit-quiz').click();assert page.locator('.feedback.ok').count()==2
        for box in page.locator('#inspect input').all():box.check()
        assert '0 / 8' in page.locator('#progress-label').inner_text()
        upload_report(report(fingerprint='b'*64))
        page.locator('#tab-quiz').click();assert page.locator('#inspect input:checked').count()==0
        for box in page.locator('#inspect input').all():box.check()
        assert '1 / 8' in page.locator('#progress-label').inner_text()
        assert '1 关含自动核验' in page.locator('#progress-detail').inner_text()
        page.reload();assert '1 / 8' in page.locator('#progress-label').inner_text()
        page.locator('#tab-verify').click();page.locator('#route').select_option('ai')
        assert '0 / 8' in page.locator('#progress-label').inner_text()
        page.locator('#ai-note').fill('PDF 第 1 页中文和接管完成均已显示；已核对源码修改位置与最新编译日志。')
        assert '1 / 8' in page.locator('#progress-label').inner_text()
        assert '1 关为 AI 辅助记录' in page.locator('#progress-detail').inner_text()
        with page.expect_download() as d:page.locator('#download-ai').click()
        prompt=Path(d.value.path()).read_text(encoding='utf-8');assert 'Boot Lab' in prompt and '证据不足' in prompt
        with page.expect_download() as d:page.locator('#export').click()
        progress=json.loads(Path(d.value.path()).read_text(encoding='utf-8'));assert progress['version']==2 and progress['labs']['00']['route']=='ai'
        page.locator('#file').set_input_files({'name':'progress.json','mimeType':'application/json','buffer':json.dumps(progress).encode()})
        page.wait_for_timeout(100);assert '1 / 8' in page.locator('#progress-label').inner_text()
        page.locator('#file').set_input_files({'name':'bad.json','mimeType':'application/json','buffer':b'{}'})
        page.wait_for_timeout(100);assert '未导入' in page.locator('#toast').inner_text()
        page.goto(url+'#lab:01');upload_report(report());assert page.url.endswith('#lab:00') and page.locator('#verify-pane').is_visible()
        for i in range(8):
            page.goto(url+'#lab:'+str(i).zfill(2));page.locator('#tab-task').click()
            assert page.locator('#article h1').count()==1
            page.locator('#article details summary').first.click()
            assert page.locator('#article details').first.get_attribute('open') is not None
            page.locator('#tab-quiz').click();assert page.locator('#questions fieldset').count()==2
            assert page.locator('#inspect input').count()==2
        page.goto(url+'#doc:self-study');assert '自学' in page.locator('#article h1').inner_text()
        page.goto(url+'#doc:sources');assert '资料来源' in page.locator('#article h1').inner_text()
        page.evaluate("localStorage.clear();localStorage.setItem('latexlab.progress.v1',JSON.stringify({completed:['00'],tool:'vscode'}))")
        page.goto(url+'#lab:00');page.reload();assert '0 / 8' in page.locator('#progress-label').inner_text()
        assert '旧版' in page.locator('#completion').inner_text()
        page.evaluate('localStorage.clear()');page.reload()
        out=ROOT/'docs/validation';out.mkdir(exist_ok=True)
        real_path=sorted((ROOT/'_build').glob('validation-*/07-solution-main.tex/check-report.json'))[-1]
        real=json.loads(real_path.read_text(encoding='utf-8'))
        assert real['check_scope']=='lab' and real['status']=='passed'
        upload_report(real)
        assert page.url.endswith('#lab:07') and page.locator('#verify-pane').is_visible()
        assert page.locator('.result-item.pass').count()==len(real['checks'])
        assert real['project'] in page.locator('#report-results').inner_text()
        page.screenshot(path=str(out/'selfstudy-real-report.png'))
        page.evaluate('localStorage.clear()');page.goto(url+'#lab:00');page.reload()
        page.screenshot(path=str(out/'handbook-desktop.png'))
        page.locator('#tab-quiz').click();page.screenshot(path=str(out/'selfstudy-quiz.png'))
        page.set_viewport_size({'width':390,'height':844});page.goto(url+'#lab:00');page.reload()
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
        page.screenshot(path=str(out/'handbook-mobile.png'),full_page=True)
        page.goto(real_path.with_suffix('.html').as_uri())
        assert page.locator('article.pass').count()==len(real['checks'])
        assert '真实构建命令' in page.locator('#prompt').input_value()
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
        for href in page.locator('a').evaluate_all('(links)=>links.map(a=>a.getAttribute("href"))'):
            assert (real_path.parent/href).is_file(),href
        assert not errors,errors
        assert not network,network
        result={'file_protocol':True,'navigation':True,'hints':True,'report_import':True,'report_state_consistency':True,
            'report_text_injection_blocked':True,'build_only_report_rejected':True,'real_reference_report_import':True,
            'standalone_report_links_and_mobile_layout':True,
            'quiz_feedback':True,'fresh_report_resets_pdf_checks':True,
            'automatic_and_ai_routes_distinguished':True,'progress_persistence':True,'progress_export_import':True,
            'legacy_progress_not_machine_verified':True,'mobile_no_horizontal_overflow':True,'external_requests':network,
            'page_errors':errors,'report_fixtures':'UI fixtures only; backend tests cover real TeX builds.'}
        (out/'browser-check.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
        print(json.dumps(result));browser.close()
if __name__=='__main__':main()
