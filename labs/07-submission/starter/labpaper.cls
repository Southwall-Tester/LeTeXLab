% LaTeXLab teaching class v2.0; not a university or journal template.
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{labpaper}[2026/10/03 v2.0 Teaching paper]
\newif\iflabreview
\labreviewfalse
\DeclareOption{review}{\labreviewtrue}
\DeclareOption{final}{\labreviewfalse}
\DeclareOption*{\ClassError{labpaper}{Unknown option \CurrentOption}{Use review or final.}}
\ProcessOptions\relax
\LoadClass[UTF8,fontset=fandol,a4paper,10pt,twocolumn]{ctexart}
\RequirePackage[margin=20mm]{geometry}
\RequirePackage{fancyhdr}
\pagestyle{fancy}\fancyhf{}\fancyfoot[C]{\thepage}
\setlength{\headheight}{15pt}
\renewcommand{\headrulewidth}{0pt}
\AtBeginDocument{\iflabreview\author{匿名作者}\fi}
