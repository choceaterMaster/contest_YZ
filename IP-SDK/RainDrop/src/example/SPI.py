# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 09:57:42 2023

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

#Uart 
CSDIO=0
CLKDIO=1
DQ0=2
DQ1=3
Rate=10000
RxSize=4
rd.DigitalSPIDIOSet(IO_Tx,IO_Rx)
rd.DigitalSPIRateSet(Rate)
rd.DigitalSPITx([0xFD,0x00,0xCC,0xDF])
time.sleep(1)
rd.DigitalSPIRx(RxSize)
    
print(list(rd.spidata))

# close connect
print(rd.DeviceClose())