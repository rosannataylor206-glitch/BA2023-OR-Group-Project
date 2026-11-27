# 个人版本与研究记录规范

当前不邀请队友；本文件用于用户个人维护研究版本与审计记录，保留轻量分支和 PR 追踪，不新增多人协作要求。

## 分支与原始基线

`main` 保存经过小组确认的稳定版本。初稿基线经上传范围确认后才建立首个 Commit 和 `v0.1-first-draft` Tag；Tag 表示初稿快照，不表示通过质量审核。

审核用 `review/audit`；受控整改用 `review/revision-v2`；模型、程序、论文分别使用 `feature/model[/issue-N]`、`feature/code[/issue-N]`、`feature/paper[/issue-N]`。这些是命名规则，不预先创建空闲分支。不要在 main 直接实施未经审核的重大修改，不强制推送、不重写共享历史。

先同步 main，再切分支；原有文件不重命名、移动或覆盖。整改需新版本路径和变更记录。Word 等二进制文档另存受控版本；发生冲突时保留版本与来源，不靠自动合并判断学术内容。

## Issue 与严重程度

实际问题使用 `.github/ISSUE_TEMPLATE/problem.yml`，阶段任务使用 `task.yml`；任务不是已发现的缺陷。Issue 须包含 ID（创建后由 GitHub 分配）、描述、严重程度、文件/页码/行号、证据、影响、修复建议、验证方法、负责人及状态。

- `P0-critical`：阻止核心结论成立、严重完整性问题或凭证泄露等经证实的关键问题。
- `P1-major`：显著影响模型、结果、复现或课程要求的重要问题。
- `P2-minor`：局部问题，影响较小且不改变核心结论。
- `P3-enhancement`：改进建议。
- 领域标签：`modeling`、`programming`、`data`、`paper`、`validation`、`documentation`；受外部条件阻塞时加 `blocked`。

没有证据不预填严重缺陷。负责人未确认时写“待认领”，不虚构姓名或账号。截图/日志中的隐私与凭证不得粘贴到 Issue。

## 状态与完成定义

使用 `To Do`、`In Progress`、`In Review`、`Done`、`Blocked`。Category 使用 Requirements、Environment、Mathematical Modeling、Programming、Data & Validation、Academic Writing、Quality Assurance、Presentation、Final Submission。

`Done` 必须对应该任务自身的明确验收证据；“完成初稿”和“通过审核”是不同任务。初稿任务可根据用户确认与文件存在记录 Done，但不得据此关闭后续审核任务。证据未完成的审核只能保留其他状态。

## Commit 与 PR

Commit 格式建议 `类型(范围): 具体改动`，如 `docs(progress): 记录环境兼容性阻碍`、`fix(code): 修复已核验的约束实现问题`。避免空泛的 update/final。禁止 `git add .`；逐文件暂存，检查 staged diff、文件列表、体积、共享权利和敏感信息。

PR 使用仓库模板，记录实际验证命令、环境、退出码、误差/容差、报告路径及未验证项。`Closes #N` 仅用于确已满足验收条件的问题；其他关联用 `Refs #N`。重大调整需要用户确认，不自动合并。

## 持续同步

每个重要审核或整改任务结束后：更新 PROGRESS.md、相关 Issue 和有权限的 Projects；保存报告、测试证据和 CHANGELOG；创建说明明确的 Commit；获得相应授权后推送指定分支。未授权推送时保留本地提交并说明阻碍。最终独立审核前冻结候选 Commit/Tag 与文件哈希；不得借用历史 PASS。

## 首次推送

先审阅 `review/github_setup/upload_inventory.csv` 的逐项决定及 `review/00_github_setup.md`。批准仅针对确认的确切清单和内容哈希；新增文件、内容变化或新发现的共享风险必须重新说明。首次推送前不得上传原始项目文件，不通过 Contents API 绕过该要求。


最新执行顺序：先批准 review/baseline/phase1_upload_scope.md 所列确切文件及存储权限，再保存基线。此后按 AGENTS.md 连续审核，不为每个小步骤重复询问；正式修改模型、核心代码及论文，须先提交七份综合审核交付与整改方案，由用户确认。已批准的上传范围不能推定覆盖新的第三方或敏感文件。

## 双人Report协作（最新）

两名作者共同完善Report，负责人由两人确认，Agent不指派。Review Matrix为章节整改入口；每次更新记录父commit、文件SHA、改动、影响模型/数字/图表、验证状态和待办。先检查远程分支/PR，提交至实际需要的report或review分支。DOCX并行稿必须另存、保留双方原稿并人工合并；禁止自动覆盖。数学或核心数值变化先批准。公开权限按本轮具体确认范围执行，课程材料/第三方全文/Skills/凭证不入库。

## 默认main写作入口

main维护当前已获授权共享的完整研究资料与论文候选，README为统一导航。两位作者开始写作前读取main最新commit；论文改动在独立分支或独立Word副本进行，记录父版本，保留双方改稿并人工合并。每次更新核对模型/代码/结果/图表/正文，保存修改记录，再通过PR同步main。禁止覆盖他人Word、force push或把未验证论文标成Done。保持Report中心的轻量流程。
