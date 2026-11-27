# BA2023 Operations Research — Report Workspace

本仓库供两名论文作者统一获取研究资料、完善英文Report并记录审核进度。当前目标是基于已有数学与编程成果完成Report，不另设建模手/编程手岗位。仓库Public，Projects保持原可见性；新资料须有公开权限。

## 最新资料导航

| 模块 | 当前候选与入口 | 状态 |
| --- | --- | --- |
| Mathematical Modeling | [模型说明](MCM_B_v9/MCM_B_v9_建模修订与独立验证说明.docx) | 与初稿DOCX相同；硬件说明以新版源码/交接为准 |
| Mathematical Proofs | [8份证明](MCM_B_v9/proofs/) | 建设证明新增常数到代码映射 |
| Programming | [新版复跑程序](月球基地_编程组交付包_修订版/复跑程序/) / [运行说明](月球基地_编程组交付包_修订版/复跑程序/00_运行说明.md) | 20个PY；主流程闭式充分上界+有限目录 |
| Data and Parameters | [来源/假设](MCM_B_v9/evidence/) | 题面/常数/团队情景分开；第三方全文不入库 |
| Computational Results | [Q1–Q5结果表](月球基地_编程组交付包_修订版/results/论文组结果表.csv) / [敏感性](MCM_B_v9/results/sensitivity_v9.csv) | 新版9命令复跑退出0；六表数值一致、ID跨环境漂移 |
| Figures | [最新PNG/SVG](月球基地_编程组交付包_修订版/figures/) | 5组逻辑图；引用时匹配同批表/记录 |
| Validation and Verification | [交付验证](月球基地_编程组交付包_修订版/evidence_chain/) / [运行记录](月球基地_编程组交付包_修订版/results/run_record.json) | LP只作核验；技术通过不等于现实验证 |
| Academic Report | [英文DOCX初稿](report.1docx.docx) | 当前需整改，封面题名冲突等未解决 |
| Review and Revision | [Report Review Matrix](review/report_review_matrix.md) / [CSV](review/report_review_matrix.csv) / [路线图](review/report_completion_roadmap.md) | 21项；负责人待两人确认 |
| Handoff Documentation | [先读](月球基地_编程组交付包_修订版/00_先读.md) / [核心代码摘录](月球基地_编程组交付包_修订版/报告核心代码摘录.md) | 最新编程交接 |
| 项目进度 | [PROGRESS](PROGRESS.md) / [本轮同步报告](review/latest_sync_report.md) / [Issues](https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues) | 以真实证据更新 |

## 使用与版本

最新四份大结果JSON存于 `MCM_B_v9/results/research_results_revision.zip`。检出后执行 `python3 review/checks/restore_latest_results.py` 恢复并核验SHA-256，已有不同结果会报错而非覆盖。原代码路径不变。数值复跑使用独立环境，参考复跑说明；运行会写结果，请复制到隔离目录再执行。

初稿基线为 `v0.1-first-draft`，旧 `MCM_B_v9_编程组/` 为历史包，不与新版同名结果混用。模型包和新编程包是相同源码的不同运行批次，不能只凭策略ID拼接；详情见[编程差异](review/programming_version_diff.md)。BA2023教师Guidelines/Rubrics未取得前不宣称Excellent或提交就绪。

## 双人Word协作

编辑前查看远程分支/最新commit，并在Issue或Review Matrix确认编辑范围。并行编辑使用各自命名副本和分支，记录父提交；不要自动合并或覆盖另一人的DOCX。人工合并后保存新版本，核对最新数值/图表/引用与最终渲染，再提交PR；重大模型或结论变化先确认。GitHub固定版本是资料入口，避免多个聊天压缩包形成隐含最新版。
