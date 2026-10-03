"""Local LaTeXLab helper: copy starters, compile a fresh copy, check and package.

Python 3.9+; an editor is optional. Checks describe observed technical conditions,
not learning mastery. No source file is changed by build or check.
"""
from pathlib import Path
import argparse
import datetime
import json
import re
import shutil
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
IGNORE = {'_build', '.git', '__pycache__', 'node_modules', 'reports', '.pytest_cache'}
GENERATED = {'.aux', '.log', '.out', '.toc', '.lof', '.lot', '.bcf', '.bbl', '.blg', '.fls', '.fdb_latexmk', '.xdv', '.synctex', '.gz', '.pyc'}
GENERATED_NAMES = {'check-report.json', 'check-report.html', 'ai-review-prompt.txt', 'build-transcript.txt', 'pdf-text.txt', 'pdf-info.txt'}


def course():
    return json.loads((ROOT / 'course.json').read_text(encoding='utf-8'))


def labinfo(lab):
    return next(x for x in course() if x['id'] == str(lab).zfill(2))


def source_files(project):
    project = Path(project)
    for p in sorted(project.rglob('*')):
        parts = p.relative_to(project).parts
        if not p.is_file() or any(x in IGNORE or x.startswith('biber-cache') for x in parts):
            continue
        if p.suffix.lower() in GENERATED or p.name in GENERATED_NAMES or p.name.endswith('.run.xml'):
            continue
        if p.suffix.lower() == '.pdf' and 'figures' not in parts:
            continue
        if p.suffix.lower() == '.zip':
            continue
        yield p


def copy_sources(src, dst):
    for p in source_files(src):
        q = dst / p.relative_to(src)
        q.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, q)


def active_tex(project, entry):
    """Follow literal input/include paths only; arbitrary TeX is not parsed."""
    from selfcheck import literal_sources
    return '\n'.join(literal_sources(Path(project), entry).values())


def build_project(project, output, entry='main.tex'):
    project = Path(project).resolve()
    output = Path(output).resolve()
    output.mkdir(parents=True, exist_ok=False)
    copy_sources(project, output)
    entry_path = output / entry
    working = entry_path.parent
    stem = entry_path.stem
    logs, executed, errors = [], [], []
    blocked = None
    command = ['xelatex', '-no-shell-escape', '-recorder', '-synctex=1', '-interaction=nonstopmode', '-halt-on-error', '-file-line-error', entry_path.name]

    def run(cmd):
        nonlocal blocked
        if not shutil.which(cmd[0]):
            blocked = 'missing_tool'
            logs.append('ENVIRONMENT: 找不到 ' + cmd[0] + '。安装 TeX 发行版或把其 bin 目录加入 PATH 后重试。')
            return 127
        executed.append(cmd)
        try:
            result = subprocess.run(cmd, cwd=working, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120)
        except subprocess.TimeoutExpired as exc:
            blocked = 'timeout'
            logs.append((exc.stdout or b'').decode('utf-8', errors='replace'))
            logs.append('TIMEOUT: ' + ' '.join(cmd))
            return 124
        except OSError as exc:
            blocked = 'execution_error'
            logs.append('ENVIRONMENT: ' + str(exc))
            return 126
        logs.append(result.stdout.decode('utf-8', errors='replace'))
        return result.returncode

    if not entry_path.is_file():
        code = 2
        logs.append('找不到主文件：' + str(project / entry))
    else:
        code = run(command)
        if code == 0:
            if (working / (stem + '.bcf')).exists():
                code = run(['biber', stem])
            elif (working / (stem + '.aux')).exists() and '\\bibdata' in (working / (stem + '.aux')).read_text(errors='replace'):
                code = run(['bibtex', stem])
        if code == 0:
            for _ in range(2):
                code = run(command)
                if code:
                    break
    transcript = output / 'build-transcript.txt'
    transcript.write_text('\n\n'.join(logs), encoding='utf-8')
    log = working / (stem + '.log')
    final_log = log.read_text(encoding='utf-8', errors='replace') if log.exists() else '\n'.join(logs)
    warnings = []
    for pattern in [r'[^\n]*LaTeX Warning:[^\n]*', r'[^\n]*Package \S+ Warning:[^\n]*', r'[^\n]*Overfull \\[hv]box[^\n]*', r'[^\n]*Missing character:[^\n]*']:
        warnings.extend(re.findall(pattern, final_log))
    if code:
        errors = re.findall(r'(?m)^.*(?:Error:|Undefined control sequence|Missing \$|Emergency stop|Fatal error|:[0-9]+:|ENVIRONMENT:|TIMEOUT:|找不到主文件).*$','\n'.join(logs))[:8]
        if not errors:
            errors = ['构建未完成；查看 build-transcript.txt 的最后一个命令输出。']
    return {'compiled': code == 0 and (working / (stem + '.pdf')).is_file(), 'exit_code': code,
            'commands': executed, 'warnings': list(dict.fromkeys(warnings)), 'errors': errors,
            'pdf': str(working / (stem + '.pdf')), 'build_dir': str(output), 'entry': entry,
            'log': str(log), 'transcript': str(transcript), 'blocked_reason': blocked}


