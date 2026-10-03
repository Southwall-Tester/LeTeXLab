# Template Lab · 换模板，不拆房子

## 情景

编辑部退回了格式检查：必须使用提供的双栏匿名模板。与此同时，实验室让你理解学位论文的前置、正文与后置部分，避免照搬三年前视频里的旧选项。

## 启动

在项目根目录运行 `python tools/lab.py start 06`，或手动复制本关 `starter` 文件夹和 `REPORT.md` 到自己的工作目录。打开复制品中的 `main.tex`。每关独立可做，不会因上一关卡住而无法开始。

## 任务

1. 先读 TEMPLATE.md 和 MIGRATION.md。把主文档从 ctexart 迁移到随附 labpaper v2，启用 review。不要修改 .cls，不要叠加 geometry 改回旧边距。

2. 迁移正文、图、表、公式、参考文献到新模板，保留相对路径和标签。双栏中优先用 linewidth 控制图宽，宽表可调整结构或合理使用跨栏浮动体。

3. 检查 PDF 的 A4、20 mm 边距、双栏、匿名作者、页码，以及 PDF 元数据中是否还留下真实姓名。说明哪些参数由模板管理。

4. 编译 thesis/main.tex。实际修改中文摘要与英文摘要，把定理标题改成“零误差性质”，补一个附录说明。辨认 frontmatter/mainmatter/appendix/backmatter、chapter、目录与图表目录。

5. 阅读 docs/TEMPLATE-TRANSFER.md 的讲稿映射和迁移卡。填写官方 SJTUThesis 的文档类选项、sjtusetup、字体、数学样式、版权页、文献入口位置；区分 2023 讲稿示例和当前安装版。遇到旧选项先查同版本手册。

## 结果对照

将源码、最终 PDF 和核验报告留给自己。REPORT.md 是可选笔记；下面这些结果可结合自动报告、理解题与 PDF 自查逐项核对。

- 主文档通过教学模板的 review 模式，.cls 保持原样；图表没有挤出栏宽。
- thesis 副本可编译，新增定理名称与附录可见，说明前后页码和章节编号。
- 迁移记录含旧接口与新入口；明确教学模板不是学校正式模板。

## 技术检查

`python tools/lab.py check 06`

检查器在 `_build/` 的副本中真实构建，生成 `check-report.json`、`check-report.html` 与日志，并更新 `reports/latest-06.json`。把 JSON 导入离线手册查看具体的 pass / fail / unavailable 项，再完成该关理解题和 PDF 自查。没有本地环境时，下载在线平台的当前源码、PDF 和日志，使用页面的本关 AI 核验请求并记录具体证据；此路线不会显示为自动通过。详见 `docs/SELF-STUDY.md`。

## 变式自测

在副本切换 review → final，观察作者字段；再切回 review，解释为何不直接改 cls。

可以继续使用智能体。先预测，再在副本中修改并核对实际输出；完成后恢复最终版本。

## 按需提示

<details><summary>提示 1</summary>

先让模板的最小文档编译，再迁移内容，最后逐个恢复宏包。

</details>

<details><summary>提示 2</summary>

模板已载入 geometry；重复指定不同选项可能导致 Option clash。

</details>

<details><summary>提示 3</summary>

匿名是内容审查任务，不仅是隐藏 author：致谢、项目名、PDF 元数据也可能泄露身份。当前练习只用虚构材料。

</details>

## 学习对应

配套讲稿：sjtuthesis.tex · newversion.tex。精确视频时间点未核验。

参考实现在 `instructor/solutions/06-template`，有完整可编译源码。
