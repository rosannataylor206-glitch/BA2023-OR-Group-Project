# 02 编程与算法审核（初稿基线 9994d70）

状态：**核心数值链在隔离副本运行成功；严格复现与外部有效性仍有限制**。使用项目 `.venv`：Python 3.12.7、NumPy 2.3.5、SciPy 1.17.0、Matplotlib 3.10.8，`pip check` 为 0。仅从 PyPI 官方索引安装二进制轮子，未改全局环境。隔离目录 `review/runs/2026-11-27-v9-replay/`，原始候选代码/结果未运行或覆盖。

实际命令：`.venv/bin/python review/runs/2026-11-27-v9-replay/MCM_B_v9_编程组/run_v9.py`，退出码 **0**，80.846 秒；逐阶段运行 physics、water、joint、sensitivity、verify，日志 SHA-256 `099af3ce8ca8b9e3795139ad321ced75f4c163446096234348d722e1606b2c06`，见隔离记录 `execution.json`。`run_v9.py:40-43` 会删旧 run record，故隔离是必要的。

| ID / 级别 / 状态 | 位置与证据 | 影响 | 建议与验证 |
| --- | --- | --- | --- |
| C01 P2 Minor，已验证 | 78 份复制输入中 8 个输出文件复跑后 SHA 改变；`physics_v9.json.checks.max_ODE_endpoint_position_error_km` 从 1.752929224562015e-06 变为 1.732251330525823e-06；`joint_v9.json` 约 5.7 万项字符串 ID 差异，主数值未见实质差异。 | 结果数值基本可复现，但字节/ID 级复现失败；跨包引用必须整批生成。 | 把物理浮点输出与策略标识分离或规范化 ID 输入；固定平台/容差后双次复跑，比较业务指标与 ID 稳定性。此项属于整改建议，未改核心代码。 |
| C02 P2 Minor，已验证 | `verify_v9.py:597-598` 在本包写 `independent_v9.json`，复跑自带 `all_implemented_checks_pass=true`；其测试仍由同一项目代码实现。 | 证明声明支持内的程序自检通过，不是外部物理/价格验证。 | 保留自检证据，并由与实现不同的算式/小规模案例交叉核查；本轮独立算术脚本 19/19 通过，见 03。 |
| C03 P2 Minor，已确认依赖 | `package_v9.py` 依赖本地 `evidence/2026_MCM_Problem_B.pdf`，因第三方存储权未入 Git；仓库中两份大 JSON 要先从 `core_certificates_v9.zip` 恢复。 | 新检出仓库不能跳过恢复步骤直接运行全部读取脚本；打包流程另需合法取得题面 PDF。 | 执行 `python3 review/baseline/restore_large_results.py`，已在隔离目录证明恢复字节等于原始 JSON；打包功能单独标记未运行。 |
| C04 P1 Major，尚未验证 | `run_v9.py` 自报通过的 625 小队列案例和 13,728 策略筛选仍在声明的抽象模型内；没有教师指定模型、实际发射可靠性或外部价格输入。 | 不能提升为现实最优性或工程认证。 | 课程题目取得后补模型—实现逐约束映射和原始参数来源审计；关键保障约束做外部独立小实例/边界反例。 |

检查边界：未运行 `build_report_v9.py`（需要 Pandoc/字体）、`package_v9.py`（缺仓库内题面 PDF）、原目录 `run_v9.py`，未将这些标为通过。`review/checks/independent_checks.py` 不导入业务模块，只做跨材料算术核对。
