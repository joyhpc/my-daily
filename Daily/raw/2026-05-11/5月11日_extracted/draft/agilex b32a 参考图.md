 不是都一个芯片，应该分三层看：

  | 资料 | 实际器件 | 是否和你目标同芯片 | 主要用途 |
  |---|---|---:|---|
  | 你的目标 | A5ED052AB32AE2V | 是目标器件 | 最终设计对象 |
  | Altera 官方 065B SOM 原理图 | A5ED065B B32A | 不是 exact part，但同封装 B32A | 最高优先级参考：SDM、PMBus、VCC/SmartVID、启动配置 |
  | KEIm A5ESOM Rev1.10 | A5ED065BB32AE5SR0，B32A / BGA1591 | 不是 exact part，但同封装 B32A | 很有价值的实际 SOM 参考 |
  | Sulfur Type-A | carrier board，没有直接放 FPGA | 不是 FPGA 原理图 | 只参考 SOM 供电入口、PMBus 暴露、连接器使用 |

  关键点：

  A5ED052A 和 A5ED065B 不是同一个 die 规模。065B 资源更多，但它们都是 Agilex 5E Group B，并且都是 B32A 封装。所以 封装固定 pin、SDM/JTAG/配置、电源 ball、VCC/VCCP/SmartVID 这
  类连接参考价值很高。

  但不能说“完全一样”，因为：

  - 052A 和 065B 资源规模不同，某些 IO/硬核资源/NC/RFU 可能不同。
  - 官方 SOM、KEIm SOM、carrier 的板级架构不同。
  - VCC/SmartVID regulator 可以不一样：官方用 LTC7883 + LTC7050，KEIm 用 LTC7883 + NCP302035。
  - PMBus 主控关系不同：官方更像 SDM/板级 PMBus 体系，KEIm 是 SOM 暴露给 carrier，同时保留 SDM 路径。
  - DDR、eMMC、QSPI、时钟、复位、电源时序这些是板级方案，不是“同芯片就完全一样”。

  所以正确使用方式是：

  1. pin/ball 以 A5ED052A B32A 官方 pinout 为准。
  2. 原理图连接风格优先参考 Altera 官方 065B SOM。
  3. KEIm Rev1.10 作为同封装实际产品交叉验证，参考价值高。
  4. Sulfur Type-A 只看 carrier/SOM 连接和 PMBus 暴露，不拿它推 FPGA 内部电源方案。


