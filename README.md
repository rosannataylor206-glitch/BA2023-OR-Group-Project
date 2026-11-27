# BA2023 Operations Research — 个人研究管理

Repository: BA2023-OR-Group-Project

Operations Research Group Project | Mathematical Modeling, Optimization, Computational Validation and Academic Report

本科 Operations Research Group Project 的个人研究成果管理、版本控制、质量审核和论文完善空间。数学建模、程序求解与英文报告已形成初稿；当前优先冻结完整基线，然后提升研究与计算质量。**初稿完成不代表审核通过。**

- [Public Repository](https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project)
- [Private Projects](https://github.com/users/rosannataylor206-glitch/projects/1)
- [现有 18 项 Issues](https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues)

用户已自行邀请一名组员；Agent 不代为邀请或管理权限，不扩展复杂多人流程。GitHub 上的管理定位不改变课程小组成果的作者身份、学术责任或存储权限。

## 研究与基线入口

| 路径 | 用途 |
| --- | --- |
| `report.1docx.docx` | 可编辑英文论文初稿；原样拟存档，需确认作者元数据和存储权限 |
| `MCM_B_v9_编程组/MCM_B_v9_建模修订与独立验证说明.docx` | v9 可编辑模型说明与公式；并非根目录英文报告的自动生成源 |
| `MCM_B_v9_编程组/proofs/` | 物理、建设、供水、联合决策、成本/环境和敏感性的推导 |
| `MCM_B_v9_编程组/*.py`、`reference/`、`utils/` | 完整数值、验证、补充分析、图表和建文档源代码 |
| `MCM_B_v9_编程组/evidence/*.json` | 参数来源、假设、公开资料索引；不包含第三方论文全文 |
| `MCM_B_v9_编程组/results/` | 核心 JSON/CSV、阶段证书、敏感性及历史运行记录 |
| `MCM_B_v9_编程组/figures/` | PNG 与可编辑 SVG 图表；灰度 QA 副本保留本地 |
| `review/baseline/coverage.md` | 核心文件依赖、参数/数据口径与覆盖边界 |
| `review/baseline/phase1_upload_scope.md` | 最终逐项上传范围与人工存储权限确认点 |
| `AGENTS.md`、`PROGRESS.md`、`CHANGELOG.md` | 六阶段规范、真实进度与重要版本记录 |

旧版本、重复交接包、不相关 Q1 实验、虚拟环境、缓存、凭证、第三方课程/题目 PDF 和重新分发许可未核验的 Skills 保留本地。首次推送前必须审批确切清单，不改变原始文件路径或运行关系。

## 运行边界

`v0.1-first-draft` 保存未经正式审核的初稿。历史入口是 `MCM_B_v9_编程组/run_v9.py`。首次从仓库检出后，先运行 `python3 review/baseline/restore_large_results.py`：它从无损 ZIP 恢复 `results/joint_v9.json` 与 `results/phases_v9.json`，逐文件核验 SHA-256，再使用原有验证与绘图脚本。此步骤只恢复存档证据，不代表数值结果已经通过本轮审核。

Phase 2 将在本项目独立环境解决 NumPy 等兼容性；当前 Anaconda NumPy 1.26.4 不满足 v9 的 numpy>=2.0。历史依赖记录并非本机复现证据。所有实际复跑须在隔离副本执行，避免覆盖原始结果。建模 DOCX 构建另需 Pandoc/字体；原始题目 PDF 排除远程存储时，原打包脚本的题目文件要求仍未满足，不声称所有构建/打包流程已就绪。

## 质量提升流程

1. Phase 1：批准存储清单后 Commit、Tag `v0.1-first-draft`、Push。
2. Phase 2：独立环境与课程权威材料核验；缺件明确列出。
3. Phase 3：建模、算法、数值验证、学术审稿与课程评审五视角审核，并记录实际独立性。
4. Phase 4–5：逐章节保留/修改/删除/补充方案及七份审核报告。
5. 综合方案经用户确认后才正式修改模型、核心代码和论文。
6. 重要阶段同步报告、PROGRESS、现有 Issues、Projects 与 Commit；仅上传批准范围内成果。

以真实课程 Rubrics 的 Excellent 为目标；没有 Rubrics 时不编造权重、分数或已达 Excellent 的结论。代码、模型和论文均须接受实证核验，不能只做语言润色。

## 当前 GitHub 可见性

仓库按所有者 2026-11-27 的最新选择设为 Public；所有者已自行邀请一名组员。Projects 仍 Private。新增研究成果公开前先核对存储权限和敏感信息，重大模型/代码/论文修订仍经综合审核与用户确认。
