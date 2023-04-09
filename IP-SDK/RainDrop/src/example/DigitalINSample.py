# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 09:56:33 2023

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
#DigitalIn config
div=int(40e6/1e6)
buffersize=2048
CHEnable=0xFF
trigsrc=RDTRIGSRCDetectorDigitalIn
slope=RDTriggerSlopeRise
times=1
fsEdgeRise=0xFF
fsEdgeFall=0xFF
rd.DigitalInDividerSet(div)#div=40MHz/samplerate  -->1MHz
rd.DigitalInBufferSizeSet(buffersize)#
rd.DigitalInChannelSet(CHEnable)#set DigitalIn's IOs

rd.DigitalInTriggerSourceSet(trigsrc)#0=None
rd.DigitalInTriggerTypeSet(0)#triggerType
rd.DigitalInTriggerSlopeSet(slope)#
rd.DigitalInTriggerTimeoutSet(times)#when source!=None ,wait times. if times=0 , wait forever

rd.DigitalInTriggerSet(fsEdgeRise,fsEdgeFall)#DigitalIn Trigger Channle Edge enable

ftStatus=rd.DigitalInConfigure(True)#Run

#DigitalIn status read
rd.DigitalInStatus()
i=0
while(rd.digitalinstatus!=2)&(i<10):
    rd.DigitalInStatus()
    i=i+1
    print(rd.digitalinstatus)
    
#DigitalIn data read
if(rd.digitalinstatus==2):
    rd.DigitalInRead(buffersize)
    print(rd.dibacksize)
    rowlist=list(rd.didata)
    for ch in range(16):
        value=[]
        for i in range(buffersize):
            value.append(int((rowlist[i]>>ch)&1)*0.9+16-ch)
        plt.plot(value)

# close all instruments
print(rd.DigitalInConfigure(False))
# close connect
print(rd.DeviceClose())