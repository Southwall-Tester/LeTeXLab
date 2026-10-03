"""Authoring source for the offline LaTeXLab course. Run from the repository root."""
from pathlib import Path
import json, shutil, csv, html, zipfile

ROOT = Path(__file__).resolve().parents[1]
def put(path, text):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text.strip() + '\n', encoding='utf-8')

PRE = r'''% !TeX program = xelatex
\documentclass[UTF8,fontset=fandol,a4paper,11pt]{ctexart}
\usepackage[margin=25mm]{geometry}
\usepackage{amsmath,amssymb,amsthm,graphicx,booktabs,array,tabularx,subcaption}
\usepackage[hidelinks]{hyperref}
\graphicspath{{figures/}}
'''
BIBPRE = r'''\usepackage[backend=biber,style=numeric,sorting=none]{biblatex}
\addbibresource{references.bib}
'''
BIB = r'''@article{einstein1905,
  author = {Einstein, Albert},
  title = {Zur Elektrodynamik bewegter Körper},
  journaltitle = {Annalen der Physik},
  year = {1905}, volume = {322}, number = {10}, pages = {891--921},
  doi = {10.1002/andp.19053221004}
}
@book{knuth1984,
  author = {Knuth, Donald E.}, title = {The {TeXbook}},
  year = {1984}, publisher = {Addison-Wesley}
}
'''
INCOMING = r'''@book{lamport1994,
  author = {Lamport, Leslie},
  title = {{LaTeX}: A Document Preparation System},
  edition = {2}, year = {1994}, publisher = {Addison-Wesley}
}
'''
INTRO = r'''% !TeX root = ../main.tex
\section{引言}\label{sec:intro}
本项目比较两种室内温度校正方案。所有数据均为教学合成数据，
只用于练习论文排版，不能据此声称算法具有实际科研效果。
\emph{可复现的排版}要求正文、数据与引用能够一起交付。
数据版本为 \texttt{sensor\_v2}，抽查比例为 20\%。
\footnote{本实验不收集真实受试者数据。}
方法见第~\ref{sec:method} 节，结果与局限见第~\ref{sec:results} 节。
\subsection{研究问题}
比较 Baseline 和 Calibrated 在六个时刻的误差。
\begin{itemize}
  \item 保留原始观测；
  \item 图、表和正文使用同一组数据。
\end{itemize}
\begin{enumerate}
  \item 读取数据；\item 计算误差；\item 复核结果。
\end{enumerate}
\begin{description}
  \item[真实值] 本教学数据中给定的参照温度。
  \item[预测值] 两种方法给出的温度。
\end{description}
'''
METHOD = r'''% !TeX root = ../main.tex
\section{方法}\label{sec:method}
令 $y_i$ 为真实值，$\hat y_i$ 为预测值，样本数 $n=6$。
采用式~\eqref{eq:rmse} 的均方根误差，单位与温度相同。
\begin{equation}
 \operatorname{RMSE}=\sqrt{\frac{1}{n}\sum_{i=1}^{n}(\hat y_i-y_i)^2}.
 \label{eq:rmse}
\end{equation}
\begin{align}
 e_i &= \hat y_i-y_i,\label{eq:error}\\
 \operatorname{MSE} &= \frac{1}{n}\sum_{i=1}^{n}e_i^2.\label{eq:mse}
\end{align}
平均绝对误差为 $\operatorname{MAE}=\frac{1}{n}\sum_{i=1}^{n}|e_i|$，
它与 RMSE 一般不同；本组样本中两者恰好相等。
用分段函数标记是否超过容差：
\begin{equation*}
 q_i=\begin{cases}1,&|e_i|\leq 0.5,\\0,&|e_i|>0.5.\end{cases}
\end{equation*}
两个误差样本组成列向量 $\boldsymbol e=\begin{pmatrix}e_1\\e_2\end{pmatrix}$。
'''
FIGURE = r'''\begin{figure}[htbp]
 \centering
 \begin{subfigure}{0.48\linewidth}
  \centering\includegraphics[width=\linewidth]{baseline.pdf}
  \caption{Baseline}\label{fig:baseline}
 \end{subfigure}\hfill
 \begin{subfigure}{0.48\linewidth}
  \centering\includegraphics[width=\linewidth]{calibrated.pdf}
  \caption{Calibrated}\label{fig:calibrated}
 \end{subfigure}
 \caption{两种方法的误差对比（教学合成数据）。}\label{fig:comparison}
\end{figure}
'''
TABLE = r'''\begin{table}[htbp]
 \centering
 \caption{温度误差汇总（教学合成数据）。}\label{tab:metrics}
 \begin{tabular}{lrr}
  \toprule
  \multicolumn{1}{c}{方法} & \multicolumn{2}{c}{误差（$^\circ$C）}\\
  \cmidrule(lr){2-3}
   & RMSE & MAE\\
  \midrule
  Baseline & 1.000 & 1.000\\
  Calibrated & 0.500 & 0.500\\
  \bottomrule
 \end{tabular}
\end{table}
'''
RESULT = r'''% !TeX root = ../main.tex
\section{结果与局限}\label{sec:results}
图~\ref{fig:comparison} 的子图~\ref{fig:baseline} 和~\ref{fig:calibrated}
分别展示两种方法；表~\ref{tab:metrics} 给出汇总。
Calibrated 的 RMSE 为 $0.500\,{}^\circ\mathrm{C}$，
比 Baseline 的 $1.000\,{}^\circ\mathrm{C}$ 低 50\%。
这一比较仅对当前六条合成样本成立，不代表真实环境中的泛化效果。
''' + FIGURE + TABLE

