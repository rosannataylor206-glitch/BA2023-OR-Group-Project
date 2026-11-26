# Phase 1 最终上传清单：个人研究初稿基线

状态：**2026-11-27 用户已批准 95 项存储范围**。本文件记录获批范围；实际提交、推送与远程核验另见 `review/00_github_setup.md`。当前 Private 仓库、Private Projects、18 项 Issues 和既有标签保留，不邀请任何成员；远程 main 已有仅含 README 的 Initial commit（a4fdee6be9df0fb8c2f068adc13af990ca424f33）；现已在本地以该 Initial commit 为父节点建立基线 Commit 与 Tag；远程核验结果以 `review/00_github_setup.md` 后续记录为准，不 force push；初始化 README 名称和描述已纳入上传版 README。

已逐文件核对 SHA-256 并在本地保存 `v0.1-first-draft`。基线记录的是未审核初稿，不是经过验证的稳定结论。基线完成后可按用户已授权流程连续开展 Phase 2–5；正式修改模型、核心代码和论文前仍须提交综合审核报告和整改方案供用户确认。

## 相比旧 90 项的变化

- 保留其中 85 项，移除 5 份重复灰度 QA 预览（仅从拟上传集移除，本地文件不动）。
- 新增英文论文 DOCX、模型 DOCX、敏感性 JSON、敏感性阶段证书 JSON；联合策略 JSON 与主阶段证书 JSON 以无损 ZIP 存储，并附独立恢复脚本。
- 新增 4 项基线记录：coverage.md、skill_environment_summary.md、core_index.json、本清单。
- 最终 **95 项**；源代码与既有数据路径不变；两份大型 JSON 从 ZIP 恢复到原路径后供现有代码读取。英文论文上传副本仅去除无关 WPS 账号与应用追踪元数据，本地原件保持不变。

## 存储方式与完整性范围

原始四个大型 JSON 中，`sensitivity_v9.json` 与 `sensitivity_phases_v9.json` 直接纳入 Git；`joint_v9.json` 与 `phases_v9.json` 无损压缩为 `core_certificates_v9.zip`（约 6.69 MiB），并提供 `review/baseline/restore_large_results.py` 在原路径恢复和校验原始 SHA-256。压缩只因 GitHub API 对较大 blob 的请求拒绝，原始文件留在本地未改；无需 Git LFS，核心计算证据没有丢失。原始最大单文件 61.59 MiB，95 项上传内容均低于 GitHub 100 MiB 限制。后续若频繁重算导致仓库增长，再经批准选择新存储方案，不重写本基线历史。规则来源：[GitHub 官方大文件说明](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github)。

95 项覆盖：21 个源代码文件、8 份 proofs、8 份来源/假设 JSON、21 份原始结果对应的远程文件/无损存档、10 个彩色图/矢量源、两份可编辑 DOCX、已有证据/AI 使用记录和必要管理文件。具体数量按下表及 SHA-256 清单为准。静态覆盖说明见 coverage.md；没有以清单完整代替真实运行验证。

## 排除与已知限制

- 其他历史 v6/v9 副本、output 压缩交接、另一题 XLSX/课程混合文件、无关 Q1 实验不上传；不删除/移动这些文件。
- 第三方题目 PDF、教材/课件/文章全文、许可未核验的字体或 Skills 不上传。公开链接或来源元数据不等于第三方全文的存储授权。
- `.tools/`（含 gh 配置）、环境、缓存、系统元数据、Office 锁文件、原始隐私扫描与本机路径密集的环境明细不上传；以最新 .gitignore 和逐项清单共同控制。
- 论文 DOCX 有可编辑正文/公式，但未找到对应英文报告的独立 LaTeX/Markdown 构建源；不声称模型说明生成脚本能重建该英文论文。
- 打包脚本要求本地原始题目 PDF；它不在远程范围，故完整打包仍有外部依赖。建模 DOCX 构建所需 Pandoc/字体及数值环境尚未就绪。
- 原始 700 项历史哈希中仅 `.DS_Store` 已有漂移，其余 699 项不变。此次没有修改模型、数据、代码、结果和论文。

