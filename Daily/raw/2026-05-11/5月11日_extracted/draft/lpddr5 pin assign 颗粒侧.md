只看颗粒侧，用这几个文件：

  - lpddr5_315_DR_DS_U0_Bank2B_pin_net.tsv
    U0 颗粒侧 315-ball DS/DR ball -> net。
  - lpddr5_315_DR_DS_U1_Bank3A_pin_net.tsv
    U1 颗粒侧 315-ball DS/DR ball -> net。
  - orcad_hsio2b_lpddr5_x32_micron315b_side_aliases.csv
    更偏 OrCAD 符号用的颗粒侧 alias 表。
  - lpddr5_memory_pin_net_by_package_orcad_order.xlsx
    颗粒侧按 package / OrCAD 顺序整理的表，最适合画符号时用。

  颗粒侧重点：

  - A 通道 DQ0-DQ15：DQ*_A，ball 如 D1/C2/.../F11
  - B 通道 DQ0-DQ15：接系统 DQ16-DQ31，颗粒名是 DQ*_B
  - CA/CK/WCK/CS 是 A/B 共用 T-line，表里同一个 net 会对应 A/B 两个 ball
  - RESET_N 是单独 ball：H1
  - ZQ_A 是颗粒本地 240R 到 VDDQ，不接 FPGA
  - FPGA 的 RZQ、REFCLK 不属于 LPDDR5 颗粒侧，不要画到颗粒符号里

  你画 315-ball 颗粒符号时，优先用 lpddr5_memory_pin_net_by_package_orcad_order.xlsx。如果只要文本核对，用两个 lpddr5_315_DR_DS_U*_pin_net.tsv。





