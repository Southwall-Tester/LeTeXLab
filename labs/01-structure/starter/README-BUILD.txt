Main document: main.tex
Engine: XeLaTeX. Fonts: Fandol (included in a full TeX Live installation).
Recommended: latexmk -xelatex -interaction=nonstopmode -halt-on-error -file-line-error main.tex
Without latexmk: xelatex main.tex; if using biblatex run biber main; then xelatex main.tex twice.
If using natbib instead, run bibtex main (not biber).
Overleaf: upload this project, select main.tex and XeLaTeX. Recompile; use Recompile from scratch when needed.
This project uses synthetic teaching data, not real research findings.