## 必须由用户确认的存储权限

1. 用户已批准 95 项在本人 Private 仓库存储，并授权必要的无损压缩。研究成果、参数、结果、图表与来源索引只作个人存档；个人管理不改变原作者权利。
2. 用户已批准两份 DOCX 的存储。建模说明按原样存储；英文论文上传副本仅移除 `docProps/core.xml` 中的 WPS 最后修改者账号、`word/people.xml` 中的 WPS 数字 userId 以及 `docProps/custom.xml` 中三个应用追踪属性。正文、批注、图片和作者显示署名逐 ZIP part 校验保持原值；本地原件不变。
3. `AGENTS.md` 保留本机路径，部分历史验证记录也有工具/角色信息。正则扫描未发现其覆盖的常见凭证模式，不保证 OCR/二进制隐藏内容无敏感信息；确认前仍不上传。
4. 此批准仅针对下列研究内容及其无损压缩/元数据脱敏版本；英文论文上传副本哈希与本地原件不同，差异仅为上述三项元数据部分。后续新文件或共享范围变化另行说明，不因批准私有库就自动允许第三方全文、未核实数据或凭证入库。

本轮用户已批准此范围，并要求去除无关个人敏感元数据。

## 逐项清单

SHA-256 和精确字节数另存本地 `review/github_setup/upload_manifest.json`。两份被压缩 JSON 的原始 SHA-256 写在恢复脚本；全目录处置在 `upload_inventory.csv`；approval 已获确认。此 Markdown 的正文不嵌入自身哈希，避免自引用。

本方案共 95 项；上传副本总大小 53,190,995 字节（约 50.73 MiB）。