CLASS = r'''% LaTeXLab teaching class v2.0; not a university or journal template.
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
'''
TEMPLATE_PRE = r'''% !TeX program = xelatex
\documentclass[review]{labpaper}
\usepackage{amsmath,amssymb,amsthm,graphicx,booktabs,array,tabularx,subcaption}
\usepackage[hidelinks]{hyperref}
\graphicspath{{figures/}}
'''
THESIS = r'''% !TeX program = xelatex
% Portable practice of book structure; not SJTUThesis.
\documentclass[UTF8,fontset=fandol,openany]{ctexbook}
\usepackage{amsmath,amsthm,graphicx}
\usepackage[hidelinks]{hyperref}
\newtheorem{theorem}{定理}[chapter]
\title{温度校正排版练习}\author{实验者}\date{}
\begin{document}
\frontmatter
\maketitle
\chapter{摘要}这里是中文摘要。\chapter{Abstract}This is a typesetting exercise.
\tableofcontents\listoffigures\listoftables
\mainmatter
\chapter{方法}\label{chap:method}
\begin{theorem}若所有预测值等于真实值，则 RMSE 为零。\end{theorem}
\begin{proof}各平方误差均为零，代入定义即可。\end{proof}
\appendix
\chapter{数据说明}全部观测均为教学合成数据。
\backmatter
\chapter{致谢}感谢教学材料作者。
\end{document}
'''

