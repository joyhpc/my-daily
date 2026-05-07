# Tomorrow Boot Packet - 2026-05-08

## 明日主线

- A38 / DF108 Agilex 5 第一版原理图继续推进，但优先级不是继续画所有页，而是锁定高速接口 pin planning 前置条件和资源矩阵。

## 背景

- 当前 A38 主控板从 KU040 迁移到 Agilex 5，第一版目标是快速改版，不是最终 sign-off。
- MIPI 方向已确认：去掉 HS/LP switch 和 buffer，连接器后直连 Agilex 5 MIPI-capable HSIO bank。
- DDR4 改 LPDDR5，当前按两组 LPDDR5_CTRL0_X32 / LPDDR5_CTRL1_X32 规划，每组对应一个 LPDDR5 主控和一个 x32 颗粒。
- FAE 建议 LPDDR5、MIPI D-PHY、QSFP 不要由硬件侧单独手工定 pin，需要逻辑侧先建 Quartus 最小工程做组合验证。

## 当前状态

- A38 原理图框架：60%。
- MIPI：90%，缺 FPGA 仿真/验证。
- QSFP：已完成。
- LPDDR5：未启动，等待 Quartus EMIF + Pin Planner/Fitter 证据。
- GPIO：方案未定，当前 GPIO 过多，需要判断扩展 FPGA 还是简单 GPIO 扩展芯片。
- 电源树、时钟、复位：未启动。
- LPDDR5 采购需求已形成，状态是等待采购反馈。
- A57 后两通道 eDP 问题：记录显示 AUX 通信和链路训练正常，主攻方向转到 eDP 解码芯片配置、上电时序、IIC 参数下发和物理输出。

## 第一动作

- 建立 A38 资源矩阵初版 CSV，路径建议：
  `revisions/rev-20260506-df108-ku040-to-a5ed052ab32ae2v/02_design_evidence/a5ec052a_b32a_resource_allocation_matrix_20260507.csv`

字段使用：
`domain,group,signal_group,source,connector_or_device_pin,target_bank,target_pin_or_lane,rate_or_voltage,dependency,status,evidence_required,schematic_page,notes`

第一版只填已知事实和待确认项，未验证的 pin、bank、lane、refclk、RZQ、电压域统一标为 `pending_quartus`、`pending_pin_planner`、`pending_datasheet` 或 `pending_reference_design`。

## 注意事项

- 不要把 A5EC052A B32A / A5ED052AB32AE2V 命名差异当成已解决结论；先标 `naming_cleanup`。
- 不要把 MIPI 当普通 LVDS 差分 IO 处理。
- 不要沿用 KU040 Power Tree 的 rail、sequencing、monitor、SmartVID/PMBus、current limit、inrush、MOSFET SOA 等参数。
- 不要在 Quartus / Pin Planner / 官方 datasheet / reference design 未确认前冻结 LPDDR5 pin list。
- `Issue4.md` 是排查同步文案，是否实际发送原文未明确；记录时不要写成“已发送”。

## 不要重复踩的坑

- 先凭封装页或经验画 pin，再等逻辑侧发现 Fitter 不过。
- 把未发送详细版、最终发送简版、可复制发送文案混成同一种事实。
- 把第一版快速原理图当作 sign-off 图。
- 把 A38、A57、workspace skills、wiki sync 全部并行推进，导致明日主线发散。

## 可以交给 AI / agent 的部分

- 生成资源矩阵 CSV 初版，所有未证实字段保留 `pending_*`。
- 把 LPDDR5 / MIPI / QSFP 硬件侧输入参数整理成给逻辑侧的 checklist。
- 整理 Power Tree 页面 checklist：rail list、电流估算、sequencing group、PG/reset、test point/sense/PMBus。
- 把 A57 issue 排查计划整理成实验矩阵和记录模板。
- 把 daily notes 中的 draft / sent / confirmed 状态自动审核出来。

## 必须由我亲自判断的部分

- A38 高速接口 pin planning 的逻辑侧 owner 和交付时间。
- GPIO 过多时选扩展 FPGA 还是 GPIO 扩展芯片。
- LPDDR5 颗粒最终料号、供应风险和采购反馈。
- A57 实测结论是否足以关闭 FPGA 接收逻辑方向，转为解码芯片配置/物理输出方向。
- A5EC/A5ED 最终器件命名和正式设计证据。
