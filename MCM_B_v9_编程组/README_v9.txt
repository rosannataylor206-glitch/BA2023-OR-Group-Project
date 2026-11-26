MCM 2026 B v9 建模修订与复现交接
2026年10月28日

先读什么
建模手：MCM_B_v9_建模修订与独立验证说明.docx。
数学完整路径：proofs目录中的physics_v9、construction_v9、water_v9、joint_v9、cost_environment_v9与sensitivity_v9说明。
题目原文：evidence/2026_MCM_Problem_B.pdf。
v9是新版本，原v8保留；不要混用两版结果或运行入口。

编程手怎样运行
建议Python 3.10及以上，在解压后的MCM_B_v9目录中运行：
python -m pip install -r requirements.txt
python run_v9.py
也可从其他工作目录用run_v9.py的绝对路径启动。
仅核对已保存结果：python verify_v9.py。
完整运行依次重建物理、供水、联合策略、工程敏感性，再运行独立检查。
只有独立检查通过且数值源码在运行中未变化，才生成results/run_record.json成功记录。

各程序的作用
physics_v9.py：受限轨道、推进质量、相位与可拼接时间接口。
construction_v9.py：固定能力下的工期充分证书、建设货损、补发与有限期备用船。
water_v9.py：预存水与回收供水，R/E/ER路线及独立供水分区。
joint_v9.py：阶段顺序、关键设备身份、船队复用、仓储及完整特征账。
cost_environment_v9.py：参数化美元保守预算、运行排放代理与有限目录筛选。
sensitivity_v9.py：共同候选规则下的工程参数压力分析。
verify_v9.py：独立重建重要数学关系与跨阶段计算。
reference目录：为已证明的函数与回归检查保留的参考实现；不是本版主入口。

结果怎样找
results/policy_summary_v9.csv：先看这一张策略汇总表。
results/joint_v9.json：三路线基准、全部候选、成本与工期保证前沿、环境代理约束筛选。
results/phases_v9.json：候选引用的全部阶段证书；重复运输证书按内容哈希无损共享。
程序中用registry_v9.load_phase_registry(path)展开后按phase_id查找，避免反复存放相同长表。
results/sensitivity_v9.csv与sensitivity_v9.json：工程敏感性汇总与逐点方案。
results/sensitivity_phases_v9.json：敏感性方案引用的完整阶段证书。
results/physics_v9*与water_v9.json：物理接口及供水候选、证书和回放。
results/independent_v9.json：独立检查对象、数量、结果及范围。
results/run_record.json：运行环境、版本、时间与数值源码哈希。
若包内有portability_verification.json：记录新目录解压复算的交付检查。

数据与假设必须分清
官方题面提供人口、建设吨数、三港提升能力及未来火箭载荷范围，没有附可直接使用的未来运行观测数据集。
物理常数、概念研究和历史成本/排放标尺的来源及阅读位置在evidence和报告中。
250次/基地/年、设备模块性能、故障预算、储存损失及未来价格区间都是具名设计情景。
生成故障路径用于数学与程序核对，不是NASA观测，不能用其计算真实未来缺水概率。

模型结论的准确范围
主基准固定三个港口，每港每年179000吨总提升质量；未用扩容偷偷满足50年期限。
1亿吨一般建设物资单独保证送达。水模块、清水/原水舱、增量供电设备及初始水在晚期另运并计一次。
关键设备分同类清单运输，不能只凭总吨位便断言某种模块已经送达。
金额是所声明单价情景中的保守承诺预算，含可能毁损或最终未发出的已分配物资，不是实际未来报价或实际支出预测。
最低预算方案可能更慢，应结合预算与工期保证前沿选择，不存在未经说明的普遍最优推荐。
仓储与月面机器人接收能力采用首次到货前可用的外部服务合同；供应商的基础设施部署质量和时间不在本物理账本中。
长期备用船完好、维修更新、水质、核安全及真实设备性能仍须工程证据。维护费不等于已证明其物资保障。
环境量仅覆盖已列运行排放代理，不是完整生命周期环境评价；未知非CO2、核与生态影响没有被判定为零。
所有“最优”与“不可行”须保留有限策略目录、支持条件和充分证书口径。

修改与重建
改参数后必须重跑全部数值和独立检查；不要只改CSV或报告里的数字。
重建Word另需python-docx、pandoc、Noto Sans CJK SC与Latin Modern Math字体：
python build_report_v9.py
数值与文档检查通过后，可用python package_v9.py重建压缩包。
SHA256SUMS.json用于核对解压成员完整性，不是数学正确性的替代证据。
第三方论文不全文复制入包，请沿报告或evidence中的原始链接阅读。
