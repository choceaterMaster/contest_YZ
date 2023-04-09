# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 09:57:09 2023

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
#IIC 
IO_SCL=0
IO_SDA=1
Rate=400
Addr=0x48
RxSize=1
rd.DigitalI2CDIOSet(IO_SCL,IO_SDA)
rd.DigitalI2CRateSet(Rate)
rd.DigitalI2CTx([0x01,0x60],Addr)
rd.DigitalI2CRx(RxSize,Addr)
    
print(list(rd.I2Cdata))

# close connect
print(rd.DeviceClose())