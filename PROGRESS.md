# 个人研究项目进度

更新：2026-11-27。当前为 First Draft Baseline Archived / Quality Assurance 审核报告待整改阶段。

**初稿完成 ≠ 通过质量审核。** Gate 1–5 已产生有边界的审核证据，但均未达无保留 PASS；Gate 6 NOT_RUN。M1 独立质检 BLOCKED；详见 review/01–07。

## 任务

| ID | 任务 | Category | 状态 | 证据 / 下一步 | GitHub Issue |
| --- | --- | --- | --- | --- | --- |
| D01 | 数学建模初稿 | Mathematical Modeling | Done | 用户确认初稿完成；候选模型说明和 proofs 文件存在。未进行独立模型审核。 | [#1](https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/1) |
| D02 | 编程求解初稿 | Programming | Done | 用户确认初稿完成；候选代码与保存结果存在。历史运行记录不等于本轮测试通过。 | [#2](https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/2) |
| D03 | 论文初稿 | Academic Writing | Done | 用户确认初稿完成；report.1docx.docx 存在。未评审正文。 | [#3](https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/3) |
| D04 | Skill 检查与配置 | Environment | Done | review/00_skill_inventory.md；写作工具 22 项、decision_log 20 项内置测试通过。不是业务测试。 | [#4](https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/4) |
| D05 | AGENTS.md 建立 | Environment | Done | 课程规则、六道质量门禁已写入 AGENTS.md。 | [#5](https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/5) |
| D06 | 700 个原始文件完整性验证 | Data & Validation | Done | Git 初始化前 700/700 一致；结束快照仅系统 .DS_Store 漂移，其他 699 个原始文件一致；详见配置报告。 | [#6](https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/6) |
| T01 | NumPy 及相关计算环境兼容性 | Environment | Done | 项目 .venv：NumPy 2.3.5 / SciPy 1.17.0 / Matplotlib 3.10.8；pip check=0；隔离 run_v9.py 退出 0。 | [#7](https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/7) |
| T02 | BA2023 课程规范核验 | Requirements | Blocked | BA2023 指南、Rubrics、Syllabus、Slides 的适用版本尚未核验；存在 BUS2003 命名文件。验收：课程依据索引与冲突记录。 | [#8](https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/8) |
| T03 | 数学建模独立审核 | Mathematical Modeling | In Review | Gate 1 未运行。验收：约束/假设/单位/可行性与最优性边界的独立检查报告。 | [#9](https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/9) |
| T04 | 编程与算法审核 | Programming | In Review | Gate 2 未运行。验收：静态检查及隔离副本实际复现证据。 | [#10](https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/10) |
| T05 | 数据及数值结果验证 | Data & Validation | In Review | Gate 3 未运行。验收：来源、输入哈希、边界/残差/基准和敏感性报告。 | [#11](https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/11) |
| T06 | 论文深度审核 | Academic Writing | In Review | Gate 5 未运行。验收：结构、证据、语言、引用与格式四遍检查。 | [#12](https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/12) |
| T07 | 模型、代码、数据、结果、论文一致性检查 | Quality Assurance | In Review | Gate 4 未运行。验收：关键主张—证据与多位置数值/单位映射。 | [#13](https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/13) |
| T08 | 模拟 Rubrics 评分 | Quality Assurance | Blocked | 课程 Rubrics 未核验；不编造评分权重或分数。验收：逐条评分依据、证据和不确定性。 | [#14](https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/14) |
| T09 | 受控整改 | Quality Assurance | Blocked | 依赖正式审核发现和人工批准的整改范围；不预先虚构问题。验收：新版本、影响分析和受影响门禁复验。 | [#15](https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/15) |
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

## 2026-11-27 实际审核快照

- 远程 Private main `9994d70`、Tag `v0.1-first-draft`，父提交 `a4fdee6`；95 文件逐 SHA/大小核验。两份大 JSON 无损 ZIP 恢复；英文 DOCX 仅远程副本去除 WPS 数字账号元数据。
- 项目 .venv 兼容环境可用；隔离复跑退出 0，80.846 秒；独立跨材料算术 19/19。复跑策略 ID 漂移，不标字节级复现通过。
- 七份审核报告已写入 review/01–07；P0 封面农业题与正文月球题不一致，P1 运力口径歧义、课程 Rubric 缺失、外部设施未闭合等。模型/论文整改等待用户确认。
- 历史 MCM_B_v9/ 目录有 17 项相对早期 700 文件哈希快照变化，另有 .DS_Store 漂移；原因未确认，未混入冻结候选包。
- Issue/Projects 同步状态以远程核验为准；未验证事项不标 Done。

## GitHub 同步核验补充

- 已有任务 #7 已关闭；#8、#15 Blocked；#9–#13 In Review；#14 继续 Blocked。Projects 对应状态已同步。
- 新建实际缺陷 [#19](https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/19)（P0，论文身份）和 [#20](https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/20)（P1，运力口径），均加入 Private Projects，Blocked。18 个原阶段任务保留；看板现共 20 项。

## 可见性更正（2026-11-27）

用户确认仓库 Public 及组员邀请是本人主动操作，并明确选择今后保持 Public。Agent 已据此重新设置并核验仓库 PUBLIC；Projects 保持 Private。误判可见性异常的 [#21](https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/21) 已更正并关闭。未来新增成果公开前仍核对批准范围和敏感信息。

## Report中心更新（2026-11-27）

两名作者共同完善Report，不再分配建模/编程岗位。新版20个PY与当前模型包匹配；主链+LP+导出+绘图+补充共9命令隔离复跑均退出0，6表数值在容差内一致，ID不同。两交付运行记录为不同批次，Report更新需保持整套表/图/ID来源。21项章节整改见review/report_review_matrix.csv，负责人待确认。

本轮共同作者公开授权已取得；新研究范围112项列入latest_research_manifest.csv，四大JSON无损归档，原件只读。旧基线保留；新增工作独立分支，不改main。论文未实际整改，P0封面冲突、P1课程/运力口径、验证与结构问题仍待闭环。

## 当前14项Report任务

| 任务 | Issue | 状态 |
| --- | --- | --- |
| 最新研究资料同步 | [#22](https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/22) | In Review |
| Q1–Q5章节完善 | [#23](https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/23) | To Do |
| 管理启示与结论 | [#24](https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/24) | To Do |
| 英文学术表达 | [#25](https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/25) | To Do |
| 参考文献与引用 | [#26](https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/26) | To Do |
| 数学模型技术核验 | [#9](https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/9) | In Review |
| 最新编程结果核验 | [#10](https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/10) | In Review |
| Report结构检查 | [#12](https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/12) | In Review |
| 图表与数值一致性 | [#13](https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/13) | In Review |
| 敏感性及模型评价 | [#11](https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/11) | In Review |
| Rubrics评分审核 | [#14](https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/14) | Blocked |
| Report整改 | [#15](https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/15) | Blocked |
| 独立终审 | [#16](https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/16) | To Do |
| 最终提交 | [#18](https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/18) | Blocked |

原18项阶段任务和实际缺陷记录全部保留，改名任务已添加原因评论；未分配负责人。新任务不等于通过审核，Report整改仍待批准。

## 本轮同步完成

研究资料与Report审核流程已发布至 `sync/report-materials-20261127`，提交 `62e0d7e`，完整远程树223文件匹配。[PR #27](https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/pull/27)供双人审阅，main与初稿Tag保留。资料同步任务#22可关闭为Done（仅同步完成，不代表研究/论文质量通过）；其余任务按Report Matrix继续。

## main默认首页已更新（2026-11-28）

用户明确授权后，PR #27 以Merge commit `f4c4a94ca4db3c926b7a18c91bb8308dbb20f59e` 合并至main。两位作者现在直接打开仓库默认首页即可获取最新模型/证明、编程、结果、图表、英文Report初稿和审核资料，无需切分支。此前“尚未合并”的段落保留为历史记录，以本节最新状态为准。

README已核对所有相对链接目标，当前模型MCM_B_v9、当前编程/表图为修订交付包、英文Report仍是根目录待整改初稿。合并前PR可合并且未见组员新提交；224文件远程树与本地匹配，112项授权研究内容SHA匹配。未配置CI，未声称CI通过；此前9命令实际运行证据保留。扫描无常见凭证/邮箱/WPS账号模式命中；Git历史作者邮箱和已有本机路径风险仍如前披露。原始Word没有上传覆盖。

保留原main初稿提交和全部PR分支提交，v0.1-first-draft Tag对象仍为 `7a8221a2b6b52828d8a99acc013b6b7b6889519e`；未squash/rebase/force push。后续论文使用独立分支或Word副本，保留双方版本，人工合并、一致性审核并同步修改记录。工作聚焦Report，不增加管理流程。
