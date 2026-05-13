A5EC052A_B32 / Agilex 5 E-Series:

HSIO bank:
  VCCIO_PIO = 1.0 / 1.05 / 1.1 / 1.2 / 1.3 V

HVIO bank:
  VCCIO_HVIO = 1.8 / 2.5 / 3.3 V

SDM I/O:
  VCCIO_SDM = 1.8 V

HPS I/O:
  A5EC = No HPS，不适用



不是不确定，是需要支持CMOS1.2V和1.8V，这里由外部接入的设备决定。系统会根据接入设备信息进行VDDIO选择。重点是A5E的bank电压不支持这样调
外部io特别多，不能做HSIO和HVIO的切换，这样会远远不够用。
也不能用0Ω / DNP 做装配选择，不符合自动化。
那认为用电平转换芯片应该是最好的方案，但是方向性怎么办。收发控制这里。以及其它要考虑的问题有哪些


