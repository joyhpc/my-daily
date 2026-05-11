各位同步一下 A38 / A57 + Agilex 5 的 DDR / LPDDR5 方案评估。

1. 原 DF108 DDR4 方案
    

原 DF108 最大线速 2.5Gbps/lane，摄像头端最大数据量约 80Gbps。

原方案使用 4 颗 DDR4，型号 H5AN4G6NBJR，单颗规格 4Gb / x16，总位宽 64bit，总容量 2GB，理论峰值带宽约 153.6Gbps。

2. 当前 Agilex 5 LPDDR5 方案
    

当前最大线速提升到 4Gbps/lane，摄像头端最大数据量约 128Gbps。

初步 LPDDR5 方案为 2 颗 LPDDR5，单颗规格 4GB / 32Gb，x32，总位宽 64bit，总容量 8GB。按主控侧约 3733MT/s 计算，理论峰值带宽约 239Gbps。

目前我这边正在确认 LPDDR5 寻样和价格。

3. 当前需要确认的问题
    

问题一：LPDDR5 容量和速率都有一定过配。

目前 x32 LPDDR5 中，2GB / 16Gb 颗粒基本停产，市场上更容易找到的是 4GB / 32Gb 规格，而且这类颗粒速率通常在 7500MT/s 以上。因此 LPDDR5 方案带宽是够的，但容量和颗粒规格偏过配。

问题二：Agilex 5 LPDDR5 控制器位宽有限制。

Agilex 5 单个 LPDDR5 控制器最高支持 32bit。如果要做 64bit 总位宽，需要使用双 LPDDR5 控制器。这个需要软件侧确认是否好实现。

@何海山(hehs) @吴锋(wuf) @Candy|罗奇军(luoqj) @路阳(luy) @邱永恒(qiuyh)

4. A57 + Agilex 5 场景下的两种方案
    

由于 LPDDR5 x16 单颗极不主流，同时 Agilex 5 的 HSIO bank 资源有限。一个 HSIO bank 最多约 7 组 MIPI，总共 4 个 HSIO bank。如果两个 bank 给 MIPI，两个 bank 给 DDR/LPDDR5，就会影响 MIPI 数量。

方案一：使用 LPDDR5

大约 14 组 MIPI，2 × 32bit LPDDR5，理论峰值带宽约 239Gbps。

优点是带宽裕量大，颗粒方向相对主流。缺点是总容量偏大，需要双 LPDDR5 控制器，且 MIPI 数量会减少到约 14 组。

方案二：使用 DDR5

大约 16 组 MIPI，16bit + 32bit DDR5，按 3600MT/s 计算，理论峰值带宽约 173Gbps。

优点是可以保留更多 MIPI 通道。缺点是带宽裕量小于 LPDDR5，且 16bit + 32bit DDR5 的实现方式还需要进一步确认。

5. 当前核心取舍
    

这个问题本质上是在权衡 MIPI 数量、HSIO bank 资源、内存带宽、颗粒可采购性和控制器实现复杂度。

请大家重点帮忙确认：

1）双 LPDDR5 控制器软件侧是否好实现；  
2）A57 场景下是否必须保留 16 组 MIPI；  
3）DDR5 约 173Gbps 理论带宽是否够用；  
4）LPDDR5 8GB 容量过配是否可以接受。