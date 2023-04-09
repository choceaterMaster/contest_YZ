# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 10:00:11 2023

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
#analogout config
ch=0 #0 or 1 for channel 1 or 2
node=RDAnalogOutNodeCarrier
func=RDFUNCSine
outfre=2000
offset=0
amp=1.0
symmetry=50
phase=0

print(rd.AnalogOutNodeEnableSet(ch,node,True))
rd.AnalogOutNodeFunctionSet(ch,node,func)
rd.AnalogOutNodeFrequencySet(ch,node,outfre)
rd.AnalogOutNodeOffsetAmpSet(ch,node,offset,amp)
rd.AnalogOutNodeSymmetrySet(ch,node,symmetry)
rd.AnalogOutNodePhaseSet(ch,node,phase)
rd.AnalogOutConfigure(ch,True)

time.sleep(1)



# close all instruments
print(rd.AnalogOutConfigure(0,False))
# close connect
print(rd.DeviceClose())