| 序号 | 仓库路径 | MiB | 相对旧清单 |
| --- | --- | ---: | --- |
| 1 | `.github/ISSUE_TEMPLATE/problem.yml` | 0.0013 | 保留 |
| 2 | `.github/ISSUE_TEMPLATE/task.yml` | 0.0007 | 保留 |
| 3 | `.github/PULL_REQUEST_TEMPLATE.md` | 0.0006 | 保留 |
| 4 | `.gitignore` | 0.0014 | 保留 |
| 5 | `AGENTS.md` | 0.0211 | 保留 |
| 6 | `CHANGELOG.md` | 0.0015 | 保留 |
| 7 | `CONTRIBUTING.md` | 0.0040 | 保留 |
| 8 | `MCM_B_v9_编程组/MCM_B_v9_建模修订与独立验证说明.docx` | 0.2128 | 新增/替换 |
| 9 | `MCM_B_v9_编程组/README_v9.txt` | 0.0045 | 保留 |
| 10 | `MCM_B_v9_编程组/ai_ledger/ledger.json` | 0.0080 | 保留 |
| 11 | `MCM_B_v9_编程组/build_report_v9.py` | 0.0466 | 保留 |
| 12 | `MCM_B_v9_编程组/construction_v9.py` | 0.0217 | 保留 |
| 13 | `MCM_B_v9_编程组/cost_environment_v9.py` | 0.0156 | 保留 |
| 14 | `MCM_B_v9_编程组/evidence/assumption_ledger_v7.json` | 0.0033 | 保留 |
| 15 | `MCM_B_v9_编程组/evidence/cost_environment_v9_sources.json` | 0.0044 | 保留 |
| 16 | `MCM_B_v9_编程组/evidence/fault_math_sources.json` | 0.0167 | 保留 |
| 17 | `MCM_B_v9_编程组/evidence/physics_sources.json` | 0.0184 | 保留 |
| 18 | `MCM_B_v9_编程组/evidence/physics_v8_sources.json` | 0.0057 | 保留 |
| 19 | `MCM_B_v9_编程组/evidence/power_v9_sources.json` | 0.0009 | 保留 |
| 20 | `MCM_B_v9_编程组/evidence/system_cost_v8_sources.json` | 0.0015 | 保留 |
| 21 | `MCM_B_v9_编程组/evidence/water_sources.json` | 0.0147 | 保留 |
| 22 | `MCM_B_v9_编程组/evidence_chain/P2_技术复核.json` | 0.0012 | 保留 |
| 23 | `MCM_B_v9_编程组/evidence_chain/P2_补充分析复核.json` | 0.0008 | 保留 |
| 24 | `MCM_B_v9_编程组/evidence_chain/evidence.json` | 0.0545 | 保留 |
| 25 | `MCM_B_v9_编程组/fault_attribution_v9.py` | 0.0052 | 保留 |
| 26 | `MCM_B_v9_编程组/figures/process_q3_water_preposition.png` | 0.0794 | 保留 |
| 27 | `MCM_B_v9_编程组/figures/process_q3_water_preposition.svg` | 0.0122 | 保留 |
| 28 | `MCM_B_v9_编程组/figures/raw_q2_declared_fault_budgets.png` | 0.0568 | 保留 |
| 29 | `MCM_B_v9_编程组/figures/raw_q2_declared_fault_budgets.svg` | 0.0086 | 保留 |
| 30 | `MCM_B_v9_编程组/figures/result_q1_construction_bounds.png` | 0.0671 | 保留 |
| 31 | `MCM_B_v9_编程组/figures/result_q1_construction_bounds.svg` | 0.0108 | 保留 |
| 32 | `MCM_B_v9_编程组/figures/result_q4_emissions_budget_frontier.png` | 0.0836 | 保留 |
| 33 | `MCM_B_v9_编程组/figures/result_q4_emissions_budget_frontier.svg` | 0.3137 | 保留 |
| 34 | `MCM_B_v9_编程组/figures/result_q5_habitation_budget_frontier.png` | 0.0910 | 保留 |
| 35 | `MCM_B_v9_编程组/figures/result_q5_habitation_budget_frontier.svg` | 0.3142 | 保留 |
| 36 | `MCM_B_v9_编程组/joint_screening_v9.py` | 0.0054 | 保留 |
| 37 | `MCM_B_v9_编程组/joint_v9.py` | 0.0268 | 保留 |
| 38 | `MCM_B_v9_编程组/package_v9.py` | 0.0057 | 保留 |
| 39 | `MCM_B_v9_编程组/phase_audit_v9.py` | 0.0171 | 保留 |
| 40 | `MCM_B_v9_编程组/physics_v9.py` | 0.0175 | 保留 |
| 41 | `MCM_B_v9_编程组/plot_handoff.py` | 0.0066 | 保留 |
| 42 | `MCM_B_v9_编程组/programming_handoff.py` | 0.0138 | 保留 |
| 43 | `MCM_B_v9_编程组/proofs/audit_scope_v9.md` | 0.0053 | 保留 |
| 44 | `MCM_B_v9_编程组/proofs/construction_v9.md` | 0.0088 | 保留 |
| 45 | `MCM_B_v9_编程组/proofs/cost_environment_v9.md` | 0.0064 | 保留 |
| 46 | `MCM_B_v9_编程组/proofs/joint_v9.md` | 0.0092 | 保留 |
| 47 | `MCM_B_v9_编程组/proofs/physics_v9.md` | 0.0087 | 保留 |
| 48 | `MCM_B_v9_编程组/proofs/sensitivity_v9.md` | 0.0039 | 保留 |
| 49 | `MCM_B_v9_编程组/proofs/water_v8_reference.md` | 0.0106 | 保留 |
| 50 | `MCM_B_v9_编程组/proofs/water_v9.md` | 0.0103 | 保留 |
| 51 | `MCM_B_v9_编程组/reference/__init__.py` | 0.0000 | 保留 |
| 52 | `MCM_B_v9_编程组/reference/physics_v8.py` | 0.0221 | 保留 |
| 53 | `MCM_B_v9_编程组/reference/water_v8.py` | 0.0276 | 保留 |
| 54 | `MCM_B_v9_编程组/registry_v9.py` | 0.0017 | 保留 |
| 55 | `MCM_B_v9_编程组/requirements.txt` | 0.0000 | 保留 |
| 56 | `MCM_B_v9_编程组/results/archive_comparison.json` | 0.0043 | 保留 |
| 57 | `MCM_B_v9_编程组/results/core_certificates_v9.zip` | 6.6855 | 新增/替换 |
| 58 | `MCM_B_v9_编程组/results/independent_v9.json` | 0.0034 | 保留 |
| 59 | `MCM_B_v9_编程组/results/physics_v9.json` | 0.1535 | 保留 |
| 60 | `MCM_B_v9_编程组/results/physics_v9_catalogue.csv` | 0.0046 | 保留 |
| 61 | `MCM_B_v9_编程组/results/policy_summary_v9.csv` | 1.9283 | 保留 |
| 62 | `MCM_B_v9_编程组/results/programming_smoke.json` | 0.0012 | 保留 |
| 63 | `MCM_B_v9_编程组/results/programming_table_profile.json` | 0.0090 | 保留 |
| 64 | `MCM_B_v9_编程组/results/run_record.json` | 0.0030 | 保留 |
| 65 | `MCM_B_v9_编程组/results/sensitivity_phases_v9.json` | 12.1760 | 新增/替换 |
| 66 | `MCM_B_v9_编程组/results/sensitivity_v9.csv` | 0.0161 | 保留 |
| 67 | `MCM_B_v9_编程组/results/sensitivity_v9.json` | 25.9001 | 新增/替换 |
| 68 | `MCM_B_v9_编程组/results/supplemental/q2_fault_attribution.csv` | 0.0040 | 保留 |
| 69 | `MCM_B_v9_编程组/results/supplemental/q4_q5_joint_screening.csv` | 0.0128 | 保留 |
| 70 | `MCM_B_v9_编程组/results/supplemental/q4_q5_joint_screening_custom.csv` | 0.0008 | 保留 |
| 71 | `MCM_B_v9_编程组/results/supplemental/verification.json` | 0.0005 | 保留 |
| 72 | `MCM_B_v9_编程组/results/supplemental/复现清单.json` | 0.0047 | 保留 |
| 73 | `MCM_B_v9_编程组/results/water_v9.json` | 0.4434 | 保留 |
| 74 | `MCM_B_v9_编程组/results/复现清单.json` | 0.0099 | 保留 |
| 75 | `MCM_B_v9_编程组/results/论文组结果表.csv` | 0.0158 | 保留 |
| 76 | `MCM_B_v9_编程组/run_v9.py` | 0.0030 | 保留 |
| 77 | `MCM_B_v9_编程组/sensitivity_v9.py` | 0.0124 | 保留 |
| 78 | `MCM_B_v9_编程组/utils/plot_style.py` | 0.0164 | 保留 |
| 79 | `MCM_B_v9_编程组/utils/supplemental_io.py` | 0.0015 | 保留 |
| 80 | `MCM_B_v9_编程组/verify_v9.py` | 0.0358 | 保留 |
| 81 | `MCM_B_v9_编程组/water_v9.py` | 0.0273 | 保留 |
| 82 | `MCM_B_v9_编程组/使用指南.md` | 0.0061 | 保留 |
| 83 | `MCM_B_v9_编程组/报告核心代码摘录.md` | 0.0057 | 保留 |
| 84 | `MCM_B_v9_编程组/编程交接.md` | 0.0074 | 保留 |
| 85 | `PROGRESS.md` | 0.0066 | 保留 |
| 86 | `README.md` | 0.0038 | 保留 |
| 87 | `report.1docx.docx` | 1.4538 | 新增/替换 |
| 88 | `review/00_github_setup.md` | 0.0129 | 保留 |
| 89 | `review/baseline/core_index.json` | 0.0139 | 新增/替换 |
| 90 | `review/baseline/coverage.md` | 0.0046 | 新增/替换 |
| 91 | `review/baseline/phase1_upload_scope.md` | 0.0120 | 新增/替换 |
| 92 | `review/baseline/restore_large_results.py` | 0.0019 | 新增/替换 |
| 93 | `review/baseline/skill_environment_summary.md` | 0.0012 | 新增/替换 |
| 94 | `review/github_setup/tasks.json` | 0.0068 | 保留 |
| 95 | `review/github_setup/upload_preflight.py` | 0.0043 | 保留 |
