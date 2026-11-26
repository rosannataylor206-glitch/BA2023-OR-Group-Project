# 个人研究项目进度

更新：2026-11-26。当前为 First Draft Completed / Quality Assurance 准备阶段。

**初稿完成 ≠ 通过质量审核。** Gate 1–6 均为 NOT_RUN。没有把保存的历史运行记录当作本轮验证结果。

## 任务

| ID | 任务 | Category | 状态 | 证据 / 下一步 | GitHub Issue |
| --- | --- | --- | --- | --- | --- |
| D01 | 数学建模初稿 | Mathematical Modeling | Done | 用户确认初稿完成；候选模型说明和 proofs 文件存在。未进行独立模型审核。 | [#1](https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/1) |
| D02 | 编程求解初稿 | Programming | Done | 用户确认初稿完成；候选代码与保存结果存在。历史运行记录不等于本轮测试通过。 | [#2](https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/2) |
| D03 | 论文初稿 | Academic Writing | Done | 用户确认初稿完成；report.1docx.docx 存在。未评审正文。 | [#3](https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/3) |
| D04 | Skill 检查与配置 | Environment | Done | review/00_skill_inventory.md；写作工具 22 项、decision_log 20 项内置测试通过。不是业务测试。 | [#4](https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/4) |
| D05 | AGENTS.md 建立 | Environment | Done | 课程规则、六道质量门禁已写入 AGENTS.md。 | [#5](https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/5) |
| D06 | 700 个原始文件完整性验证 | Data & Validation | Done | Git 初始化前 700/700 一致；结束快照仅系统 .DS_Store 漂移，其他 699 个原始文件一致；详见配置报告。 | [#6](https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/6) |
| T01 | NumPy 及相关计算环境兼容性 | Environment | Blocked | 已验证 Anaconda NumPy 1.26.4 不满足 v9 声明 numpy>=2.0；内置文档环境缺 SciPy/Matplotlib。验收：隔离环境、依赖记录、最小运行与版本偏差证据。 | [#7](https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/7) |
| T02 | BA2023 课程规范核验 | Requirements | To Do | BA2023 指南、Rubrics、Syllabus、Slides 的适用版本尚未核验；存在 BUS2003 命名文件。验收：课程依据索引与冲突记录。 | [#8](https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/8) |
| T03 | 数学建模独立审核 | Mathematical Modeling | To Do | Gate 1 未运行。验收：约束/假设/单位/可行性与最优性边界的独立检查报告。 | [#9](https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/9) |
| T04 | 编程与算法审核 | Programming | To Do | Gate 2 未运行。验收：静态检查及隔离副本实际复现证据。 | [#10](https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/10) |
| T05 | 数据及数值结果验证 | Data & Validation | To Do | Gate 3 未运行。验收：来源、输入哈希、边界/残差/基准和敏感性报告。 | [#11](https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/11) |
| T06 | 论文深度审核 | Academic Writing | To Do | Gate 5 未运行。验收：结构、证据、语言、引用与格式四遍检查。 | [#12](https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/12) |
| T07 | 模型、代码、数据、结果、论文一致性检查 | Quality Assurance | To Do | Gate 4 未运行。验收：关键主张—证据与多位置数值/单位映射。 | [#13](https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/13) |
| T08 | 模拟 Rubrics 评分 | Quality Assurance | Blocked | 课程 Rubrics 未核验；不编造评分权重或分数。验收：逐条评分依据、证据和不确定性。 | [#14](https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/14) |
| T09 | 受控整改 | Quality Assurance | To Do | 依赖正式审核发现和人工批准的整改范围；不预先虚构问题。验收：新版本、影响分析和受影响门禁复验。 | [#15](https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/15) |
| T10 | 最终独立审核 | Quality Assurance | To Do | Gate 6 未运行。验收：冻结版本、独立性记录、残余问题及提交建议。 | [#16](https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/16) |
| T11 | Presentation 准备 | Presentation | To Do | 尚未制作；课程 Presentation 要求待核验。验收以真实课程要求为准。 | [#17](https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/17) |
| T12 | 最终提交 | Final Submission | Blocked | 需课程要求核验、审核闭环、用户最终确认与最终文件检查；本阶段不提交作业。 | [#18](https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/18) |

GitHub 用于 rosannataylor206-glitch 个人管理；暂不邀请队友，既有 Issue assignees 不自动更改。Done 的 6 项只代表对应初稿/配置任务完成。

## 当前工作与阻碍

- 当前进行 Phase 1 完整研究基线清单核查；清单审批前不进入环境安装或业务审核。
- gh 已从官方源安装并通过 SHA-256 校验；仓库、Projects 与 Issues 状态以 review/00_github_setup.md 为准。
- 首次推送与初稿基线 Commit/Tag 等待人工确认确切上传范围。
- 复现环境、BA2023 规范和 Rubrics 仍待补齐。

## 下一步

1. 已建立 Private 仓库、Projects、18 项 Issues 和标签，全部保留。
2. 核对拟上传逐项清单、共享权利、文档元数据与哈希；取得明确批准后才暂存、提交、打 Tag 和推送。
3. 基线存档后，按已授权的 Phase 2–5 连续开展环境与课程材料准备、实际复跑和全面独立审核；正式整改先交综合方案供用户确认。

## 同步规则

重要审核/整改结束时同步 PROGRESS、Issue、Projects（有权限时）、报告、测试证据、CHANGELOG 和 Commit；获得相应授权后推送，重大修改经人工确认才合并。

GitHub 配置已完成：Private 仓库、Private Projects 和 18 项 Issues 均已核验；首次推送仍待上传范围批准。局部 Git 凭证助手曾被自动审批拒绝；用户随后明确授权仅限本仓库配置，已成功设置并验证。未修改全局 Git 配置，未推送。

当前批准清单已由旧 90 项方案重新核查，以 review/baseline/phase1_upload_scope.md 和最新 upload_manifest.json 为准。初稿基线仍未 Commit/Tag/Push，所有业务门禁 NOT_RUN。

远程最新检查：main 已有初始化提交 a4fdee6be9df0fb8c2f068adc13af990ca424f33，仅含 README.md（144 字节）；本 Agent 未创建该提交，本地仍未提交或暂存。获批后须先核对远程最新历史，以其为父链保存初稿基线，不 force push、不覆盖初始化历史。
