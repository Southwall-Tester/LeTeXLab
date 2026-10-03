'use strict';
const course=JSON.parse(document.getElementById('course-data').textContent),$=id=>document.getElementById(id);
const storageKey='latexlab.progress.v2',labIds=course.labs.map(l=>l.id),tools=['vscode','texstudio','overleaf','other'];
let state={version:2,tool:'vscode',labs:{},legacyCompleted:[]},current='00',currentTab='task',nextTab=null;
const emptyLab=()=>({route:'auto',answers:{},tested:false,inspect:{},aiNote:'',report:null});
function validReport(r){
 if(!r||r.schema!=='latexlab.check.v2'||!labIds.includes(r.lab)||!['passed','needs_work','blocked'].includes(r.status)||!Array.isArray(r.checks)||!r.checks.length||r.checks.length>120)throw Error('不是本工具生成的新版核验报告');
 if(typeof r.project_fingerprint!=='string'||typeof r.generated_at!=='string')throw Error('报告缺少工程标识或生成时间');
 if(r.check_scope!=='lab'||r.entry!=='main.tex')throw Error('这份报告仅验证了入口编译；请运行本关 check 命令，再导入主关报告');
 const ids=new Set();for(const c of r.checks){if(typeof c.id!=='string'||ids.has(c.id)||typeof c.name!=='string'||!['pass','fail','unavailable'].includes(c.status)||c.pass!==(c.status==='pass'))throw Error('核验条目格式或状态不一致');ids.add(c.id);}
 if(r.status==='passed'&&r.checks.some(c=>c.status!=='pass'))throw Error('报告总状态与条目不一致');
 return r;
}
function validateState(v){
 if(v.version===1&&Array.isArray(v.completed)&&tools.includes(v.tool))return {version:2,tool:v.tool,labs:{},legacyCompleted:v.completed.filter(x=>labIds.includes(x))};
 if(v.version!==2||!tools.includes(v.tool)||!v.labs||typeof v.labs!=='object'||Array.isArray(v.labs))throw Error('进度文件格式不正确');
 const result={version:2,tool:v.tool,labs:{},legacyCompleted:Array.isArray(v.legacyCompleted)?v.legacyCompleted.filter(x=>labIds.includes(x)):[]};
 for(const id of labIds){const l=v.labs[id];if(!l)continue;if(!['auto','ai'].includes(l.route)||typeof l.answers!=='object'||!l.answers||Array.isArray(l.answers)||typeof l.inspect!=='object'||!l.inspect||Array.isArray(l.inspect)||typeof l.aiNote!=='string')throw Error('关卡记录格式不正确');const clean=emptyLab();clean.route=l.route;clean.aiNote=l.aiNote.slice(0,12000);clean.tested=l.tested===true;
  for(const q of course.study[id].questions){const a=l.answers[q.id];if(Number.isInteger(a)&&a>=0&&a<q.options.length)clean.answers[q.id]=a;}
  for(const item of course.study[id].inspect)clean.inspect[item.id]=l.inspect[item.id]===true;
  if(l.report){clean.report=validReport(l.report);if(clean.report.lab!==id)throw Error('报告关卡与进度不对应');}
  result.labs[id]=clean;
 }
 return result;
}
try{const saved=localStorage.getItem(storageKey)||localStorage.getItem('latexlab.progress.v1');if(saved){const v=JSON.parse(saved);if(!v.version)v.version=1;state=validateState(v);}}catch(e){$('storage-note').textContent='无法读取保存的进度。可以继续使用，或导入已导出的进度文件。';}
function learning(id=current){if(!state.labs[id])state.labs[id]=emptyLab();return state.labs[id];}
function save(){try{localStorage.setItem(storageKey,JSON.stringify(state));}catch(e){$('storage-note').textContent='本地进度未能保存，请使用“导出进度”。';}}
function toast(s){$('toast').textContent=s;$('toast').hidden=false;setTimeout(()=>$('toast').hidden=true,4500);}
function element(tag,text,cls){const e=document.createElement(tag);if(text!==undefined)e.textContent=text;if(cls)e.className=cls;return e;}
function status(id){const l=learning(id),c=course.study[id];const quiz=l.tested&&c.questions.every(q=>l.answers[q.id]===q.answer);const inspect=c.inspect.every(x=>l.inspect[x.id]);const evidence=l.route==='auto'?!!l.report&&l.report.status==='passed':l.aiNote.trim().length>0;return {quiz,inspect,evidence,complete:quiz&&inspect&&evidence,route:l.route};}
function nav(){
 const q=$('search').value.trim().toLowerCase();$('labnav').replaceChildren();$('docnav').replaceChildren();
 for(const lab of course.labs){if(q&&!JSON.stringify(lab).toLowerCase().includes(q))continue;const b=element('button',undefined,'nav-item');b.setAttribute('aria-current',current===lab.id?'page':'false');b.append(element('span',lab.id,'num'),element('span',lab.name.split(' · ')[1],'nav-name'),element('span',status(lab.id).complete?'✓':'','dot'));b.onclick=()=>location.hash='lab:'+lab.id;$('labnav').append(b);}
 if(!$('labnav').children.length)$('labnav').append(element('div','没有匹配的关卡','empty'));
 for(const d of course.docs){if(q&&!(d.title+d.body).toLowerCase().includes(q))continue;const b=element('button',d.title,'nav-item');b.setAttribute('aria-current',current==='doc:'+d.id?'page':'false');b.onclick=()=>location.hash='doc:'+d.id;$('docnav').append(b);}
 const completed=labIds.filter(id=>status(id).complete),auto=completed.filter(id=>learning(id).route==='auto').length;$('fill').style.width=(completed.length/8*100)+'%';$('progress-label').textContent=completed.length+' / 8 自学流程完成';$('progress-detail').textContent=completed.length?`${auto} 关含自动核验 · ${completed.length-auto} 关为 AI 辅助记录`:'';document.querySelector('.track').setAttribute('aria-valuenow',completed.length);
}
function renderTools(){const notes={vscode:'打开工作工程，使用 XeLaTeX 构建配方。完成修改后，在项目根目录运行本关 check 命令。',texstudio:'用所选编辑器修改和编译；再用本关 check 命令产生核验报告。',overleaf:'上传起始包，选择 XeLaTeX。下载修改后的源码包到本地运行核验，或切换到 AI 辅助核对并提供真实 PDF 和日志。',other:'编辑器任选；本地 check 命令会在副本中运行编译和核验。'};$('tool').value=state.tool;$('tool-note').textContent=notes[state.tool];}
function switchTab(tab){currentTab=tab;for(const t of ['task','verify','quiz']){const b=$('tab-'+t);b.setAttribute('aria-selected',String(t===tab));$(t==='task'?'article':t+'-pane').hidden=t!==tab;} }
function renderCompletion(){
 const s=status(current),l=learning();$('completion').replaceChildren();const rows=[[s.evidence,l.route==='auto'?'自动核验报告通过':'已填写 AI 核对依据'],[s.quiz,'理解自测已答对'],[s.inspect,'PDF 自查已完成']];
 for(const [yes,text] of rows){const line=element('div',undefined,'completion-row');line.append(element('span',yes?'✓':'○',yes?'ok':'muted'),element('span',text));$('completion').append(line);}
 $('completion-note').textContent=s.complete?'本关自学流程已完成。修改源码后请重新核验。':'完成以下三项即可记录本关进度，无需老师确认。';
 if(state.legacyCompleted.includes(current))$('completion').append(element('p','旧版自评标记已保留；本版另行记录核验与自测。','micro'));
 $('tab-verify').textContent='核验结果'+(l.report?' · '+({'passed':'通过','needs_work':'待修改','blocked':'未完成检测'}[l.report.status]):'');
}
function renderReport(){
 const l=learning();$('route').value=l.route;$('auto-route').hidden=l.route!=='auto';$('ai-route').hidden=l.route!=='ai';$('ai-note').value=l.aiNote;
 $('command').textContent='python tools/lab.py check '+current;$('report-latest').textContent='reports/latest-'+current+'.json';
 const box=$('report-results');box.replaceChildren();const r=l.report;
 if(!r){box.append(element('p','尚未导入报告。先执行命令，再选择生成的 JSON 文件。','muted'));return;}
 const heading=element('div',undefined,'result-heading '+r.status);heading.append(element('strong',{'passed':'自动核验通过','needs_work':'发现需要修改的项目','blocked':'部分检测尚未完成'}[r.status]));box.append(heading);
 box.append(element('p','报告时间：'+r.generated_at+' · 工程指纹：'+r.project_fingerprint.slice(0,12),'micro'));
 if(r.project)box.append(element('p','核验工程：'+r.project,'source-location'));
 box.append(element('p','此结果对应生成报告时的源码。修改后重新运行 check 并导入新报告。','micro'));
 const summary=typeof r.summary==='string'?r.summary:r.summary?.message;if(summary)box.append(element('p',summary));
 for(const c of r.checks){const d=element('details',undefined,'result-item '+c.status);d.open=c.status!=='pass';const label={pass:'通过',fail:'需修改',unavailable:'未检测'}[c.status];d.append(element('summary',label+' · '+c.name));if(c.file)d.append(element('p',c.file+(c.line?':'+c.line:''),'source-location'));for(const [label,value] of [['证据',c.evidence],['说明',c.detail],['下一步',c.next_action]]){if(!value)continue;d.append(element('div',label,'micro'));d.append(element('pre',typeof value==='string'?value:JSON.stringify(value,null,2)));}box.append(d);}
 if(r.pdf)box.append(element('p','本次 PDF：'+r.pdf,'source-location'));
 const clear=element('button','清除当前报告','smallbtn');clear.onclick=()=>{learning().report=null;save();renderReport();renderCompletion();nav();};box.append(clear);
}
function renderQuiz(){
 const l=learning(),study=course.study[current],form=$('questions');form.replaceChildren();
 for(const q of study.questions){const field=element('fieldset');field.append(element('legend',q.prompt));q.options.forEach((option,i)=>{const label=element('label',undefined,'answer-option'),input=element('input');input.type='radio';input.name=q.id;input.value=String(i);input.checked=l.answers[q.id]===i;input.onchange=()=>{l.answers[q.id]=i;l.tested=false;document.querySelectorAll('#questions .feedback').forEach(x=>x.remove());save();$('quiz-result').textContent='答案已修改，请重新核对。';renderCompletion();nav();};label.append(input,element('span',option));field.append(label);});if(l.tested){const correct=l.answers[q.id]===q.answer;const explanation=element('p',(correct?'理解正确。':'再检查一下。')+q.explanation,correct?'feedback ok':'feedback retry');field.append(explanation);}form.append(field);}
 const all=l.tested&&study.questions.every(q=>l.answers[q.id]===q.answer);$('quiz-result').textContent=l.tested?(all?'这组理解题已答对。':'对照解释修改答案，再试一次。'):'';
 const checks=$('inspect');checks.replaceChildren();for(const item of study.inspect){const label=element('label',undefined,'inspection'),input=element('input');input.type='checkbox';input.checked=l.inspect[item.id]===true;input.onchange=()=>{l.inspect[item.id]=input.checked;save();renderCompletion();nav();};const body=element('span');body.append(element('strong',item.prompt),element('span',item.why,'micro'));label.append(input,body);checks.append(label);}
}
function render(){
 let hash='';try{hash=decodeURIComponent(location.hash.slice(1));}catch(e){}const id=hash.startsWith('lab:')?hash.slice(4):hash||'00',doc=course.docs.find(d=>'doc:'+d.id===id);
 if(doc){current=id;document.body.classList.add('document');$('article').innerHTML=doc.body;$('article').hidden=false;$('verify-pane').hidden=$('quiz-pane').hidden=true;$('study-tabs').hidden=true;$('prev').hidden=$('next').hidden=true;$('notice').textContent='按需查阅工具、核验方法和证据说明。';}
 else{const lab=course.labs.find(l=>l.id===id)||course.labs[0];current=lab.id;document.body.classList.remove('document');$('article').innerHTML=lab.body;$('study-tabs').hidden=false;$('download').href='downloads/'+lab.folder+'.zip';$('handout').href='labs/'+lab.folder+'/HANDOUT.md';$('solution').href='instructor/solutions/'+lab.folder+'/main.tex';$('preview').href='instructor/previews/'+lab.folder+'.pdf';$('local-path').textContent='工作目录：work/'+lab.folder;$('prev').hidden=$('next').hidden=false;$('prev').disabled=lab.id==='00';$('next').disabled=lab.id==='07';$('notice').textContent='修改工程 → 查看核验结果 → 完成理解自测与 PDF 自查。';renderReport();renderQuiz();renderCompletion();switchTab(currentTab);}
 nav();renderTools();
}
function download(name,text,type='text/plain'){const a=document.createElement('a'),url=URL.createObjectURL(new Blob([text],{type}));a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}
function aiPrompt(){const lab=course.labs.find(x=>x.id===current),l=learning();let p=`我正在自学 ${lab.name}。\n${course.study[current].ai_prompt}\n\n任务要求：\n`+lab.tasks.map((t,i)=>`${i+1}. ${t}`).join('\n');p+='\n\n请逐条输出：已验证 / 发现问题 / 证据不足；给出文件行号或PDF页码和最小修改提示。没有源码、PDF或实际日志时先列明缺少什么，不假装已经编译或看过输出。允许帮助生成代码，但要让我解释修改并完成一个变式。不要以你的判断代替本地自动核验结果。\n';if(l.report)p+='\n已有核验报告：\n'+JSON.stringify(l.report,null,2);p+='\n\n我会另外附上当前源码、CSV/文献库、PDF和最后一次构建日志。';return p;}
async function copy(text){try{await navigator.clipboard.writeText(text);toast('已复制。');}catch(e){$('copy-fallback').value=text;$('copy-dialog').showModal();$('copy-fallback').focus();$('copy-fallback').select();}}
for(const t of ['task','verify','quiz'])$('tab-'+t).onclick=()=>switchTab(t);
$('search').oninput=nav;$('tool').onchange=()=>{state.tool=$('tool').value;save();renderTools();};$('route').onchange=()=>{learning().route=$('route').value;save();renderReport();renderCompletion();nav();};
$('copy-command').onclick=()=>copy($('command').textContent);$('copy-ai').onclick=()=>copy(aiPrompt());$('download-ai').onclick=()=>download('latexlab-'+current+'-ai-review.txt',aiPrompt());$('copy-close').onclick=()=>$('copy-dialog').close();
$('ai-note').oninput=()=>{learning().aiNote=$('ai-note').value;save();renderCompletion();nav();};
$('submit-quiz').onclick=()=>{const l=learning();if(course.study[current].questions.some(q=>!Number.isInteger(l.answers[q.id]))){$('quiz-result').textContent='请先选择每道题的答案。';return;}l.tested=true;save();renderQuiz();renderCompletion();nav();};
$('load-report').onclick=()=>$('report-file').click();$('report-file').onchange=async()=>{const f=$('report-file').files[0];if(!f)return;try{if(f.size>3000000)throw Error('报告超过 3 MB，请重新生成或查看独立报告');const report=validReport(JSON.parse(await f.text()));const l=learning(report.lab);if(l.report?.project_fingerprint!==report.project_fingerprint)l.inspect={};l.report=report;l.route='auto';save();currentTab='verify';nextTab=location.hash!=='#lab:'+report.lab?'verify':null;location.hash='lab:'+report.lab;render();toast('已导入 Lab '+report.lab+' 的核验结果。');}catch(e){toast('未导入：'+e.message);}$('report-file').value='';};
$('prev').onclick=()=>location.hash='lab:'+String(Number(current)-1).padStart(2,'0');$('next').onclick=()=>location.hash='lab:'+String(Number(current)+1).padStart(2,'0');window.addEventListener('hashchange',()=>{currentTab=nextTab||'task';nextTab=null;render();(current.startsWith('doc:')?$('article'):$('study-tabs')).scrollIntoView({block:'start'});});
$('print').onclick=()=>{document.querySelectorAll('article details, .result-item').forEach(d=>d.open=true);window.print();};
$('export').onclick=()=>download('latexlab-progress.json',JSON.stringify(state,null,2),'application/json');$('import').onclick=()=>$('file').click();$('file').onchange=async()=>{const f=$('file').files[0];if(!f)return;try{if(f.size>5000000)throw Error();state=validateState(JSON.parse(await f.text()));save();render();toast('已导入自学进度。');}catch(e){toast('未导入：进度文件无效。');}$('file').value='';};render();
