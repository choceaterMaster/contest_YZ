# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 14:58:15 2023

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
#Supplies 
postivech=0
posV=5
negativech=1
negV=-3.3
rd.AnalogIOChannelNodeSet(postivech,posV) 
rd.AnalogIOChannelEnableSet(postivech,1) 
rd.AnalogIOChannelNodeSet(negativech,negV) 
rd.AnalogIOChannelEnableSet(negativech,0) 
time.sleep(1)
#Uart 
IO_Tx=0
IO_Rx=1
Rate=9600
RxSize=4
rd.DigitalUartDIOSet(IO_Tx,IO_Rx)
rd.DigitalUartRateSet(Rate)
#rd.DigitalUartTx([0xFD,0x00,0xCC,0xDF])
time.sleep(1)
i=10
while i>=0:
    rd.DigitalUartRx(RxSize)
    time.sleep(0.5)
    print(list(rd.uartdata))
    i=i-1
    
print(list(rd.uartdata))

rd.AnalogIOChannelEnableSet(postivech,0) 
rd.AnalogIOChannelEnableSet(negativech,0) 

# close connect
print(rd.DeviceClose())