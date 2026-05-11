

| 功能               | A5ED065B B32A / Agilex 5    |                 Ball | Xilinx XCKU 对应            | 是否一一对应                |
| ---------------- | --------------------------- | -------------------: | ------------------------- | --------------------- |
| JTAG clock       | TCK                         |                CA109 | TCK                       | 是                     |
| JTAG mode        | TMS                         |                CA112 | TMS                       | 是                     |
| JTAG data in     | TDI                         |                BW112 | TDI                       | 是                     |
| JTAG data out    | TDO                         |                BW109 | TDO                       | 是                     |
| 重新配置控制           | nCONFIG                     |                 BU99 | PROGRAM_B                 | 功能等价                  |
| 配置状态/错误          | nSTATUS                     |                 BW99 | INIT_B                    | 近似等价                  |
| 配置完成             | CONF_DONE on SDM_IO16       |                BP102 | DONE                      | 近似等价                  |
| 用户模式完成           | INIT_DONE on SDM_IO0        |                 CA99 | 无完全等价 dedicated pin       | 不完全对应                 |
| 配置模式选择           | MSEL[2:0]                   |      复用在 SDM_IO5/7/9 | M[2:0]                    | 功能等价，但物理实现不同          |
| SPI/QSPI 时钟      | AS_CLK on SDM_IO2           |                 BK99 | CCLK                      | 功能等价                  |
| QSPI IO0         | AS_DATA0 on SDM_IO4         |                 BH99 | D00_MOSI                  | 功能等价                  |
| QSPI IO1         | AS_DATA1 on SDM_IO1         |                BK102 | D01_DIN                   | 功能等价                  |
| QSPI IO2         | AS_DATA2 on SDM_IO3         |                 CH99 | D02                       | 功能等价                  |
| QSPI IO3         | AS_DATA3 on SDM_IO6         |                CF102 | D03                       | 功能等价                  |
| Flash CS0        | AS_nCSO0 / MSEL0 on SDM_IO5 |                CF112 | FCS_B                     | 功能等价，但 Intel 复用 MSEL0 |
| Flash CS1/2/3    | AS_nCSO1/2/3                | BM102 / BM99 / CC102 | Xilinx x8 / 多 Flash 相关 CS | 不严格一一对应               |
| Flash reset      | AS_nRST on SDM_IO15         |                CA102 | 无直接 dedicated 等价          | Intel 特有              |
| 外部配置参考时钟         | OSC_CLK_1                   |                BR102 | EMCCLK                    | 近似，不完全等价              |
| SDM 参考电阻         | RREF_SDM                    |                CL103 | 无                         | Intel 特有              |
| SmartVID / PMBus | PWRMGT_SCL / PWRMGT_SDA     |         CF109 / CF99 | 无 XCKU dedicated 等价       | Intel 特有              |
| 配置 bank 电压选择     | 无同类 pin                     |                    - | CFGBVS                    | Xilinx 特有             |
| 配置期间上拉控制         | 无同类 pin                     |                    - | PUDC_B                    | Xilinx 特有             |
| 电池密钥备份           | 无同类 pin                     |                    - | VBATT                     | Xilinx 特有             |