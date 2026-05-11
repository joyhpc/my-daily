可信度高，可入知识库。

附件 eDP v1.4b：

HBR3 = 8.1Gbps/lane，1UI≈123ps。  
TP3_EQ EYE mask：**75mVpp differential / 0.5UI**。  
其中 75mVpp 来自 +37.5mV / -37.5mV，0.5UI≈61.5ps。

所以我们内部建议按：

**最低判断：75mVpp differential / 0.5UI**  
**更稳妥目标：90mVpp differential / 0.5UI**

之前看到的 **75mV / 0.35UI** 更偏普通 DP RX/接收能力测试资料，不能作为 eDP v1.4b 附件标准的主结论。

参考：

1. 附件 eDP v1.4b：Table 4-11 / Table 4-18
    
2. Intel / Altera AN745：HBR3 RX 75mV / 0.35UI  
    [https://docs.altera.com/r/docs/683623/current/an-745-design-guidelines-for-displayport-ip-interface/main-link-rx-electrical-specifications?contentId=hLW5MMuFf5GkETGJqJ~R2A](https://docs.altera.com/r/docs/683623/current/an-745-design-guidelines-for-displayport-ip-interface/main-link-rx-electrical-specifications?contentId=hLW5MMuFf5GkETGJqJ~R2A)
    
3. Tektronix DP1.4 RX：HBR3 RX 75mV / 0.35UI  
    [https://www.tek.com.cn/sites/default/files/2018-05/DisplayPort-1.4%20Challenges-and-Solutions%20Webinar-2017-61W-61165-0-170417.pdf](https://www.tek.com.cn/sites/default/files/2018-05/DisplayPort-1.4%20Challenges-and-Solutions%20Webinar-2017-61W-61165-0-170417.pdf)
    
4. Tektronix DP1.4 HBR3：90mV / 0.5UI  
    [https://www.tek.com.cn/sites/default/files/2018-05/DisplayPort%20over%20Type-C-TX-RX.pdf](https://www.tek.com.cn/sites/default/files/2018-05/DisplayPort%20over%20Type-C-TX-RX.pdf)

eDP 1.4b / HBR3 / 8.1Gbps 接收端眼图，建议以附件 eDP v1.4b 标准为准，不直接套普通 DP 的 RX 数值。