def technical_checks(info, project, build, entry='main.tex'):
    """Compatibility API: retains name/pass/detail; adds evidence and status."""
    from selfcheck import evaluate
    return evaluate(info, Path(project), build, entry, ROOT)[0]


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('list')
    sub.add_parser('doctor')
    for cmd in ['start', 'build', 'check', 'pack']:
        q = sub.add_parser(cmd)
        q.add_argument('lab', choices=[str(i).zfill(2) for i in range(8)])
        if cmd != 'start':
            q.add_argument('--project', type=Path, help='现有工程目录；默认使用 work/关卡目录')
        if cmd in ['build', 'check']:
            q.add_argument('--entry', default='main.tex', help='工程内主文件，例如 thesis/main.tex')
    args = parser.parse_args()
    if args.command == 'list':
        for info in course():
            print(info['id'], info['name'])
        return 0
    if args.command == 'doctor':
        for exe in ['xelatex', 'biber', 'bibtex', 'latexmk', 'pdftotext', 'pdfinfo']:
            print(exe, shutil.which(exe) or '未找到')
        print('编辑器任选。自动核验在本机使用 Python 3.9+ 和 TeX；PDF 取证使用 pdftotext/pdfinfo。')
        return 0
    info = labinfo(args.lab)
    project = ROOT / 'work' / info['folder']
    if args.command == 'start':
        if project.exists():
            print('已有工作目录，未覆盖：', project)
            return 1
        shutil.copytree(ROOT / 'labs' / info['folder'] / 'starter', project)
        print('已创建：', project, '\n在所选编辑器中打开 main.tex。')
        return 0
    if args.project:
        project = args.project.resolve()
    if not project.is_dir():
        raise ValueError('请先 start，或用 --project 指向已有工程。')
    stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    if args.command == 'pack':
        dest = ROOT / 'dist' / f"submission-{info['id']}-{stamp}.zip"
        dest.parent.mkdir(exist_ok=True)
        with zipfile.ZipFile(dest, 'w', zipfile.ZIP_DEFLATED) as z:
            for f in source_files(project):
                z.write(f, f.relative_to(project))
        print('源码包：', dest, '\n解压到新目录后再次 check --project，以核对搬家后的构建。')
        return 0
    entry = Path(args.entry)
    if entry.is_absolute() or '..' in entry.parts:
        raise ValueError('entry 必须是工程内的相对文件路径。')
    build = build_project(project, ROOT / '_build' / f"{info['id']}-{stamp}", args.entry)
    from selfcheck import make_report, write_report
    report = make_report(info, project, build, args.entry, ROOT, source_files,
                         run_checks=args.command == 'check')
    write_report(report, ROOT)
    for check in report['checks']:
        print(check['status'].upper(), check['name'])
        if check['status'] != 'pass':
            print('  ' + check['detail'] + '\n  下一步：' + check['next_action'])
    print('状态：', report['status'], '；', report['summary']['message'])
    print('打开报告：', Path(build['build_dir']) / 'check-report.html')
    print('导入手册：', ROOT / 'reports' / ('latest-' + info['id'] + '.json'))
    print('自动核验仅覆盖报告列出的条件；请继续完成报告中的 PDF 自查和变式实验。')
    return 0 if report['status'] == 'passed' else (2 if report['status'] == 'blocked' else 1)


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (ValueError, RuntimeError, OSError, StopIteration) as exc:
        print('ERROR:', exc)
        sys.exit(2)
