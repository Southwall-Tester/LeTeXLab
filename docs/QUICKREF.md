# 按症状查，不按命令背

|现象|先查什么|最小验证|
|---|---|---|
|命令不存在 / ENOENT|实际执行的程序、发行版安装、PATH|终端运行 xelatex --version|
|Undefined control sequence|首个出错命令的拼写及提供它的宏包|只修一处，再编译|
|File ... not found|相对主文件的路径、大小写、zip 内是否漏文件|换新目录编译；Windows 不敏感不代表 Linux 也如此|
|Missing $ inserted|正文下划线、未成对的数学定界符|检查出错行及其前一行|
|Misplaced alignment tab &|正文中的 & 没转义或表格列数不对|普通文本用反斜线转义；表格逐行数分隔|
|begin... ended by...|环境名是否成对，是否不合法嵌套|从最内层检查|
|引用出现 ??|主键/label 拼写、标签位置、是否重编译|检查 .aux 和最后一轮日志|
|文献不显示|cite 主键、bib 数据、后端、文献输出命令|辨认 .bcf→Biber 或 .aux→BibTeX|
|Overfull hbox|图片宽度、固定列宽、长单词/路径、当前栏宽|打开对应 PDF 页，检查实际越界|
|字体缺失 / 缺字|编译引擎、字体是否存在、字形覆盖|先用本包 Fandol 基线；再按模板手册调整|
|Option clash|同一宏包被模板和正文用不同参数重复加载|读取模板职责，删重复配置而非删正文|
|PDF 没变化|编译的根文件、返回码、PDF 时间、是否看旧缓存|用全新构建目录验证|

## 常见结构

```tex
\documentclass{ctexart}       % 文档类型
\usepackage{graphicx}        % 导言区的功能包
\begin{document}             % 正文开始
\section{方法}\label{sec:method}
\input{sections/method}      % 像插入文本一样接入子文件
\end{document}
```

`\command[可选参数]{必选参数}` 是常见形式，具体以该命令为准。`%` 后是注释；空行分段；空格不是稳定的布局工具。正文中的 `% _ & # $` 一般需转义。

图表的 `label` 放在 `caption` 后；章节标签放标题后；公式使用有编号环境和 `eqref`。浮动体会为排版移动，源码位置不承诺最终页面位置。

## 扩展微实验（对应视频提及的能力）

在某关工作目录创建 scratch.tex，复制已验证的导言区。以下内容均可独立编译；不要求加入投稿正文。

### 长文本表格

用 `p{4cm}` 给描述列固定宽度，比较与 `l` 列的换行差异。用 `\multicolumn{1}{c}{描述}` 临时居中表头；有多个共享表头时用 `\multicolumn{2}{c}{指标}`，下一行必须相应补齐列。

### 多行公式

```tex
\begin{gather}
 a=b+c\\
 d=e+f
\end{gather}
\begin{multline}
 S=a_1+a_2+a_3+a_4+a_5\\
 +a_6+a_7+a_8.
\end{multline}
```

比较 align 的指定对齐、gather 的逐行居中、multline 的首末行位置。长公式是否要拆行由真实栏宽决定。

### 跨页表与表下注释

60 行原始数据需跨页：单栏附录可用 longtable（载入同名宏包），不要再套 table 浮动体；双栏场景需先设计单栏页或遵守模板替代方案。复制普通数据行到跨页，观察页断点，并查 `endfirsthead/endhead` 设置重复表头。

仅三行汇总数据但有单位和显著性注释：可用 threeparttable 包，在 table 内组织 threeparttable、tabular、tablenotes；不要为这三行使用跨页机制。写一句选择理由即可，进阶实现按需。

### 图像参数与浮动

在副本中试 `width`、`height`、`scale`、`angle`；同时给宽高可能导致拉伸，可使用 keepaspectratio。正式稿只保留满足阅读尺寸的版本。H 需要 float 包，允许移动的 h/t/b/p 通常更灵活。

这些微实验只扩展排版工具选择，不要求宏编程、TikZ 绘图或手写类文件。
