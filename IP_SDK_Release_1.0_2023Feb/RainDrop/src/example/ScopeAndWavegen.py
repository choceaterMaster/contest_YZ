# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 11:35:52 2022

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


a=RD()
a.DeviceEnumLists()
print(a.devicelist)
print(a.DeviceOpen(1))
#analogout config
ch=0 #0 or 1 for channel 1 or 2
node=RDAnalogOutNodeCarrier
func=RDFUNCSine
outfre=2000
offset=0
amp=1.0
symmetry=50
phase=0

print(a.AnalogOutNodeEnableSet(ch,node,True))
a.AnalogOutNodeFunctionSet(ch,node,func)
a.AnalogOutNodeFrequencySet(ch,node,outfre)
a.AnalogOutNodeOffsetAmpSet(ch,node,offset,amp)
a.AnalogOutNodeSymmetrySet(ch,node,symmetry)
a.AnalogOutNodePhaseSet(ch,node,phase)
a.AnalogOutConfigure(ch,True)

time.sleep(1)

#analogin config

in_ch=0 #0 or 1 for channel 1 or 2
in_range=5 #5 or 25
in_range2=25#not use until use double chs
in_fre=1e6
trig_timeout = 0 # 0 for forever, 1 for 1s
trig_src=RDTRIGSRCNone #RDTRIGSRCDetectorAnalogInCH1 for anlogout channel 1
trig_type=RDTRIGTYPEEdge
trig_leve=0
trig_slope=RDTriggerSlopeEdge
buffersize=2048

a.AnalogInCHEnable(in_ch,True)
a.AnalogInCHRangeSet(in_ch,in_range)
a.AnalogInFrequencySet(in_fre)
a.AnalogInTriggerAutoTimeoutSet(trig_timeout)
a.AnalogInTriggerSourceSet(trig_src)
a.AnalogInTriggerTypeSet(trig_type)
a.AnalogInTriggerLevelSet(trig_leve,int_range)#(trig_src==RDTRIGSRCDetectorAnalogInCH1)?in_range:in_range2
a.AnalogInTriggerConditionSet(trig_slope)
a.AnalogInBufferSizeSet(buffersize)
a.AnalogInRun(True)

a.AnalogInStatus()
i=0
while(a.analoginstatus!=2)&(i<10):
    a.AnalogInStatus()
    i=i+1
    print(a.analoginstatus)
    
if(a.analoginstatus==2):
    a.AnalogInRead(buffersize,0)
    print(a.aibacksizech1)
    value=list(a.aidatach1)#the ch1 scope data as c_char_p(4086)  don't use a.aidatach1.value
    plt.plot(value)

# close all instruments
print(a.AnalogOutConfigure(0,False))
print(a.AnalogInRun(False))
# close connect
print(a.DeviceClose())