LABS = [
dict(id='00',slug='boot',name='Boot Lab · 接管工程',
story='周一 09:00。师兄发来一个论文工程，只说“在我电脑上能跑”。你需要证明自己的环境能编译，并找到正文和 PDF 的对应关系。',
tasks=[r'复制 starter 后打开 main.tex。先原样编译，再把标题改为“温度校正研究：工程接管”，作者改成自己的署名。保留中英文测试段落。',r'在自己的笔记中记录编辑器、TeX 发行版、实际引擎及版本、主文件、编译动作、PDF 路径。区分编辑器、发行版、XeLaTeX、latexmk 四个角色。',r'在 PDF 找到“接管标记”，回到对应源码改为“接管完成”，重新编译核对。尝试编辑器的 SyncTeX 正反向跳转，记录实际入口；平台不支持时用搜索定位并注明。',r'指出导言区、宏包、正文环境、注释以及 .tex / .pdf / .log / .aux 的用途。在日志中找到实际引擎名称。'],
accept=['中文与英文均显示，标题和署名已改变，正文出现“接管完成”。','能分清工具角色；能从输出定位源码，主文件选择正确。'],
probe='把一个正文短语改成英文再编译；说明为什么换编辑器不等于换编译引擎。',
hints=['打开 main.tex；正文起点是 begin{document}。','标题信息在导言区，maketitle 决定其输出位置。中文练习采用 XeLaTeX 与 Fandol 字体。','若命令不存在，检查 TeX 发行版和 PATH；若已找到引擎但缺包，依据首个错误补齐依赖。不要仅重装编辑器。'],
files=['main.tex'],source='intro.tex · install.tex · minimal.tex'),
dict(id='01',slug='structure',name='Structure Lab · 整理师兄的草稿',
story='导师要看论文结构，但草稿用加粗文字冒充标题，摘要混在正文里，所有内容塞在 main.tex。你需要把它整理成可维护的工程。',
tasks=[r'将草稿整理成标题、摘要、目录、引言、方法、结果与局限。用 section / subsection 表示层级，并给三个主要章节稳定标签。目录只显示到 subsection。',r'将三个章节拆到 sections/intro.tex、sections/method.tex、sections/results.tex，通过 input 接入。子文件不能再有 documentclass 或 document 环境。添加指向 ../main.tex 的根文件注释。',r'加入无序列表、有序列表和术语描述列表各一处。使用 emph 或 textbf 标记一个概念，用局部分组限制 small 的作用范围，并给数据来源加脚注。',r'让 sensor_v2、20%、A&B 三段文字在 PDF 中正确显示。不要直接插入未转义的特殊字符。',r'将方法和结果两节交换顺序，观察自动编号和目录，再恢复。另在副本中把 input 换为 include，记录分页变化。'],
accept=['目录对应真实章节；三份子文件由唯一主文档调用。','字号改变不泄漏到后文，三个列表与特殊字符正确显示。','章节重排无需手改编号；用副本观察并解释 input 和 include 的分页差别。'],
probe='新增一个“误差定义”小节并让目录自动更新，说明星号标题与普通标题的差别。',
hints=['先用注释画出导言区与正文边界，再拆文件。','空行代表分段；连续空格不能可靠地排版对齐；字号声明放在一对大括号内。','目录需要多轮编译。article 系列没有 chapter；短论文用 section，学位论文章结构见 Lab 06。'],
files=['main.tex','sections/*.tex'],source='text-style.tex · structure.tex'),
dict(id='02',slug='rescue',name='Rescue Lab · 拆掉六个编译炸弹',
story='合作者合并了一段智能体生成的代码，论文突然无法编译。截止前你要找到首个根因，逐个修复，并保留每次诊断证据。',
tasks=[r'对 starter 做第一次真实编译。不要先查看参考解。在自己的笔记中为每次修复记录：首个有效错误或警告、文件与行、判断、最小修改、重编译结果。',r'工程内有六类问题：命令拼写、宏包依赖、特殊字符、环境闭合、交叉引用、版心溢出。按实际日志出现的顺序处理；后续错误可能是前一个错误的连锁反应。',r'保留题目中的全部信息、表格和数据。不能删除报错段、关掉警告、改成图片或硬写编号来过关。将 label 放在产生相应编号的位置之后。',r'最后进行一次干净构建，检查 PDF、日志和引用。区分 error、undefined reference 与 Overfull hbox 的后果。'],
accept=['六类问题都已修复，原有内容保留，交叉引用可随编号变化。','最终日志无未定义引用、致命错误或本题制造的溢出。','用六类问题的修复证据核对结果，能说明为何先看首个错误。'],
probe='在副本中将一个 ref 的键拼错，预测结果，再编译验证并恢复。',
hints=['从日志首个指向源码的错误开始；Emergency stop 常常不是根因。','命令名区分拼写；toprule 由 booktabs 提供；正文中的 & 与 tabular 内的 & 意义不同。','检查 sectoin、booktabs、A&B、itemize 的结束环境、tab:result / tab:results 和 1.35 倍版心的固定横线。每次只修一个根因。'],
files=['main.tex'],source='sjtuthesis.tex「编译问题排查」· reference.tex'),
dict(id='03',slug='figures',name='Figure Lab · 审稿人看不清你的图',
story='审稿意见：“两张图无法比较，图题缺失，正文只说见下图。换成双栏后更是溢出版心。”图已经由组内脚本生成，你负责可靠地排进去。',
tasks=[r'用 figures/baseline.pdf 和 calibrated.pdf 替换占位图。采用相对路径或 graphicspath；不要使用自己的桌面绝对路径。',r'把两图排为一张总图下的 (a)(b) 两个子图，各约 0.48 倍当前 linewidth，保留纵横比。加入子图题、总图题、稳定标签，并在正文引用总图及两个子图。',r'总图说明“教学合成数据”。图在正文首次提及附近浮动，理解 [htbp] 是位置偏好。对比 h 与 H：H 需要 float 宏包，可能造成空白，不能把它当普遍修复。',r'在副本中将 documentclass 加 twocolumn，确认当前栏内图片不溢出；解释嵌套 minipage 中 linewidth 和 textwidth 的差别。',r'再在副本中把 subfigure 换为两个 minipage，各自 caption，观察“一个图的两个子图”和“两张独立编号的图”的区别，保留对比 PDF 或截图。'],
accept=['两幅真实素材均出现，比例不变，标签在 caption 后，正文使用 ref。','单栏和双栏试验都无图片越界；文件夹搬家后仍可编译。','通过副本变化解释浮动体、相对尺寸和两种并排编号方式。'],
probe='交换两子图顺序，并把每幅宽度调为 0.44 倍 linewidth；引用仍应跟随对象。',
hints=['先插入一张图并成功编译，再建立子图结构。','graphicx 负责插图，subcaption 提供 subfigure；每个子图内部用 width=linewidth。','总标签放在总 caption 之后；子标签放在各自 caption 之后。不要用图 1(a) 这样的正文常量。'],
files=['main.tex','figures/*.pdf'],source='figure.tex · reference.tex'),
dict(id='04',slug='results',name='Results Lab · 让公式和表格对得上',
story='智能体生成的公式能编译，但计算的其实不是 RMSE；表里还抄错了一个结果。你需要核对含义，再按论文规范排版。',
tasks=[r'阅读 data/observations.csv。修正 RMSE 为平方误差均值再开平方；写清 n、真实值、预测值与单位。独立计算两方法的 RMSE 和 MAE，保留三位小数。',r'使用带编号 equation 并由 eqref 引用；用 align 排两行误差定义，增加一个无编号分段函数及一个矩阵。禁止用图片替代数学公式。',r'将 data/summary.csv 导入 Tables Generator 或用智能体生成表格草稿，再核对原始数据。用 booktabs 三线表、合并表头、caption 和 label；无竖线，数字右对齐。表上方标题、正文动态引用。',r'表格结果应与原始数据一致。把“降低 50%”限制为本教学样本上的观察，不推断真实有效性。',r'在 scratch.tex 副本中试一次固定宽度 p 列、multicolumn 表头以及 gather / multline。读扩展卡选择 longtable 或 threeparttable 处理给定场景。'],
accept=['RMSE 公式含平方、均值与平方根，MAE 含绝对值；两方法结果分别为 1.000 / 0.500。','表中名称、单位、列数与 CSV 一致，数字未被生成工具改写。','公式和表格均可引用；对齐与多行环境使用正确。'],
probe='仅在数据副本中将 Calibrated 第一个预测值改为 22，重新算指标并更新表；说明只改 LaTeX 公式为何不会自动重算静态表。',
hints=['本题合成数据的 Baseline 误差绝对值均为 1，Calibrated 均为 0.5。','amsmath 提供 align、cases、pmatrix 和 eqref；不要把 align 套进 equation。','三列每个普通数据行应有两个 &。检查平方根包住的范围，不能以编译成功判断数学正确。'],
files=['main.tex','data/*.csv'],source='math.tex · table.tex'),
dict(id='05',slug='citations',name='Citation Lab · 文献编号大洗牌',
story='本次修改需要让编号按首次引用顺序出现，并补入一篇参考资料。你收到文献管理器导出的 .bib，却发现 [1] 不对应自己预期的那篇。',
tasks=[r'阅读 references.bib 和 incoming.bib 的主键及字段。将 incoming.bib 的 lamport1994 合并到 references.bib，保留另两条记录；不手写正文参考文献列表。',r'按正文首次引用顺序引用 lamport1994、knuth1984、einstein1905。设 biblatex 的 backend=biber、style=numeric、sorting=none，输出参考文献表。',r'完整运行 XeLaTeX → Biber → XeLaTeX → XeLaTeX，或用 latexmk。说明 .bib、.bcf、.bbl、.aux 分别处在哪条链路。找出最初 undefined citation 的原因。',r'交换正文前两处引用，重编译并记录 [1] 对象如何变化。不要靠修改 .bib 条目排列或手写 [1] 调编号。',r'在副本中改用 authoryear 并比较显示；再编译 legacy/main.tex，识别 natbib + BibTeX 的另一套链路。不要在同一主文件同时加载 natbib 和 biblatex。'],
accept=['三条文献都有合法主键且显示在文献表，无未定义引用。','主交付为数字引用且首次出现的 Lamport 对应 [1]；顺序变化有记录。','能指出不同模板的后端与样式入口；检查原始来源而非相信智能体编造条目。'],
probe='把正文主键临时改错一个字母，区分缺条目、漏跑 Biber 与旧中间文件，再恢复。',
hints=['cite 的参数是 .bib 第一行的主键，不是标题、文件名或显示编号。','sorting=none 按引用顺序；style 控制展示。Biber 读 .bcf，BibTeX 读 .aux。','导入并不会自动引用全部文献；只有被引用的通常才输出。真实项目用 Zotero/JabRef/出版商导出，并对照来源核验元数据。'],
files=['main.tex','references.bib','incoming.bib','legacy/main.tex'],source='reference.tex · sjtuthesis.tex「参考文献」'),
dict(id='06',slug='template',name='Template Lab · 换模板，不拆房子',
story='编辑部退回了格式检查：必须使用提供的双栏匿名模板。与此同时，实验室让你理解学位论文的前置、正文与后置部分，避免照搬三年前视频里的旧选项。',
tasks=[r'先读 TEMPLATE.md 和 MIGRATION.md。把主文档从 ctexart 迁移到随附 labpaper v2，启用 review。不要修改 .cls，不要叠加 geometry 改回旧边距。',r'迁移正文、图、表、公式、参考文献到新模板，保留相对路径和标签。双栏中优先用 linewidth 控制图宽，宽表可调整结构或合理使用跨栏浮动体。',r'检查 PDF 的 A4、20 mm 边距、双栏、匿名作者、页码，以及 PDF 元数据中是否还留下真实姓名。说明哪些参数由模板管理。',r'编译 thesis/main.tex。实际修改中文摘要与英文摘要，把定理标题改成“零误差性质”，补一个附录说明。辨认 frontmatter/mainmatter/appendix/backmatter、chapter、目录与图表目录。',r'阅读 docs/TEMPLATE-TRANSFER.md 的讲稿映射和迁移卡。填写官方 SJTUThesis 的文档类选项、sjtusetup、字体、数学样式、版权页、文献入口位置；区分 2023 讲稿示例和当前安装版。遇到旧选项先查同版本手册。'],
accept=['主文档通过教学模板的 review 模式，.cls 保持原样；图表没有挤出栏宽。','thesis 副本可编译，新增定理名称与附录可见，说明前后页码和章节编号。','迁移记录含旧接口与新入口；明确教学模板不是学校正式模板。'],
probe='在副本切换 review → final，观察作者字段；再切回 review，解释为何不直接改 cls。',
hints=['先让模板的最小文档编译，再迁移内容，最后逐个恢复宏包。','模板已载入 geometry；重复指定不同选项可能导致 Option clash。','匿名是内容审查任务，不仅是隐藏 author：致谢、项目名、PDF 元数据也可能泄露身份。当前练习只用虚构材料。'],
files=['main.tex','labpaper.cls','TEMPLATE.md','MIGRATION.md','thesis/main.tex'],source='sjtuthesis.tex · newversion.tex'),
dict(id='07',slug='submission',name='Submission Lab · 今晚交稿',
story='今天 20:00 截稿。你拿到一份可编译但不合格的合并稿，需要落实审稿意见，并让同事在另一台机器上得到同样的 PDF。',
tasks=[r'从本关 starter 或自己的 Lab 06 结果开始。逐项落实 REVIEW.md：整理真实章节、修公式、补双子图、改三线表、导入三条文献、开启匿名模板。',r'保留 sections/ 下独立章节；在正文动态引用公式、图、表及章节。删除过度科研结论，声明教学合成数据。在自己的记录中区分智能体/生成器产出与已经核对的部分。',r'使用干净构建检查首个错误、引用、文献、浮动体、越界、中文缺字和残留 TODO。打开最终 PDF，逐页检查而非只看构建状态。',r'整理源码包：main.tex、sections、figures、data、references.bib、labpaper.cls、README-BUILD.txt、REPORT.md。用 pack 命令或手动压缩，将源码包与最终 PDF 一起保留。',r'把包解压到一个新目录，从 main.tex 重新编译，记录环境和结果。执行本关变式测试，保存变式前后证据，再恢复最终版。'],
accept=['最终 PDF 包含摘要、引言、方法、结果与局限、正确公式、双子图、三线表、三条文献。','全部交叉引用和文献引用已解析，无报错和任务造成的越界。','解压后的源码不依赖原路径，能够重新构建；保留本次核验报告和自己的 PDF 自查记录。'],
probe='审稿人临时要求交换结果与方法、先引用 Einstein、把双子图改成独立编号。完成变式，展示编号自动变化，然后恢复投稿要求。',
hints=['把审稿意见变成可观察输出，按“能编译→内容正确→格式正确→可移交”的顺序处理。','不要逐处修正文中的“图 1”；改用 label/ref 让重排自然更新。','check 只能证明部分技术条件，不会替你判断公式含义、版式美观、匿名完整性或科研结论。'],
files=['main.tex','sections/*.tex','figures/*.pdf','references.bib','REVIEW.md'],source='综合自测 · 五项学习能力要求')
]

