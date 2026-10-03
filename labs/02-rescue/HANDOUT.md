# Rescue Lab · 拆掉六个编译炸弹

## 情景

合作者合并了一段智能体生成的代码，论文突然无法编译。截止前你要找到首个根因，逐个修复，并保留每次诊断证据。

## 启动

在项目根目录运行 `python tools/lab.py start 02`，或手动复制本关 `starter` 文件夹和 `REPORT.md` 到自己的工作目录。打开复制品中的 `main.tex`。每关独立可做，不会因上一关卡住而无法开始。

## 任务

1. 对 starter 做第一次真实编译。不要先查看参考解。在自己的笔记中为每次修复记录：首个有效错误或警告、文件与行、判断、最小修改、重编译结果。

2. 工程内有六类问题：命令拼写、宏包依赖、特殊字符、环境闭合、交叉引用、版心溢出。按实际日志出现的顺序处理；后续错误可能是前一个错误的连锁反应。

3. 保留题目中的全部信息、表格和数据。不能删除报错段、关掉警告、改成图片或硬写编号来过关。将 label 放在产生相应编号的位置之后。

4. 最后进行一次干净构建，检查 PDF、日志和引用。区分 error、undefined reference 与 Overfull hbox 的后果。

## 结果对照

将源码、最终 PDF 和核验报告留给自己。REPORT.md 是可选笔记；下面这些结果可结合自动报告、理解题与 PDF 自查逐项核对。

- 六类问题都已修复，原有内容保留，交叉引用可随编号变化。
- 最终日志无未定义引用、致命错误或本题制造的溢出。
- 用六类问题的修复证据核对结果，能说明为何先看首个错误。

## 技术检查

`python tools/lab.py check 02`

检查器在 `_build/` 的副本中真实构建，生成 `check-report.json`、`check-report.html` 与日志，并更新 `reports/latest-02.json`。把 JSON 导入离线手册查看具体的 pass / fail / unavailable 项，再完成该关理解题和 PDF 自查。没有本地环境时，下载在线平台的当前源码、PDF 和日志，使用页面的本关 AI 核验请求并记录具体证据；此路线不会显示为自动通过。详见 `docs/SELF-STUDY.md`。

## 变式自测

在副本中将一个 ref 的键拼错，预测结果，再编译验证并恢复。

可以继续使用智能体。先预测，再在副本中修改并核对实际输出；完成后恢复最终版本。

## 按需提示

<details><summary>提示 1</summary>

从日志首个指向源码的错误开始；Emergency stop 常常不是根因。

</details>

<details><summary>提示 2</summary>

命令名区分拼写；toprule 由 booktabs 提供；正文中的 & 与 tabular 内的 & 意义不同。

</details>

<details><summary>提示 3</summary>

检查 sectoin、booktabs、A&B、itemize 的结束环境、tab:result / tab:results 和 1.35 倍版心的固定横线。每次只修一个根因。

</details>

## 学习对应

配套讲稿：sjtuthesis.tex「编译问题排查」· reference.tex。精确视频时间点未核验。

参考实现在 `instructor/solutions/02-rescue`，有完整可编译源码。
