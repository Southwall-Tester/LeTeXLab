# Boot Lab · 接管工程

## 情景

周一 09:00。师兄发来一个论文工程，只说“在我电脑上能跑”。你需要证明自己的环境能编译，并找到正文和 PDF 的对应关系。

## 启动

在项目根目录运行 `python tools/lab.py start 00`，或手动复制本关 `starter` 文件夹和 `REPORT.md` 到自己的工作目录。打开复制品中的 `main.tex`。每关独立可做，不会因上一关卡住而无法开始。

## 任务

1. 复制 starter 后打开 main.tex。先原样编译，再把标题改为“温度校正研究：工程接管”，作者改成自己的署名。保留中英文测试段落。

2. 在自己的笔记中记录编辑器、TeX 发行版、实际引擎及版本、主文件、编译动作、PDF 路径。区分编辑器、发行版、XeLaTeX、latexmk 四个角色。

3. 在 PDF 找到“接管标记”，回到对应源码改为“接管完成”，重新编译核对。尝试编辑器的 SyncTeX 正反向跳转，记录实际入口；平台不支持时用搜索定位并注明。

4. 指出导言区、宏包、正文环境、注释以及 .tex / .pdf / .log / .aux 的用途。在日志中找到实际引擎名称。

## 结果对照

将源码、最终 PDF 和核验报告留给自己。REPORT.md 是可选笔记；下面这些结果可结合自动报告、理解题与 PDF 自查逐项核对。

- 中文与英文均显示，标题和署名已改变，正文出现“接管完成”。
- 能分清工具角色；能从输出定位源码，主文件选择正确。

## 技术检查

`python tools/lab.py check 00`

检查器在 `_build/` 的副本中真实构建，生成 `check-report.json`、`check-report.html` 与日志，并更新 `reports/latest-00.json`。把 JSON 导入离线手册查看具体的 pass / fail / unavailable 项，再完成该关理解题和 PDF 自查。没有本地环境时，下载在线平台的当前源码、PDF 和日志，使用页面的本关 AI 核验请求并记录具体证据；此路线不会显示为自动通过。详见 `docs/SELF-STUDY.md`。

## 变式自测

把一个正文短语改成英文再编译；说明为什么换编辑器不等于换编译引擎。

可以继续使用智能体。先预测，再在副本中修改并核对实际输出；完成后恢复最终版本。

## 按需提示

<details><summary>提示 1</summary>

打开 main.tex；正文起点是 begin{document}。

</details>

<details><summary>提示 2</summary>

标题信息在导言区，maketitle 决定其输出位置。中文练习采用 XeLaTeX 与 Fandol 字体。

</details>

<details><summary>提示 3</summary>

若命令不存在，检查 TeX 发行版和 PATH；若已找到引擎但缺包，依据首个错误补齐依赖。不要仅重装编辑器。

</details>

## 学习对应

配套讲稿：intro.tex · install.tex · minimal.tex。精确视频时间点未核验。

参考实现在 `instructor/solutions/00-boot`，有完整可编译源码。