def project(base, files):
    for path, text in files.items(): put(f'{base}/{path}', text)
    put(f'{base}/README-BUILD.txt', '''Main document: main.tex
Engine: XeLaTeX. Fonts: Fandol (included in a full TeX Live installation).
Recommended: latexmk -xelatex -interaction=nonstopmode -halt-on-error -file-line-error main.tex
Without latexmk: xelatex main.tex; if using biblatex run biber main; then xelatex main.tex twice.
If using natbib instead, run bibtex main (not biber).
Overleaf: upload this project, select main.tex and XeLaTeX. Recompile; use Recompile from scratch when needed.
This project uses synthetic teaching data, not real research findings.
''')
    put(f'{base}/.latexmkrc', "$pdf_mode = 5;\n$xelatex = 'xelatex -no-shell-escape -synctex=1 -interaction=nonstopmode -file-line-error %O %S';")
    put(f'{base}/.vscode/settings.json', json.dumps({
        'latex-workshop.latex.recipes':[{'name':'LaTeXLab · XeLaTeX + bibliography','tools':['latexlab']}],
        'latex-workshop.latex.tools':[{'name':'latexlab','command':'latexmk','args':['-xelatex','-synctex=1','-interaction=nonstopmode','-file-line-error','-halt-on-error','-no-shell-escape','%DOC%']}],
        'latex-workshop.latex.autoBuild.run':'never','latex-workshop.view.pdf.viewer':'tab'},ensure_ascii=False,indent=2))

