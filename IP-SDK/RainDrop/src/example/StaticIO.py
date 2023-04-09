# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 09:56:01 2023

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
CHs_OUT=0x01 #DIO0 enable output
CHs_OUTValue=0x01 #DIO0 output value set high

rd.DigitalIOOutputEnableSet(CHs_OUT) 
rd.DigitalIOOutputSet(CHs_OUTValue) 
rd.DigitalIOInputStatus() #first reading drop

time.sleep(0.1)
j=10
while(j>0):
    rd.DigitalIOInputStatus() 
    value=rd.stiodata.value
    print(value)
    status=[]
    for i in range(16):
        status.append((value>>i)&1)
    print(status)
    j=j-1
    time.sleep(0.1)
# close connect
print(rd.DeviceClose())