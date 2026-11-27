# 共享变量字典

定义作用域、类型、单位和来源，随后逐公式核对。首先检查候选符号是否已定义，跨章节保持同义。单位统一为列，比例声明用 [0,1] 或 %，给定的参数提供来源和取值区间，拟合参数的估计量加帽。英文论文用 booktabs 三线表，符号左对齐，名称和说明左对齐，单位与范围独立。时间单位与基期写在表注或数据章节。

## 统计分析

| Symbol | Type / scope | Definition | Unit / shape | First use |
|---|---|---|---|---|
| i | Index / global | Observation or sampling unit | 1,…,n | Data |
| X | Matrix / regression | Design matrix | n×p, column-specific units | Regression |
| yᵢ | Response / global | Measured response at unit i | [unit] | Data |
| eᵢ | Residual / diagnostics | yᵢ − ŷᵢ | [unit] | Validation |

## 数学优化

| Symbol | Role | Definition | Unit / domain | Source |
|---|---|---|---|---|
| J | Set | Feasible resources | Finite set | Inventory |
| xⱼ | Decision | Resource j allocation | Integer [unit] | Program |
| bⱼ | Parameter | Resource j limit | [unit] | Capacity |
| λ | Dual variable | Price of a capacity constraint | [cost/unit] | Optimum conditions |

## 多模型研究

| Symbol | Stage | Definition | Unit / shape | Consumed by |
|---|---|---|---|---|
| zₜ | Feature | Information available at decision time t | [shape] | Prediction |
| Dₜ₊₁⁽ˢ⁾ | Scenario | Demand draw for future period | [unit] | Optimization |
| pₛ | Scenario parameter | Probability weight for scenario s | [0,1], sums to 1 | Cost aggregation |
| qₜ | Decision | Order placed before demand is observed | [unit] | Held-out evaluation |
| L(q,D) | Outcome | Over- and under-stock cost | [currency] | Comparison |

同一符号跨模型复用仅限量纲和定义一致。不同时间粒度或状态类型用下标/作用域明确。主表保留文中反复使用的量，局部中间量紧邻公式解释。