def doc(body, title='室内温度校正：排版练习', pre=PRE):
    return pre + '\\title{'+title+'}\n\\author{研究助理}\n\\date{}\n\\begin{document}\n\\maketitle\n'+body+'\n\\end{document}\n'

def main():
    for lab in LABS:
        lab['folder'] = f"{lab['id']}-{lab['slug']}"
        base=f"labs/{lab['folder']}"
        put(base+'/REPORT.md', '''# 自学记录（可选）

这份记录留给自己，便于回看修改与证据，无需提交给其他人。也可以使用自己的笔记工具。

- 环境 / 编辑器 / 引擎版本：
- 主文档与编译命令或菜单：
- 使用的智能体或生成器（不用则留空）：

## 修改与诊断
文件与位置 / 预期变化 / 首个有效错误或警告 / 最小修改 / 本次构建结果。

## 核验记录
本次报告路径或时间 / fail 与 unavailable 项 / 后续处理。
若用 AI 辅助：实际提供的文件 / 模型引用的具体证据 / 自己复查的结果 / 仍缺的信息。

## 理解自测
页面题目中不确定的地方 / 对应源码 / 试改后观察。

## 变式操作
先写预测，再在副本修改，记录实际变化，最后恢复自己的最终版本。

## PDF 自查
实际打开的 PDF / 检查页码与对象 / 图表、引用、字体与越界问题 / 尚未确认事项。

自动报告、AI 解释、理解题和 PDF 自查分别提供不同信息，不等于学习效果证明。
''')
        text=f"# {lab['name']}\n\n## 情景\n\n{lab['story']}\n\n## 启动\n\n在项目根目录运行 `python tools/lab.py start {lab['id']}`，或手动复制本关 `starter` 文件夹和 `REPORT.md` 到自己的工作目录。打开复制品中的 `main.tex`。每关独立可做，不会因上一关卡住而无法开始。\n\n## 任务\n\n"
        text+='\n\n'.join(f'{i+1}. {x}' for i,x in enumerate(lab['tasks']))
        text+='\n\n## 结果对照\n\n将源码、最终 PDF 和核验报告留给自己。REPORT.md 是可选笔记；下面这些结果可结合自动报告、理解题与 PDF 自查逐项核对。\n\n'+'\n'.join('- '+x for x in lab['accept'])
        text+=f"\n\n## 技术检查\n\n`python tools/lab.py check {lab['id']}`\n\n检查器在 `_build/` 的副本中真实构建，生成 `check-report.json`、`check-report.html` 与日志，并更新 `reports/latest-{lab['id']}.json`。把 JSON 导入离线手册查看具体的 pass / fail / unavailable 项，再完成该关理解题和 PDF 自查。没有本地环境时，下载在线平台的当前源码、PDF 和日志，使用页面的本关 AI 核验请求并记录具体证据；此路线不会显示为自动通过。详见 `docs/SELF-STUDY.md`。\n\n## 变式自测\n\n{lab['probe']}\n\n可以继续使用智能体。先预测，再在副本中修改并核对实际输出；完成后恢复最终版本。\n\n## 按需提示\n\n"
        for i,h in enumerate(lab['hints']): text+=f'<details><summary>提示 {i+1}</summary>\n\n{h}\n\n</details>\n\n'
        text+=f"## 学习对应\n\n配套讲稿：{lab['source']}。精确视频时间点未核验。\n\n参考实现在 `instructor/solutions/{lab['folder']}`，有完整可编译源码。\n"
        put(base+'/HANDOUT.md',text)

    solution={}
    starter={}
    solution['00']={'main.tex':doc('中文能够正常显示。English text is readable.\n\n接管完成。','温度校正研究：工程接管')}
    starter['00']={'main.tex':doc('中文能够正常显示。English text is readable.\n\n接管标记。','师兄的最小工程')}
    structure_body=r'''\begin{abstract}本文以教学合成数据演示论文工程的组织与修改。\end{abstract}
\setcounter{tocdepth}{2}\tableofcontents
{\small 这段说明使用局部小字号。}后面恢复正常字号。A\&B。
\input{sections/intro}
\input{sections/method}
\input{sections/results}'''
    solution['01']={'main.tex':doc(structure_body),'sections/intro.tex':INTRO,'sections/method.tex':r'\section{方法}\label{sec:method}采用误差指标比较两种方法。','sections/results.tex':r'\section{结果与局限}\label{sec:results}这里只是合成数据练习。'}
    starter['01']={'main.tex':doc(r'''\textbf{摘要} 我们要比较两种温度校正方法。

\textbf{引言} 数据来自教学合成数据。先读数据，再算误差。

\textbf{方法} 这里需要层级和列表。

\textbf{结果} 不应推断真实科研效果。
% TODO: 整理结构、拆分子文件、加入列表和特殊字符示例。
''')}
    rescue=r'''\section{故障合并稿}\label{sec:rescue}
合作组 A\&B 给出的数据如下。内容必须保留。
\begin{itemize}\item 第一项：保留数据。\item 第二项：核对单位。\end{itemize}
\begin{table}[htbp]\centering
\caption{两方法的误差}\label{tab:results}
\begin{tabular}{lr}\toprule 方法 & RMSE\\\midrule
Baseline & 1.000\\Calibrated & 0.500\\\bottomrule\end{tabular}
\end{table}
表~\ref{tab:results} 给出结果。

\noindent\rule{0.9\linewidth}{2pt}
'''
    solution['02']={'main.tex':doc(rescue)}
    bad=doc(rescue).replace(r'\section{故障',r'\sectoin{故障').replace(',booktabs','').replace(r'A\&B','A&B').replace(r'\end{itemize}',r'\end{enumerate}').replace(r'\ref{tab:results}',r'\ref{tab:result}').replace(r'0.9\linewidth',r'1.35\linewidth')
    starter['02']={'main.tex':bad}
    solution['03']={'main.tex':doc(r'\section{图像对比}图~\ref{fig:comparison} 包含子图~\ref{fig:baseline} 和~\ref{fig:calibrated}。'+FIGURE)}
    starter['03']={'main.tex':doc(r'''\section{图像对比}
见下图，两种方法似乎不同。
\begin{figure}[ht]\centering
\fbox{\rule{0pt}{35mm}\rule{0.65\linewidth}{0pt}}
\caption{待替换的占位图}
\end{figure}
% TODO: 插入真实素材，建立双子图、总图题和引用。
''')}
    solution['04']={'main.tex':doc(METHOD+r'\section{结果}表~\ref{tab:metrics} 给出误差汇总。所有数据为教学合成数据。'+TABLE)}
    starter['04']={'main.tex':doc(r'''\section{方法}
下面这段来自智能体，能够编译，但语义待检查。
\begin{equation}
\operatorname{RMSE}=\frac{1}{n}\sum_{i=1}^{n}|\hat y_i-y_i|.
\end{equation}
\section{结果}
\begin{tabular}{|l|r|r|}\hline
方法 & RMSE & MAE\\\hline
Baseline & 1.000 & 1.000\\
Calibrated & 0.050 & 0.500\\\hline
\end{tabular}
% TODO: 核对原始 CSV，生成规范表格，补充公式解释和引用。
''')}
    citebody=r'''\section{资料引用练习}
文档准备参考 Lamport 的教材\cite{lamport1994}。
排版系统背景参考 Knuth 的著作\cite{knuth1984}。
Einstein 的论文\cite{einstein1905}仅用于练习期刊条目的导入与引用，
并非温度校正方法的理论依据。
\printbibliography[title={参考文献}]
'''
    legacy=r'''% !TeX program = xelatex
\documentclass[UTF8,fontset=fandol]{ctexart}
\usepackage[numbers]{natbib}
\begin{document}
\citet{lamport1994}介绍文档准备；括号式引用\citep{knuth1984}。
\bibliographystyle{unsrtnat}
\bibliography{references}
\end{document}'''
    solution['05']={'main.tex':doc(citebody,pre=PRE+BIBPRE),'references.bib':BIB+INCOMING,'incoming.bib':INCOMING,'legacy/main.tex':legacy,'legacy/references.bib':BIB+INCOMING}
    starter['05']={'main.tex':doc(citebody,pre=PRE+BIBPRE.replace('style=numeric,sorting=none','style=alphabetic,sorting=nyt')),'references.bib':BIB,'incoming.bib':INCOMING,'legacy/main.tex':legacy,'legacy/references.bib':BIB+INCOMING}
    paperbody=r'''\begin{abstract}本文使用六条教学合成观测比较两种温度校正结果，演示论文结构、图表与文献的组织。本文不报告真实科研发现。\end{abstract}
\input{sections/intro}
\input{sections/method}
\input{sections/results}
\section{排版资料}
文档组织参考\cite{lamport1994}，排版背景参考\cite{knuth1984}。
文献\cite{einstein1905}仅作期刊条目格式示例，不作为本方法依据。
\printbibliography[title={参考文献}]
'''
    template_docs={
      'labpaper.cls':CLASS,
      'TEMPLATE.md':'''# 教学编辑部格式要求 v2.0
此类文件为 LaTeXLab 原创练习模板，不代表任何学校或期刊。

- 使用 `\\documentclass[review]{labpaper}`。
- 模板管理 A4、10pt、双栏、20 mm 四边距和页码；主文档不要重复设置 geometry。
- review 隐藏 author，final 显示 author。不要修改 .cls 来切换模式。
- 内容文件、图片和文献库仍由作者管理。自行检查全文和 PDF 元数据的匿名性。
- 通用包：amsmath、graphicx、booktabs、subcaption、biblatex。模板未自动载入它们。
- XeLaTeX + Biber。Fandol 字体随完整 TeX Live 提供，无需操作系统商业字体。
- 不要求做成正式投稿论文，不包含学校封面或版权声明。
''',
      'MIGRATION.md':'''# 教学迁移卡
旧草稿：ctexart + 自己设置 margin=25mm；作者始终显示；单栏。
新模板：labpaper v2；版心由类管理；review/final 控制匿名；双栏。

先跑新模板最小文档，再迁移宏包和内容，逐次编译。冲突时定位双方责任，不删除整块正文。
在 REPORT 写下每项旧设置的去向。不要把本文档的 review 选项套到 SJTUThesis。
''', 'thesis/main.tex':THESIS}
    full={'main.tex':doc(paperbody,pre=TEMPLATE_PRE+BIBPRE),'sections/intro.tex':INTRO,'sections/method.tex':METHOD,'sections/results.tex':RESULT,'references.bib':BIB+INCOMING,**template_docs}
    solution['06']=full.copy()
    solution['06']['thesis/main.tex']=THESIS.replace('这里是中文摘要。','本练习以六条合成观测演示学位论文结构。').replace('This is a typesetting exercise.','This exercise demonstrates thesis structure using six synthetic observations.').replace(r'\newtheorem{theorem}{定理}',r'\newtheorem{theorem}{零误差性质}').replace('全部观测均为教学合成数据。','六条观测均为教学合成数据，不对应任何真实设备或受试者。')
    starter['06']={**full,'main.tex':doc(paperbody,pre=PRE+BIBPRE)}
    review='''# 编辑部来信 · 请逐项处理

1. 使用 labpaper v2 的 review 模式，不修改类文件。
2. 用真实章节组织论文，加入摘要，正文说明数据为合成数据。
3. RMSE 定义要有平方和平方根；n=6。表中 Calibrated RMSE 应由原始数据复核。
4. 并排展示 baseline.pdf 和 calibrated.pdf，分别标记子图，使用动态引用。
5. 用三线表，保留三位小数与单位；不要以表格图片代替可编辑表格。
6. 导入 Lamport，数字引用按首次出现顺序；三条文献都要出现且说明用途。
7. 修正硬写的章节/公式/图表编号，不声称六条合成数据证明实际泛化效果。
8. 交付可复编译源码包和最终 PDF。说明使用智能体的范围与自己的核验依据。
'''
    solution['07']={**full,'REVIEW.md':review}
    starter['07']={**full,'REVIEW.md':review,'main.tex':doc(r'''\input{sections/intro}
\input{sections/method}
\input{sections/results}
\printbibliography''',pre=PRE+BIBPRE.replace('sorting=none','sorting=nyt')),
    'sections/intro.tex':r'''% !TeX root = ../main.tex
\textbf{引言}
我们采用六条教学合成数据。本稿参考排版背景资料\cite{knuth1984}，
并用\cite{einstein1905}练习期刊文献引用。
% TODO: 补入 Lamport 引用和真实章节结构。
''',
    'sections/method.tex':r'''% !TeX root = ../main.tex
\section{方法}
\begin{equation}\operatorname{RMSE}=\frac1n\sum_{i=1}^{n}|\hat y_i-y_i|.\end{equation}
公式 1 就是我们的评估方法。
''',
    'sections/results.tex':r'''% !TeX root = ../main.tex
\section{结果}
见图 1 和表 1，真实部署一定有效。
\begin{figure}[ht]\centering\includegraphics[width=0.5\linewidth]{baseline.pdf}\caption{结果}\end{figure}
\begin{tabular}{|l|r|r|}\hline 方法 & RMSE & MAE\\\hline Baseline & 1.000 & 1.000\\Calibrated & 0.050 & 0.500\\\hline\end{tabular}
''','references.bib':BIB,'incoming.bib':INCOMING}
    # Reproducible, original teaching figures and data.
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    media=ROOT/'assets'; media.mkdir(exist_ok=True)
    for name,errs in [('baseline',[1,-1,1,-1,1,-1]),('calibrated',[.5,-.5,.5,-.5,.5,-.5])]:
        fig,ax=plt.subplots(figsize=(4.8,3.2),layout='constrained')
        ax.plot(range(1,7),errs,'o-',color='#14766b',lw=2)
        ax.axhline(0,color='#84909b',lw=.8);ax.set(xlabel='Observation',ylabel='Error (°C)',ylim=(-1.3,1.3),xticks=range(1,7))
        ax.grid(alpha=.15);ax.spines[['top','right']].set_visible(False)
        fig.savefig(media/f'{name}.pdf');plt.close(fig)
    obs='index,truth,baseline,calibrated\n1,20,21,20.5\n2,21,20,20.5\n3,22,23,22.5\n4,23,22,22.5\n5,24,25,24.5\n6,25,24,24.5\n'
    summary='method,RMSE_C,MAE_C\nBaseline,1.000,1.000\nCalibrated,0.500,0.500\n'
    for lab in LABS:
        for kind,files in [('starter',starter[lab['id']]),('solution',solution[lab['id']])]:
            base=f"labs/{lab['folder']}/starter" if kind=='starter' else f"instructor/solutions/{lab['folder']}"
            project(base,files)
            shutil.copyfile(ROOT/f"labs/{lab['folder']}/REPORT.md",ROOT/base/'REPORT.md')
            if int(lab['id'])>=3:
                for name in ['baseline','calibrated']:
                    target=ROOT/base/'figures';target.mkdir(exist_ok=True)
                    shutil.copyfile(media/f'{name}.pdf',target/f'{name}.pdf')
                put(base+'/data/observations.csv',obs);put(base+'/data/summary.csv',summary)
    put('course.json',json.dumps(LABS,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
