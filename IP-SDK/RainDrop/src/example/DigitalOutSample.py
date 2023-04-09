# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 09:56:42 2023

@author: jackscl
"""

import matplotlib.pyplot as plt
import numpy as np
import time
import sys,os
import pathlib
py_path, py_name = os.path.split(os.path.abspath(__file__))

base_dir = pathlib.Path(py_path).absolute().parent #sys.argv[0]
 
if sys.path.count(base_dir) == 0:
    sys.path.append(str(base_dir))
 
from pyRD import RD
from pyRD.core.RDconstant import *


rd=RD()
rd.DeviceEnumLists()
print(rd.devicelist)
print(rd.DeviceOpen(0))
#DigitalOut config
div=int(20e6/1e3)#max=20MHz

trigsrc=RDTRIGSRCDetectorDigitalIn
slope=RDTriggerSlopeRise
chEnables=[1,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0]#digtial io 0 enable
chTypes=[RDDigitalOutTypePulse,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0]#digtial io 0 enable
divs=[div,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0]
idles=[0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0]#空闲电平高低
divinit=[0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0]#初始状态保持时间的div个数
counter_l=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]#高电平计数
counter_h=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]#低电平计数

rd.DigitalOutTriggerSourceSet(trigsrc)#0=None
rd.DigitalOutTriggerSlopeSet(slope)#
rd.DigitalOutEnableSet(0x01)#设置输出使能
temp=0
for i in range(16):
    temp|=chEnables[i]<<i#
    if chEnables[i]==0:
        continue
    rd.DigitalOutTypeSet(i,chTypes[i])#
    rd.DigitalOutIdleSet(i, idles[i])#
    rd.DigitalOutDividerSet(i, divs[i])#
    if chTypes[i]==RDDigitalOutTypePulse:    
        rd.DigitalOutCounterInitSet(i, idles[i], divinit[i])#//
        rd.DigitalOutCounterSet(i,  counter_l[i],counter_h[i])#    
    elif(chTypes[i]==RDDigitalOutTypeCustom):    
        rd.DigitalOutCounterInitSet(i,0, divinit[i])#
        # rd.DigitalOutDataSet(i, rgdSamples[i], countOfBits[i])#    
    elif(chTypes[i]==RDDigitalOutTypeRandom):    
        rd.DigitalOutCounterSet(i,1, 1)#
    

    
ftStatus=rd.DigitalOutRun(True)#Run

time.sleep(1)

# close all instruments
print(rd.DigitalOutRun(False))
# close connect
print(rd.DeviceClose())