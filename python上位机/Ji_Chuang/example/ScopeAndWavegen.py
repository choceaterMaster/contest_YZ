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

rd.AnalogInCHEnable(in_ch,True)
rd.AnalogInCHRangeSet(in_ch,in_range)
rd.AnalogInFrequencySet(in_fre)
rd.AnalogInTriggerAutoTimeoutSet(trig_timeout)
rd.AnalogInTriggerSourceSet(trig_src)
rd.AnalogInTriggerTypeSet(trig_type)
rd.AnalogInTriggerLevelSet(trig_leve,in_range)#(trig_src==RDTRIGSRCDetectorAnalogInCH1)?in_range:in_range2
rd.AnalogInTriggerConditionSet(trig_slope)
rd.AnalogInBufferSizeSet(buffersize)
rd.AnalogInRun(True)

rd.AnalogInStatus()
i=0
while(rd.analoginstatus!=2)&(i<10):
    rd.AnalogInStatus()
    i=i+1
    print(rd.analoginstatus)
    
if(rd.analoginstatus==2):
    rd.AnalogInRead(buffersize,0)
    print(rd.aibacksizech1)
    value=list(rd.aidatach1)#the ch1 scope data as c_char_p(4086)  don't use rd.aidatach1.value
    plt.plot(value)

# close all instruments
print(rd.AnalogOutConfigure(0,False))
print(rd.AnalogInRun(False))
# close connect
print(rd.DeviceClose())