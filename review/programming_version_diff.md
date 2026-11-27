# 编程新旧版本差异与论文影响

基线：`v0.1-first-draft` 下 MCM_B_v9_编程组；新版候选：月球基地_编程组交付包_修订版/复跑程序，与当前 MCM_B_v9 对应源码逐字节一致。判定依据是源码/结果哈希、AST、内置说明和实际运行，不依赖文件名或mtime。

| 文件 | 变化 | Report影响 |
| --- | --- | --- |
| construction_v9.py | service_parameters/_route_plan：4/5/6/1常数命名；补闭式界及非MILP说明，默认数值不变 | 方法章解释保守取整与尾货储量，不能声称整数规划求解 |
| water_v9.py | _component/_aggregate/_validate/build_water_catalogue/run：包装比例移入WaterInputs，默认103.618/125未变；增加HARDWARE_ACCOUNTING | 明确包装比例是团队情景；100Mt通用材料之外另计水模块/舱/电力，改掉旧文字的内含/扣减矛盾 |
| joint_v9.py | 新construction_config_token；configure_inputs返回/更新token，build_policy记录token；run拒绝混合配置目录 | 说明参数一致性防护；策略ID公式仍未包含token，跨配置/跨平台不能只凭ID认同一方案 |
| run_v9.py | producer哈希列表加入share_lp_check_v9.py；执行阶段未加LP | 不把“源码列入清单”误写为“主流程执行LP” |
| share_lp_check_v9.py | 新增，两变量线性规划vs解析平衡份额 | 作为验证附录；理想/故障share_gap=0，solver status=0；只能证明该仿射分解的LP最优 |
| 其他15个PY | 与基线相同 | 无重构需要；保留原逻辑 |

新版共20个PY：1新增、4修改、15相同。模型证明 construction_v9.md 仅补代码常数映射；其余7证明字节相同；建模DOCX字节相同。默认参数及计算公式未发现实质性更改，硬件口径文字统一不等于新增物理建模。新增电网情景CSV与revision_table_comparison.json；四关键表与基线字节相同，新增包10图文件哈希均不同（不能据此认定图的数字变化）。

本机隔离复跑9命令全退出0，主运行67.660秒；LP0.461秒；绘图14.085秒。六CSV逐单元比较：数值在rel_tol=1e-9、abs_tol=1e-7内全部一致；字符串差异集中mission/policy ID，不能称跨平台字节复现。主结果表117行、故障表16行、联合筛选63行、自定义2行、电网各1行。

**运行批次差异**：MCM_B_v9 run_record完成15:34:49；编程交付包外层run_record完成14:25:04（均2026-11-27 +08:00）。生产源码哈希相同，但不是同一运行批次；包内“同一批源码”不证明“同一次运行”。引用整套外层交付表图及对应记录，或整套本机新复跑结果，不能拼接ID。保留两个批次且标记，不直接替换初稿数值。

补充实验建议仅针对缺口：179000吨单港/系统口径澄清；包装比例非默认值的边界/输入校验；配置token是否纳入跨运行引用；真实价格/运力范围。重大假设变化先确认。本轮没有改核心代码或原始结果。
