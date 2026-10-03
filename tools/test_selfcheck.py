"""Regression tests for truthful status, evidence boundaries and stale results.

Run: python -m unittest discover -s tools -p test_selfcheck.py -v
Real compilation tests skip only when XeLaTeX or pdftotext is unavailable.
"""
from pathlib import Path
import json
import re
import shutil
import tempfile
import unittest
from unittest.mock import patch

import lab
import selfcheck


class SelfcheckTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='latexlab-selfcheck-')
        self.base = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def copy(self, number, kind='solution'):
        info = lab.labinfo(number)
        origin = lab.ROOT / ('instructor/solutions' if kind == 'solution' else 'labs') / info['folder']
        if kind == 'starter':
            origin /= 'starter'
        project = self.base / ('source-' + number)
        lab.copy_sources(origin, project)
        return info, project

    def test_generated_reports_and_caches_do_not_change_fingerprint_or_pack(self):
        _, project = self.copy('00')
        before = selfcheck.fingerprint(project, lab.source_files)
        for name in ['check-report.json', 'check-report.html', 'ai-review-prompt.txt', 'build-transcript.txt',
                     'pdf-text.txt', 'pdf-info.txt', 'main.aux', 'main.pdf', 'biber-cache-isolated/a.txt', 'reports/latest-00.json']:
            path = project / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('generated', encoding='utf-8')
        self.assertEqual(before, selfcheck.fingerprint(project, lab.source_files))

    def test_missing_engine_still_produces_blocked_versioned_report(self):
        info, project = self.copy('00')
        before = selfcheck.fingerprint(project, lab.source_files)
        with patch('lab.shutil.which', return_value=None):
            build = lab.build_project(project, self.base / 'build')
        report = selfcheck.make_report(info, project, build, 'main.tex', lab.ROOT, lab.source_files)
        selfcheck.write_report(report, self.base)
        self.assertEqual('blocked', report['status'])
        self.assertEqual('latexlab.check.v2', report['schema'])
        self.assertEqual('unavailable', report['checks'][0]['status'])
        self.assertTrue((self.base / 'reports/latest-00.json').is_file())
        self.assertTrue((self.base / 'build/check-report.html').is_file())
        self.assertEqual(before, selfcheck.fingerprint(project, lab.source_files))
        self.assertIn('ENVIRONMENT', report['ai_review_prompt'])
        self.assertIsInstance(report['project_fingerprint'], str)
        latest = self.base / 'reports/latest-00.json'
        latest.write_text('existing learner report', encoding='utf-8')
        selfcheck.write_report(report, self.base, update_latest=False)
        self.assertEqual('existing learner report', latest.read_text(encoding='utf-8'))

    def test_compile_failure_never_passes_downstream_evidence_checks(self):
        info, project = self.copy('07', 'starter')
        build = {'compiled': False, 'build_dir': str(self.base / 'build'), 'pdf': str(self.base / 'build/main.pdf'),
                 'exit_code': 1, 'warnings': [], 'errors': ['main.tex:10: Undefined control sequence.'], 'commands': []}
        report = selfcheck.make_report(info, project, build, 'main.tex', lab.ROOT, lab.source_files)
        self.assertEqual('needs_work', report['status'])
        dependent = ['log-clean', 'structure-inputs', 'figure-assets', 'table-values', 'bib-order', 'template-layout']
        checks = {item['id']: item for item in report['checks']}
        for check_id in dependent:
            self.assertEqual('unavailable', checks[check_id]['status'], check_id)
            self.assertFalse(checks[check_id]['pass'])

    def test_metrics_change_with_raw_data(self):
        _, project = self.copy('04')
        path = project / 'data/observations.csv'
        metrics, count = selfcheck.compute_metrics(path)
        self.assertEqual(6, count)
        self.assertEqual(0.5, metrics['Calibrated']['RMSE'])
        path.write_text(path.read_text(encoding='utf-8').replace('1,20,21,20.5', '1,20,21,22'), encoding='utf-8')
        changed, _ = selfcheck.compute_metrics(path)
        self.assertAlmostEqual((5.25/6)**0.5, changed['Calibrated']['RMSE'])
        self.assertEqual(0.75, changed['Calibrated']['MAE'])

    def test_nonfinite_csv_rejected(self):
        path = self.base / 'data.csv'
        path.write_text('truth,baseline,calibrated\n20,nan,20.5\n', encoding='utf-8')
        with self.assertRaises(ValueError):
            selfcheck.compute_metrics(path)

    def test_object_types_do_not_depend_on_reference_solution_keys(self):
        aux = (r'\newlabel{custom-method}{{2}{1}{方法}{section.2}{}}' + '\n' +
               r'\newlabel{my-formula}{{1}{1}{方法}{equation.1}{}}' + '\n' +
               r'\newlabel{plot-first}{{1a}{1}{Baseline}{figure.caption.2}{}}' + '\n' +
               r'\newlabel{sub@plot-first}{{a}{1}{Baseline}{figure.caption.2}{}}')
        objects = selfcheck.compiled_objects(aux, '')
        self.assertEqual('section', objects['custom-method']['role'])
        self.assertEqual('equation', objects['my-formula']['role'])
        self.assertEqual('subfigure', objects['plot-first']['role'])
        plain = selfcheck.compiled_objects(r'\newlabel{custom-table}{{1}{1}}', r'\begin {table}\caption{结果}\label{custom-table}\end {table}')
        self.assertEqual('table', plain['custom-table']['role'])

    @unittest.skipUnless(shutil.which('xelatex') and shutil.which('pdftotext'), 'TeX/PDF toolchain unavailable')
    def test_check_scope_distinguishes_lab_build_and_side_entry(self):
        info, project = self.copy('00')
        build = lab.build_project(project, self.base / 'main-build')
        full = selfcheck.make_report(info, project, build, 'main.tex', lab.ROOT, lab.source_files)
        compile_only = selfcheck.make_report(info, project, build, 'main.tex', lab.ROOT, lab.source_files, run_checks=False)
        self.assertEqual(('lab', 'passed'), (full['check_scope'], full['status']))
        self.assertEqual(('build', 'passed'), (compile_only['check_scope'], compile_only['status']))
        self.assertEqual(['build', 'log-clean'], [x['id'] for x in compile_only['checks']])
        (project / 'side').mkdir()
        shutil.copy2(project / 'main.tex', project / 'side/main.tex')
        side_build = lab.build_project(project, self.base / 'side-build', 'side/main.tex')
        side = selfcheck.make_report(info, project, side_build, 'side/main.tex', lab.ROOT, lab.source_files)
        self.assertEqual(('build', 'passed'), (side['check_scope'], side['status']))
        self.assertEqual('side/main.tex', side['entry'])
        self.assertEqual(['build', 'log-clean'], [x['id'] for x in side['checks']])

    @unittest.skipUnless(shutil.which('xelatex') and shutil.which('pdftotext'), 'TeX/PDF toolchain unavailable')
    def test_lab01_custom_labels_need_not_be_referenced(self):
        info, project = self.copy('01')
        for path in project.rglob('*.tex'):
            text = path.read_text(encoding='utf-8')
            text = text.replace('sec:intro', 'opening').replace('sec:method', 'approach').replace('sec:results', 'observations')
            text = text.replace(r'方法见第~\ref{approach} 节，结果与局限见第~\ref{observations} 节。', '')
            path.write_text(text, encoding='utf-8')
        build = lab.build_project(project, self.base / 'build')
        report = selfcheck.make_report(info, project, build, 'main.tex', lab.ROOT, lab.source_files)
        self.assertEqual('passed', report['status'], [x for x in report['checks'] if not x['pass']])
        self.assertNotIn('structure-references', {x['id'] for x in report['checks']})

    @unittest.skipUnless(all(shutil.which(exe) for exe in ['xelatex', 'pdftotext', 'pdfinfo', 'biber']), 'TeX/PDF toolchain unavailable')
    def test_submission_accepts_renamed_keys_files_and_equivalent_review_option(self):
        info, project = self.copy('07')
        changes = {'sections/intro': 'sections/background', 'sections/method': 'sections/procedure',
                   'sections/results': 'sections/findings', 'baseline.pdf': 'raw.pdf', 'calibrated.pdf': 'corrected.pdf'}
        for path in project.rglob('*.tex'):
            text = path.read_text(encoding='utf-8')
            text = re.sub(r'\b(sec|fig|eq|tab):([a-z]+)', r'object-\1-\2', text)
            for old, new in changes.items():
                text = text.replace(old, new)
            text = text.replace(r'\documentclass[review]{labpaper}', r'\PassOptionsToClass{review}{labpaper}' + '\n' + r'\documentclass{labpaper}')
            path.write_text(text, encoding='utf-8')
        for old, new in [('intro', 'background'), ('method', 'procedure'), ('results', 'findings')]:
            (project / 'sections' / (old + '.tex')).rename(project / 'sections' / (new + '.tex'))
        for old, new in [('baseline', 'raw'), ('calibrated', 'corrected')]:
            (project / 'figures' / (old + '.pdf')).rename(project / 'figures' / (new + '.pdf'))
        build = lab.build_project(project, self.base / 'build')
        report = selfcheck.make_report(info, project, build, 'main.tex', lab.ROOT, lab.source_files)
        self.assertEqual('passed', report['status'], [x for x in report['checks'] if not x['pass']])
        self.assertIn('object-eq-rmse', next(x for x in report['checks'] if x['id'] == 'math-reference')['evidence'])

    @unittest.skipUnless(shutil.which('xelatex') and shutil.which('pdftotext'), 'TeX/PDF toolchain unavailable')
    def test_real_wrong_table_is_detected(self):
        info, project = self.copy('04')
        main = project / 'main.tex'
        main.write_text(main.read_text(encoding='utf-8').replace('Baseline & 1.000 & 1.000', 'Baseline & 9.999 & 1.000'), encoding='utf-8')
        build = lab.build_project(project, self.base / 'build')
        self.assertTrue(build['compiled'])
        # Editing the original after compilation must not alter this snapshot's
        # evidence or make the incorrect rendered table match changed data.
        (project / 'data/observations.csv').write_text('invalid changed source', encoding='utf-8')
        checks = {x['id']: x for x in lab.technical_checks(info, project, build)}
        self.assertEqual('fail', checks['table-values']['status'])
        self.assertIn('9.999', checks['table-values']['evidence'])
        self.assertEqual('pass', checks['data-metrics']['status'])

    @unittest.skipUnless(shutil.which('xelatex') and shutil.which('pdftotext'), 'TeX/PDF toolchain unavailable')
    def test_compilable_wrong_formula_does_not_claim_semantic_verification(self):
        info, project = self.copy('04')
        main = project / 'main.tex'
        main.write_text(main.read_text(encoding='utf-8').replace(r'\sqrt{\frac{1}{n}\sum_{i=1}^{n}(\hat y_i-y_i)^2}', '123'), encoding='utf-8')
        build = lab.build_project(project, self.base / 'build')
        report = selfcheck.make_report(info, project, build, 'main.tex', lab.ROOT, lab.source_files)
        self.assertTrue(build['compiled'])
        self.assertEqual('passed', report['status'], [x for x in report['checks'] if not x['pass']])
        self.assertTrue(any('不证明公式写对' in step for step in report['self_review']))
        self.assertTrue(any('公式语义' in line for line in report['limitations']))
        self.assertFalse(any('公式正确' in x['name'] or '语义正确' in x['name'] for x in report['checks']))

    @unittest.skipUnless(shutil.which('xelatex'), 'TeX toolchain unavailable')
    def test_missing_pdf_extractor_cannot_be_treated_as_pass(self):
        info, project = self.copy('00')
        build = lab.build_project(project, self.base / 'build')
        real_which = shutil.which
        with patch('selfcheck.shutil.which', side_effect=lambda exe: None if exe == 'pdftotext' else real_which(exe)):
            report = selfcheck.make_report(info, project, build, 'main.tex', lab.ROOT, lab.source_files)
        self.assertEqual('blocked', report['status'])
        check = next(x for x in report['checks'] if x['id'] == 'boot-output')
        self.assertEqual('unavailable', check['status'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
