# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import time
import sys, os
import pathlib

py_path, py_name = os.path.split(os.path.abspath(__file__))

base_dir = pathlib.Path(py_path).absolute().parent  # sys.argv[0]

if sys.path.count(base_dir) == 0:
    sys.path.append(str(base_dir))

from pyRD import RD
from pyRD.core.RDconstant import *
from LMS import *
rd = RD()
rd.DeviceEnumLists()
print(rd.devicelist)
print(rd.DeviceOpen(0))

#四个口：模拟量输出(AO)，GND(G),电源+(+)，数字量输出(DO)
#只需要管理模拟量输出和数字量输出
#以下为这两个输出的测试脚本

in_ch=0 #0 or 1 for channel 1 or 2
in_ch2=1
in_range=5 #5 or 25
in_range2=25#not use until use double chs
in_fre=1e6
trig_timeout = 0 # 0 for forever, 1 for 1s
trig_src=RDTRIGSRCNone #RDTRIGSRCDetectorAnalogInCH1 for anlogout channel 1
trig_type=RDTRIGTYPEEdge
trig_leve=0
trig_slope=RDTriggerSlopeEdge
buffersize=2048 # 0.002s

rd.AnalogInCHEnable(in_ch,True)
rd.AnalogInCHRangeSet(in_ch,in_range)
rd.AnalogInCHEnable(in_ch2,True)
rd.AnalogInCHRangeSet(in_ch2,in_range)
rd.AnalogInFrequencySet(in_fre)
rd.AnalogInTriggerAutoTimeoutSet(trig_timeout)
rd.AnalogInTriggerSourceSet(trig_src)
rd.AnalogInTriggerTypeSet(trig_type)
rd.AnalogInTriggerLevelSet(trig_leve,in_range)#(trig_src==RDTRIGSRCDetectorAnalogInCH1)?in_range:in_range2
rd.AnalogInTriggerConditionSet(trig_slope)
rd.AnalogInBufferSizeSet(buffersize)
rd.AnalogInRun(True)

rd.AnalogInStatus() # 获取设备模拟输入模块的状态
i=0
while(rd.analoginstatus!=2)&(i<10):
    rd.AnalogInStatus()
    i=i+1
    print("rd.analoginstatus=",rd.analoginstatus)
#analogIn data read
if(rd.analoginstatus==2):
    rd.AnalogInRead(buffersize,0)
    #rd.AnalogInRead(buffersize,1)
    #print(rd.aibacksizech1,rd.aibacksizech2)
    data=np.array(rd.aidatach1)
    size=rd.aibacksizech1
    av_data=aver(data)
    print("av_data=",av_data)
    fil_data=lms(data,av_data)
    #rd.aidatach1 采样数组?
    #rd.aibacksizech1 实际大小？
    print("rd.aibacksizech1=",rd.aibacksizech1)
    value=list(fil_data)#the ch1 scope data as c_char_p(4086)  don't use rd.aidatach1.value
    ori_value=list(data)
    #err=list(fil_data-data)
    plt.plot(ori_value,'x')
    plt.plot(value,'o')
    plt.show()

# close all instruments
print(rd.AnalogInRun(False))
# close connect
print(rd.DeviceClose())