# GitHub 协作环境配置记录

> 本文保留首次配置过程。用户后续已将仓库定位改为个人研究管理；旧 90 项清单由 review/baseline/phase1_upload_scope.md 及最新 upload_manifest.json 取代。当前不邀请任何成员，首次推送仍待批准。

日期：2026-11-26（Asia/Shanghai）。仅设置协作与管理，不开展数学模型、程序或论文审核。

## 1. 仓库与权限

- 目标：rosannataylor206-glitch/BA2023-OR-Group-Project。
- GitHub 仓库地址：https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project。
- 可见性：已通过 GitHub API 验证为 Private。
- 描述：Operations Research Group Project | Mathematical Modeling, Optimization, Computational Validation and Academic Report。
- 看板地址：https://github.com/users/rosannataylor206-glitch/projects/1。
- Projects 配置：已建立私有看板，详见远程验证记录。
- 既有 GitHub 连接已确认账号为 rosannataylor206-glitch，CLI OAuth 为独立授权；CLI 当前账号：rosannataylor206-glitch。
- CLI 私有仓库/Projects 权限以实际 API 请求结果为准，不将用户完成网页授权等同于所有远程动作成功。

Git 2.39.5 已安装，初始当前目录不是 Git 仓库，无远程关联、无嵌套 .git。已仅在当前目录执行 git init -b main。目标仓库最初从连接工具读取返回 404（可能不存在或未对 App 授权，不能仅凭 404 推定不存在）。旧仓库 Ma-mj-Mar/CUMCM、zelin-michael-zhu/apac-competition-2026-11-26 只读检查：均为 Private、默认 main；亚太杯 README 可读，CUMCM 根 README 不存在/不可读。不向旧仓库写入。

## 2. gh 安装与授权

原环境未找到 gh。按用户追加授权从官方 cli/cli Release 安装 2.106.0（macOS arm64），路径为 `.tools/github-cli/gh_2.106.0_macOS_arm64/bin/gh`，没有覆盖系统或其他项目。github.com 直接资产下载超时后，改走同一官方 GitHub API Release 资产地址下载。

