LPDDR5 pin assign / pin placement 规范在这个文件：

  External Memory Interfaces (EMIF) IP User Guide Agilex™ 5 FPGAs and SoCs 817467_D842785.pdf
  (https://drive.google.com/file/d/1xbcT4cdCmZ0dgqwX9zzrEvWQ5DXGSVPA/view)

  重点位置：

  - Chapter 9. Agilex 5 FPGA EMIF IP - LPDDR5 Support
  - 9.2.3 Pin Guidelines for Agilex 5 FPGA EMIF IP，PDF 第 237 页左右
  - 9.2.4 Pin Placements for Agilex 5 FPGA LPDDR5 EMIF IP，PDF 第 240 页左右
  - 9.2.4.1 Address and Command Pin Placement for LPDDR5
  - 9.2.4.2 LPDDR5 Data Width Mapping
  - 9.2.4.3 LPDDR5 Byte Lane Swapping

  官方在线版本也在这里：

  - LPDDR5 Support 目录

  (https://docs.altera.com/r/docs/817467/25.3.1/external-memory-interfaces-emif-ip-user-guide-agilextm-5-fpgas-and-socs/agilextm-5-fpga-emif-ip-lpddr5-support)
  - Address and Command Pin Placement for LPDDR5

  (https://docs.altera.com/r/docs/817467/25.3.1/external-memory-interfaces-emif-ip-user-guide-agilextm-5-fpgas-and-socs/address-and-command-pin-placement-for-lpddr5?contentId=aMXZgx5RXexgoj~e2joi7A)
  - LPDDR5 Data Width Mapping

  (https://docs.altera.com/r/docs/817467/25.3.1/external-memory-interfaces-emif-ip-user-guide-agilextm-5-fpgas-and-socs/lpddr5-data-width-mapping?contentId=kZhHwBujCfglRh7hbL_OyA)

  我也核了一下：文件夹里的 altera-pbc-b32a-a5e.xlsx 只是 package ball coordinate，不是 LPDDR5 pin assignment；开发板 schematic/user guide 主要是 LPDDR4，不
  是你要的 LPDDR5 规范。

