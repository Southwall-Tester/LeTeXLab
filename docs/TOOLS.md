# 工具选择与结果核验

编辑器负责写文件和发起构建；TeX Live / MacTeX / MiKTeX 提供引擎与宏包；XeLaTeX 读取源码排版；Biber 或 BibTeX 处理文献；latexmk 决定要跑哪些程序、跑几轮。

本练习选 **XeLaTeX + Fandol** 作为可移植基线，使用 biblatex 的项目配 Biber。你可以用任何能运行同等编译链的工具，不要求换掉现有 VS Code。

本地检查器用 Python 标准库协调构建，并用 `pdftotext`、`pdfinfo` 读取本次 PDF 的文字和元数据。运行 `python tools/lab.py doctor` 查看工具是否可用；缺少取证程序时，相关检查显示 `unavailable`，不会因为已有 PDF 就认定通过。

## VS Code

安装 TeX 发行版和 LaTeX Workshop，打开某一关的工作目录，而不是把所有关卡当成一篇论文。工程内 `.vscode/settings.json` 提供手动构建配方，避免保存时无意触发多个关卡编译。命令面板查找 `LaTeX Workshop: Build with recipe`，选择本工程配方。打开内置 PDF 阅读器，使用其 SyncTeX 跳转功能核对源码与输出。具体快捷键可随平台与用户键位变化。

若报 `spawn ... ENOENT`，检查程序是否安装和 PATH；若能启动但报 `.sty not found`，根据缺失的宏包补齐 TeX 环境。不要把两者都当编辑器错误。

## TeXstudio

打开工程的 main.tex。默认编译器选 XeLaTeX；主项目为 biblatex 时运行 Biber。使用软件的构建菜单或内置终端完成以下顺序，重复点击单次 XeLaTeX 不能替代 Biber。不同版本菜单名称可能不同，以显示的实际命令为准。

## Overleaf / 其他在线平台

上传 `downloads/关卡.zip`，保留原目录，主文件设为 main.tex，选择 XeLaTeX。平台通常使用 latexmk 管理文献与重复编译。查看日志而不是只看预览是否有 PDF；必要时从头重新编译。练习 thesis/main.tex 或 legacy/main.tex 时临时切换主文件，完成后切回 main.tex。

在线平台完成修改后，下载当前源码、PDF 与日志。有本地 TeX 时解压工程并运行 `check --project`；没有时使用手册的本关 AI 核验请求，把结论与证据记为 AI 辅助核对，再做理解题与 PDF 自查。两条路线见 `docs/SELF-STUDY.md`。

## 通用命令

在含 main.tex 的工程目录运行：

```text
latexmk -xelatex -interaction=nonstopmode -halt-on-error -file-line-error main.tex
```

不使用 latexmk 时，含 biblatex 的工程依次运行：

```text
xelatex -interaction=nonstopmode -halt-on-error -file-line-error main.tex
biber main
xelatex -interaction=nonstopmode -halt-on-error -file-line-error main.tex
xelatex -interaction=nonstopmode -halt-on-error -file-line-error main.tex
```

不含参考文献时不跑 Biber，XeLaTeX 至引用稳定即可。Lab 05 的 legacy 工程改用 `bibtex main`。遇到模板时以其文档要求为准，不机械套用本课程配方。

## 保存工程与干净重建

```text
python tools/lab.py pack 07
```

把生成的源码 zip 解压到新目录，然后 `python tools/lab.py check 07 --project "解压后的目录"`。pack 有意不打包构建生成的正文 PDF；将最终 PDF 单独保留。图形素材 PDF 会保留。

检查器在 `_build/关卡-时间/` 复制源码后构建，保留原工作区。失败后的旧 PDF 不作为通过证据。清理时只删自己确认属于构建产物的文件，不盲删 `.tex`、`.bib`、图片或类文件。

`build` 与支线入口也会写报告并更新 `reports/latest-XX.json`。主关进度只采用 `check_scope='lab'` 的完整核验报告；支线练习后重新运行主入口 `python tools/lab.py check XX`，再将新报告导入手册。每次构建目录中的 `ai-review-prompt.txt` 可用于请求智能体解释已有证据，其中的截取内容不能替代完整源码、日志或 PDF。

参考：[LaTeX Workshop 构建文档](https://github.com/James-Yu/LaTeX-Workshop/wiki/Compile)、[TeX Live](https://tug.org/texlive/)、[Overleaf 的 biblatex 说明](https://www.overleaf.com/learn/latex/Bibliography_management_with_biblatex)。