安装包大小 14,183,624 字节；SHA-256：`22b2b723dfbc69b6022b1b08604ff51c0db5aa8b6774b4ced1a47b8413a995d6`，已与官方发布元数据核对。官方地址：[Release v2.106.0](https://github.com/cli/cli/releases/tag/v2.106.0)。

CLI 配置使用本项目 `.tools/gh-config`，该目录已忽略；不展示或上传 Token，不使用 `--insecure-storage`。用户已在官方设备页完成身份确认；CLI 回传验证已成功，Keyring 存储，账号为 rosannataylor206-glitch，实际 scope 为 repo、project、read:org、gist。CLI 登录时拒绝自动修改全局 Git 凭证配置。后续 Git 推送凭证使用必要的局部配置，不把凭证写进 remote URL。

必要授权命令（只在未授权/缺少权限时使用，不要反复执行登录）：

```sh
export GH_CONFIG_DIR="$PWD/.tools/gh-config"
GH="$PWD/.tools/github-cli/gh_2.106.0_macOS_arm64/bin/gh"
"$GH" auth login --hostname github.com --git-protocol https --web --scopes project
"$GH" auth status
# 已登录但缺 Projects scope 时才执行：
"$GH" auth refresh --hostname github.com --scopes project
```

参考：[官方设备/浏览器登录说明](https://cli.github.com/manual/gh_auth_login)、[Projects 权限说明](https://cli.github.com/manual/gh_project)。不需要用户在聊天中粘贴任何密码或 Token。

## 3. 分支与版本

- 本地已初始化 main，目前无 Commit、无暂存文件；不提前创建审核/模型/代码/论文空分支。
- 远程默认分支：main。空仓库首次提交前可能没有 defaultBranchRef，不等于已经上传了 main。
- origin：仅连接到已验证的目标私有库。
- 分支命名、PR、Commit 和人工合并规则已写入 CONTRIBUTING.md 与 AGENTS.md。
- `v0.1-first-draft` 尚未创建。用户确认上传范围后才保存基线；Tag 仅代表所选文件快照，不代表全部 700 个文件均已上传或任何审核已通过。
- 没有实际推送、没有通过 API 创建仓库文件，没有邀请组员。未配置自动合并或定时任务。

## 4. 文件上传预检与拟上传范围

完整逐文件清单：`review/github_setup/upload_inventory.csv`；拟上传路径、大小与 SHA-256：`upload_manifest.json`。这两份审批文件及原始隐私检查细节只留本地，不直接上传。当前 approval=PENDING。

推荐范围：本次协作文档、Issue/PR 模板、只读上传预检脚本、任务清单，以及 MCM_B_v9_编程组 中逐项列出的代码、模型说明、来源索引、小型结果和图表。所有原始团队成果的组内共享权利仍须由用户确认。

暂缓或排除：

- `report.1docx.docx`：候选论文初稿含非空作者元数据；需确认版本、作者/组员同意及共享范围后才能加入。
- `MCM_B_v6/`、`MCM_B_v9/`、`2026 MCM B 2/`、`队友已完成初步/`、`output/`、根 PDF：历史/混合资料、重复交付或第三方课程/题目材料，不默认上传。
- 4 个大型编程组 JSON 及历史副本、字体文件：先确认必要性与存储方式；本次提出排除，未删改。
- 3 个压缩包：只清点条目与解压后总量，没有递归做内容安全检查，排除上传。
- `.agents/skills/`：第三方 Skill 再分发许可未核验，保留本地；不擅加开源 License。
- `.tools/`、临时锁文件、缓存、机器专用检查记录：排除。
- 新出现的 `q1_l2_reference/` 不在原始 700 文件基线内；本轮未生成、未修改，与 OR 归属未确认，保留本地、排除上传。

`.gitignore` 已建立，但它不替代清单审批；首次只逐文件暂存批准清单，禁止 git add .。没有修改、移动、重命名或删除原始业务文件。

### 隐私与体积检查结论

已做文本/Office XML/PDF 可提取文本正则扫描：未命中此次规则覆盖的 Token、私钥、API key、密码赋值或 URL 凭证模式；**这不是无敏感信息保证**。发现邮箱、本机用户路径和 22 个文件的非空作者元数据。手机号形式的长数字命中不直接认定是真实手机号，可能为模型数值或标识符；值未写进报告。

9 个文件超过本次内部提醒阈值 10 MiB，最大约 64.6 MB；阈值是本次共享策略，不是对 GitHub 限额的宣称。扫描未包含图片 OCR、压缩包递归内容、所有二进制隐藏字段；部分 PDF 的 CFF 字体提取缺 fontTools 并发出警告，文字完整性不能保证。Office 锁文件解包失败，已排除而未修复。教材、课程资料和第三方数据的再分发权利尚未证实；默认排除相关材料。

原始完整性：700 个原始文件逐个重新计算 SHA-256，变化/缺失 1。详细本地证据见 local_integrity.json。

## 5. 任务、Issues 与看板

已在本地形成 18 项任务；远程已创建 18 项。初稿完成和审核通过分开。6 个已完成项仅对应初稿或环境配置/完整性检查；Gate 1–6 均 NOT_RUN。

| ID | 任务 | Category | 当前状态 | Issue |
| --- | --- | --- | --- | --- |
| D01 | 数学建模初稿 | Mathematical Modeling | Done | https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/1 |
| D02 | 编程求解初稿 | Programming | Done | https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/2 |
| D03 | 论文初稿 | Academic Writing | Done | https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/3 |
| D04 | Skill 检查与配置 | Environment | Done | https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/4 |
| D05 | AGENTS.md 建立 | Environment | Done | https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/5 |
| D06 | 700 个原始文件完整性验证 | Data & Validation | Done | https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/6 |
| T01 | NumPy 及相关计算环境兼容性 | Environment | Blocked | https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/7 |
| T02 | BA2023 课程规范核验 | Requirements | To Do | https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/8 |
| T03 | 数学建模独立审核 | Mathematical Modeling | To Do | https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/9 |
| T04 | 编程与算法审核 | Programming | To Do | https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/10 |
| T05 | 数据及数值结果验证 | Data & Validation | To Do | https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/11 |
| T06 | 论文深度审核 | Academic Writing | To Do | https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/12 |
| T07 | 模型、代码、数据、结果、论文一致性检查 | Quality Assurance | To Do | https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/13 |
| T08 | 模拟 Rubrics 评分 | Quality Assurance | Blocked | https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/14 |
| T09 | 受控整改 | Quality Assurance | To Do | https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/15 |
| T10 | 最终独立审核 | Quality Assurance | To Do | https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/16 |
| T11 | Presentation 准备 | Presentation | To Do | https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/17 |
| T12 | 最终提交 | Final Submission | Blocked | https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project/issues/18 |


看板目标状态：To Do / In Progress / In Review / Done / Blocked。Category：Requirements / Environment / Mathematical Modeling / Programming / Data & Validation / Academic Writing / Quality Assurance / Presentation / Final Submission。

标签：P0-critical、P1-major、P2-minor、P3-enhancement、modeling、programming、data、paper、validation、documentation、blocked。实际创建状态以远程记录为准。

Task T01 是已核验的依赖兼容性缺口；其余待审核任务不预设模型/算法有缺陷。实际发现问题再用问题模板填写位置、证据、严重度、影响、修复和验证方案。负责人均待认领，不编造团队成员。

## 6. 持续同步与邀请

README 明确三角色如何查看/认领 Issue、创建分支、提交 PR、查看进度和讨论重大问题；AGENTS 明确每次重要审核/整改后更新 PROGRESS、Issue、Projects、证据和修改记录，保存 Commit 并在授权后推送；重大修改不自动合并，未验证审核不标 Done。

成员账号未提供，不邀请未知用户。提供准确用户名后，由仓库所有者在 Settings → Collaborators 邀请，按职责选择权限；继续保持 Private。

## 7. 人工确认与停止点

1. CLI 网页身份授权必须由用户本人完成；回传/权限检查不成功时保留阻碍，不伪称登录成功。
2. **首次推送前批准逐项上传清单及哈希**，确认团队成果共享权利、AGENTS 中本机路径及图片内容；候选论文初稿要单独确认作者元数据和版本。
3. 确认 BA2023 权威课程材料和成员账号；本阶段不自动补写课程要求，不邀请未知成员。
4. 原始文件暂未提交或上传；不开展正式业务审核。

完整性补充：Git 初始化前检查为 700/700 一致；配置结束快照发现根 .DS_Store 与历史哈希不同，其他 699 个原始文件仍字节一致。该系统元数据文件未被本轮命令主动写入，原因未独立核验；不恢复、不删除，已排除 Git。不能声称结束时仍为 700/700 一致。

凭证配置补充：为本仓库持久设置 gh Git 凭证助手的操作被自动审批拒绝，未执行。审批认为此前登录中“不认证 Git”的选择与此操作冲突；该选项实际由 Agent 为避免全局配置修改而选择。未绕过拒绝，已向用户请求仅限本仓库的明确授权。登录、仓库、Projects、Issues 均已成功；首次推送仍未执行。

最终配置确认：用户随后明确授权仅配置本仓库的 Git 凭证助手，重试已获准并成功验证；仅修改 .git/config，不修改全局 Git 配置，未推送。先前自动审批拒绝已解决。

远程最终只读核验：仓库 isPrivate=true、isEmpty=true，默认 main 尚无首个 Commit；Projects public=false，18 个条目，6 Done / 9 To Do / 3 Blocked；Issues 6 closed / 12 open。5 个状态及 9 个分类均已核对。

首次拟上传清单已整理为 90 项，约 4.62 MiB；精确路径、大小及哈希见 upload_manifest.json，所有文件的处置决定见 upload_inventory.csv。论文初稿、第三方附件、大结果文件及历史副本不在这 90 项中；未经确认不暂存、提交、打 Tag 或推送。

个人管理定位补充：保留 Private 仓库、Private Projects、18 项 Issues 与现有标签，不邀请成员、不增加复杂多人机制。研究质量提升完整规则见 AGENTS.md；基线存档前停在文件范围/存储权限确认点。

最新远程状态补充：main 出现 Initial commit `a4fdee6be9df0fb8c2f068adc13af990ca424f33`，仅含 README.md（144 字节）。本 Agent 未执行该提交或任何 Push；本地仍为无提交 main。仓库 Private，Projects Private，18 个条目（6 Done、9 To Do、3 Blocked）均重新核验。新基线确认后必须先读取/衔接最新远程历史，不 force push。初始化 README 的项目名称和描述已纳入本地拟上传 README。

## 2026-11-27 基线完成记录（覆盖上述历史待确认状态）

用户批准 95 项私有存储范围并要求去除无关 DOCX 账号元数据。英文论文的 Git blob 仅清除 WPS 数字账号、最后修改者标识与三个应用追踪属性，正文、批注、图片和作者显示署名不变；本地原件未改。45/64 MiB 原始 JSON 因 GitHub API 大请求受限，按批准的必要压缩方案无损封装为 `results/core_certificates_v9.zip`（7,010,274 字节），由 `review/baseline/restore_large_results.py` 在原路径恢复，隔离测试字节一致。

Git HTTPS 到 github.com:443 超时，改用已授权 GitHub API 上传并逐 blob 验证 SHA；远程树 `e4e7559edc25085437fa9f167a513e61890380d3` 与本地一致，95 文件共 53,190,995 字节。Private main 为 `9994d70a150c9e5cbe34a3ba726fbe7b4237c7a9`，父提交为原 README Initial commit `a4fdee6be9df0fb8c2f068adc13af990ca424f33`；annotated Tag `v0.1-first-draft` 对象 `7a8221a2b6b52828d8a99acc013b6b7b6889519e`。Projects 仍 Private，18 Issues，未邀请成员。Tag 表示未审核初稿。
