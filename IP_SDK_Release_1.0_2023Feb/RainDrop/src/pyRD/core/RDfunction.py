# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 11:55:36 2022

@author: jackscl
"""

from ctypes import *
import platform
from pyRD.core.RDconstant import *
import time

import sys,os
import pathlib
 
py_path, py_name = os.path.split(os.path.abspath(__file__))

base_dir = pathlib.Path(py_path).absolute().parent.parent.parent #sys.argv[0]
dll_dir = pathlib.Path(base_dir,"lib")

if sys.path.count(base_dir) == 0:
    sys.path.append(str(base_dir))

class RD:
    def __init__(self):
        if platform.architecture()[0]=='64bit' :
            self.dll=CDLL(str(pathlib.Path(dll_dir,"64","InstrumentsPlayground.dll")))
            self.handle=c_uint64(0) #uint64 is ok at 64-bit platfom
        else:
            self.dll=CDLL(str(pathlib.Path(dll_dir,"32","InstrumentsPlayground.dll")))
            self.handle=c_uint32(0) #uint32 is also ok at 32-bit platfom
        self.devicecount=0        
        self.devicecalibration=(c_uint8*14)()#ao oaoa;sp oo;ai 5oaoa 25oaoa;
        self.range_ch1=5
        self.range_ch2=5

    def SDKVersion(self,prenable=False):
        version=create_string_buffer(64)
        self.dll.RDSDKVersion(byref(version))
        self.SDKversion=version.value

    def DeviceCount(self,prenable=False):
        count=c_int(0)
        self.dll.RDEnumDeviceCount(byref(count))
        self.devicecount=count.value
        if(prenable):
            print(count)
            
    def DeviceEnumLists(self):
        if self.devicecount==0 :
            self.DeviceCount()
        self.devicelist=[]
        for i in range(0,self.devicecount):
            sn=create_string_buffer(64)
            descript=create_string_buffer(64)
            self.dll.RDEnumDeviceInfo(i,byref(sn),byref(descript))
            self.devicelist.append([sn.value,descript.value])
            
    def DeviceOpen(self,index):
        if self.devicecount==0 :
            self.DeviceCount()
        if index>self.devicecount :
            index=self.devicecount-1
        if index<0 :
            index=0
        sts= self.dll.RDdeviceOpen(index,byref(self.handle))
        if sts==0:
            sts=self.dll.RDCalibrationRead(self.handle,byref(self.devicecalibration))
            print("open device success")
        return sts
        
    def DeviceClose(self):
        return self.dll.RDdeviceClose(self.handle)
        
    def AnalogInConfig(self):
       pass
   
    def AnalogInCHEnable(self,ch:int,enable:bool):
        '''Enable AnalogIn current channel acquire data'''
        return self.dll.RDAnalogInChannelEnableSet(self.handle,c_int(ch),c_bool(enable))

    def AnalogInCHRangeSet(self,ch:int,Vrange:float):
        '''Set AnalogIn current channel range: 5 or 25V'''
        if ch==0:
            self.range_ch1=Vrange
        elif ch==1:
            self.range_ch2=Vrange
            
        return self.dll.RDAnalogInChannelRangeSet(self.handle,c_int(ch),c_double(Vrange))
    
    def AnalogInFrequencySet(self,fre:int):
        '''Set AnalogIn Frequency from 1~40e6'''
        return self.dll.RDAnalogInFrequencySet(self.handle,c_int(int(fre)))
    
    def AnalogInTriggerAutoTimeoutSet(self,timeout=0):
        '''timeout 0 for no timeout ,N for timeout = N s'''
        return self.dll.RDAnalogInTriggerAutoTimeoutSet(self.handle,c_int(timeout))
    
    def AnalogInTriggerSourceSet(self,trigsrc=RDTRIGSRCNone):
        '''Set Trigger Source: None CH1 CH2 Ext1 Ext2...'''        
        return self.dll.RDAnalogInTriggerSourceSet(self.handle,c_int(trigsrc))
    
    def AnalogInTriggerTypeSet(self,trigtype=RDTRIGTYPEEdge):
        '''Set Trigger Type: edge is ok'''        
        return self.dll.RDAnalogInTriggerTypeSet(self.handle,c_int(trigtype))
    
    def AnalogInTriggerLevelSet(self,voltsLevel=0.0,voltRange=5):
        '''Set Trigger voltage level : -range ~ +range'''        
        return self.dll.RDAnalogInTriggerLevelSet(self.handle,c_double(voltsLevel),c_int(voltRange))
    
    def AnalogInTriggerConditionSet(self,slope=RDTriggerSlopeEdge):
        '''Set Trigger Slope: edge rising falling for edge type'''        
        return self.dll.RDAnalogInTriggerConditionSet(self.handle,c_int(slope))    
    
    def AnalogInBufferSizeSet(self,buffersize=2048):
        '''Set AnalogIn buffersize:32,64,128,256,512,1024,2048 is fine'''        
        return self.dll.RDAnalogInBufferSizeSet(self.handle,c_int(buffersize))    

    def AnalogInRun(self,run=True):
        '''Set AnalogIn Run or Stop'''        
        return self.dll.RDAnalogInConfigure(self.handle,c_bool(run))        
    
    def AnalogInStatus(self):
        '''Read AnalogIn Status'''
        temp=c_int(0)          
        status=self.dll.RDAnalogInStatus(self.handle,byref(temp))  
        self.analoginstatus = temp.value
        return status
    
    def AnalogInRead(self,size=2048,ch=0):
        '''Read AnalogIn Data ,if something wrong,timeout is 10s'''
        if ch==0 :
            self.aibacksizech1=c_int(0)
            self.aidatach1=(c_double*size)()
            status=self.dll.RDAnalogInRead(self.handle,c_int(ch),c_int(size),c_double(self.range_ch1), byref(self.aidatach1),byref(self.devicecalibration),byref(self.aibacksizech1))
        else:
            self.aibacksizech2=c_int(0)
            self.aidatach2=(c_double*size)()
            status=self.dll.RDAnalogInRead(self.handle,c_int(ch),c_int(size),c_double(self.range_ch2), byref(self.aidatach2),byref(self.devicecalibration),byref(self.aibacksizech2))
        return status
    
    def AnalogOutNodeEnableSet(self,ch=0,node=RDAnalogOutNodeCarrier,enable=True):
        '''Set AnalogOut ch=0or1 :ch1 or ch2; not use'''        
        return self.dll.RDAnalogOutNodeEnableSet(self.handle,c_int(ch),c_int(node),c_bool(enable))     

    def AnalogOutNodeFunctionSet(self,ch=0,node=RDAnalogOutNodeCarrier,func=RDFUNCDC):
        '''Set AnalogOut ch=0or1 :ch1 or ch2;'''        
        return self.dll.RDAnalogOutNodeFunctionSet(self.handle,c_int(ch),c_int(node),c_int(func))
    
    def AnalogOutNodeFrequencySet(self,ch=0,node=RDAnalogOutNodeCarrier,hzFrequency=1000):
        '''Set AnalogOut ch=0or1 :ch1 or ch2;'''        
        return self.dll.RDAnalogOutNodeFrequencySet(self.handle,c_int(ch),c_int(node),c_int(hzFrequency))

    def AnalogOutNodeOffsetAmpSet(self,ch=0,node=RDAnalogOutNodeCarrier,vOffset=0,amp=1.0):
        '''Set AnalogOut ch=0or1 :ch1 or ch2;'''        
        return self.dll.RDAnalogOutNodeOffsetAmpSet(self.handle,c_int(ch),c_int(node),c_double(vOffset),c_double(amp),byref(self.devicecalibration))
    
    def AnalogOutNodeSymmetrySet(self,ch=0,node=RDAnalogOutNodeCarrier,percentageSymmetry=50):
        '''Set AnalogOut ch=0or1 :ch1 or ch2;'''        
        return self.dll.RDAnalogOutNodeSymmetrySet(self.handle,c_int(ch),c_int(node),c_double(percentageSymmetry))
    
    def AnalogOutNodePhaseSet(self,ch=0,node=RDAnalogOutNodeCarrier,degreePhase=0):
        '''Set AnalogIn c_int(ch),node degreePhase=0~360'''        
        return self.dll.RDAnalogOutNodePhaseSet(self.handle,c_int(ch),c_int(node),c_double(degreePhase))
    
    def AnalogOutConfigure(self,ch=0,output=True):
        '''Set AnalogOut ch=0or1 :ch1 or ch2;'''        
        return self.dll.RDAnalogOutConfigure(self.handle,c_int(ch),c_bool(output))

    def AnalogOutNodeDataSet(self,ch=0,node=RDAnalogOutNodeCarrier,data=[]):
        '''Set AnalogOut Custom data set'''        
        size=sizeof(data)
        arr = (ctypes.c_uint8 * len(data))(*data)
        return self.dll.RDAnalogOutNodeDataSet(self.handle,c_int(ch),c_int(node),byref(arry),size)
    
    def AnalogIOChannelNodeSet(self,ch=0,value=0):
        '''Set powerSupply ch=0or1 :positive or negative;value for output voltage , positive 0~5V,negative -5~0V'''        
        return self.dll.RDAnalogIOChannelNodeSet(self.handle,c_int(ch),c_double(value),byref(self.devicecalibration))
    
    def AnalogIOChannelEnableSet(self,ch=0,enable=True):
        '''Set powerSupply ch=0or1 :ch1 or ch2;enable is True for output'''        
        return self.dll.AnalogIOChannelEnableSet(self.handle,c_int(ch),c_bool(enable))
    #DIGITAL IO Part   
    def DigitalIOOutputEnableSet (self,channel=0x00):
        '''DigitalIO staticIO set ch 0x00 to 0xFF LSB for each bit, 1:output 0:input '''        
        return self.dll.RDDigitalIOOutputEnableSet(self.handle,c_uint(channel))
    
    def DigitalIOOutputSet  (self,outdata=0x00):
        '''DigitalIO staticIO set ch 0x00 to 0xFF LSB for each bit, 1:high 0:low '''        
        return self.dll.RDDigitalIOOutputSet(self.handle,c_uint(outdata))
    
    def DigitalIOInputStatus (self):
        '''DigitalIO staticIO read buffer'''   
        self.stiodata=(c_uint32*size)()
        return self.dll.RDDigitalIOInputStatus (self.handle,byref(self.stiodata))
    
    #digital in
    def DigitalInDividerSet(self,div=1):
        '''DigitalIO In (Logic) set Div div=MaxHz/fre '''        
        return self.dll.RDDigitalInDividerSet(self.handle,c_uint32(div))
    
    def DigitalInBufferSizeSet(self,buffersize=2048):
        '''DigitalIO In (Logic) set buffersize 32~2048 '''        
        return self.dll.RDDigitalInBufferSizeSet(self.handle,c_int(buffersize))
    
    def DigitalInChannelSet(self,channel=0x00):
        '''DigitalIO In (Logic) set ch 0x00 to 0xFF LSB for each bit, 1:open 0:close '''        
        return self.dll.RDDigitalInChannelSet(self.handle,c_int(channel))
    
    def DigitalInTriggerSourceSet(self,trigsrc=RDTRIGSRCDetectorDigitalIn):
        '''DigitalIO In (Logic) set trigger source '''        
        return self.dll.RDDigitalInTriggerSourceSet(self.handle,c_int(trigsrc))
   
    def DigitalInTriggerTypeSet(self,trigtype=RDTRIGTYPEEdge):
        '''DigitalIO In (Logic) set trigger type '''        
        return self.dll.RDDigitalInTriggerTypeSet(self.handle,c_int(trigtype))
   
    def DigitalInTriggerSlopeSet(self,trigslope=RDTriggerSlopeEdge):
        '''DigitalIO In (Logic) set trigger slope '''        
        return self.dll.RDDigitalInTriggerSlopeSet(self.handle,c_int(trigslope))
   
    def DigitalInTriggerSet(self,Rais=0,Fall=0):
        '''DigitalIO In (Logic) set trigger r f '''        
        return self.dll.RDDigitalInTriggerSet(self.handle,c_uint32(Rais),c_uint32(Fall))
   
    def DigitalInTriggerTimeoutSet(self,enable=0):
        '''DigitalIO In (Logic) set 1 for 10s 0 for foever '''        
        return self.dll.RDDigitalInTriggerTimeoutSet(self.handle,c_int(enable))
   
    def DigitalInConfigure(self,enable=True):
        '''DigitalIO In (Logic) set buffersize 32~2048 '''        
        return self.dll.RDDigitalInConfigure(self.handle,c_bool(enable))
   
    def DigitalInStatus(self):
        '''DigitalIO In (Logic) status=2 for success '''      
        temp=c_int(0)          
        status=self.dll.RDDigitalInStatus(self.handle,byref(temp))  
        self.digitalinstatus = temp.value
        return status
  
    def DigitalInRead(self,size=2048):
        '''DigitalIO Out (pattern) read buffer'''   
        self.dibacksize=c_int(0)
        self.didata=(c_uint16*size)()
        return self.dll.RDDigitalInRead(self.handle,c_int(size), byref(self.didata),byref(self.dibacksize))
 
    #digital out
    def DigitalOutRun(self,enable=True):
        '''DigitalIO Out (pattern) enable =1 to run '''        
        return self.dll.RDDigitalOutRun(self.handle,c_bool(enable))
    def DigitalOutTriggerSourceSet(self,trigsrc=RDTRIGSRCDetectorDigitalIn):
        '''DigitalIO Out (pattern) set TriggerSource '''        
        return self.dll.RDDigitalOutTriggerSourceSet(self.handle,c_int(trigsrc))
    def DigitalOutTriggerSlopeSet(self,trigslope=RDTriggerSlopeEdge):
        '''DigitalIO Out (pattern) set TriggerSlope '''        
        return self.dll.RDDigitalOutTriggerSlopeSet(self.handle,c_int(trigslope))
    def DigitalOutEnableSet(self,chs=0x00):
        '''DigitalIO Out (pattern) set ch 0x00 to 0xFF LSB for each bit, 1:open 0:close '''        
        return self.dll.RDDigitalOutEnableSet(self.handle,c_uint(chs))
    def DigitalOutTypeSet(self,ch=0,dotype=RDDigitalOutTypePulse):
        '''DigitalIO Out (pattern) set each ch(0~15) ouytput type '''        
        return self.dll.RDDigitalOutTypeSet(self.handle,c_int(ch),c_int(dotype))
    def DigitalOutIdleSet(self,ch=0,doidle=RDDigitalOutIdleLow):
        '''DigitalIO Out (pattern) set each ch(0~15) ouytput Idle '''        
        return self.dll.RDDigitalOutIdleSet(self.handle,c_int(ch),c_int(doidle))
    def DigitalOutDividerInitSet(self,ch=0,divinit=0):
        '''DigitalIO Out (pattern) set each ch(0~15) ouytput delay 25ns=1 divinit'''        
        return self.dll.RDDigitalOutDividerInitSet(self.handle,c_int(ch),c_uint(divinit))
    def DigitalOutDividerSet(self,ch=0,div=1):
        '''DigitalIO Out (pattern) set each ch(0~15) ouytput div=maxfre/fre '''        
        return self.dll.RDDigitalOutDividerSet(self.handle,c_int(ch),c_uint(div))
    def DigitalOutCounterInitSet(self,ch=0,initlevel=0,counter=0):
        '''DigitalIO Out (pattern) set each ch(0~15) ouytput begin level and counter for last time '''        
        return self.dll.RDDigitalOutCounterInitSet(self.handle,c_int(ch),c_int(initlevel),c_uint(counter))
    def DigitalOutCounterSet(self,ch=0,counter_l=1,counter_h=1):
        '''DigitalIO Out (pattern) set each ch(0~15) ouytput duty=counter_h/counter_l '''        
        return self.dll.RDDigitalOutCounterSet(self.handle,c_int(ch),c_uint(counter_l),c_uint(counter_h))
    #protocal-uart
    def DigitalUartRateSet(self,rate=9600):
        '''DigitalIO Out (uart) fre= 110,150,300,600,1200,2400,4800,9600,14400,19200,28800,38400,56000,57600,115200,128000,153600,230400,256000,460800,921600'''        
        return self.dll.RDDigitalUartRateSet(self.handle,c_double(rate))
    def DigitalUartDIOSet(self,TxDIO=0,RxDIO=1):
        '''DigitalIO Out (uart) dio is 0 to 15 '''        
        return self.dll.RDDigitalUartTxRxIOSet(self.handle,c_int(TxDIO),c_int(RxDIO))
    def DigitalUartTx(self,data=[]):
        '''DigitalIO Out (uart) data size is max 255, each value 0~255  '''   
        arr = (ctypes.c_uint8 * len(data))(*data)
        return self.dll.RDDigitalUartTx(self.handle,byref(arr),c_int(len(data)))
    def DigitalUartRx(self,size=8192):
        '''DigitalIO Out (uart) read rx data '''        
        self.uartbacksize=c_int(0)
        fParity=c_int(0)
        self.uartdata=(c_uint8*size)()
        return self.dll.RDDigitalUartRx(self.handle, byref(self.uartdata),c_int(size),byref(self.uartbacksize),byref(fParity))
    #protocal-i2c
    def DigitalI2CtRateSet(self,rate=10000):
        '''DigitalIO Out (spi) fre={1,4,10,40,100,400,1000,4000,1e4,4e4,1e5,4e5,1e6,4e6,1e7,0};'''        
        return self.dll.RDDigitalI2CtRateSet(self.handle,c_double(rate))
    def DigitalI2CtDIOSet(self,SCLDIO=0,SDADIO=1):
        '''DigitalIO Out (spi) dio is 0 to 15 '''        
        return self.dll.RDDigitalI2CtTxRxIOSet(self.handle,c_int(SCLDIO),c_int(SDADIO))
    def DigitalI2CtTx(self,data=[],addr=0x00):
        '''DigitalIO Out (spi) data size is max 255, each value 0~255  '''   
        arr = (ctypes.c_uint8 * len(data))(*data)
        return self.dll.RDDigitalI2CtTx(self.handle,c_uint8(addr),byref(arr),c_int(len(data)))
    def DigitalI2CtRx(self,size=8192,addr=0x00):
        '''DigitalIO Out (spi) read rx data '''        
        self.I2Ctbacksize=c_int(0)
        fParity=c_int(0)
        self.I2Ctdata=(c_uint8*size)()
        return self.dll.RDDigitalI2CtRx(self.handle,c_uint8(addr), byref(self.I2Ctdata),c_int(size),byref(self.I2Ctbacksize),byref(fParity))
    #protocal-spi
    def DigitalSPIRateSet(self,rate=10000):
        '''DigitalIO Out (i2c) fre={1,4,10,40,100,400,1000,4000,1e4,4e4,1e5,4e5,1e6,4e6,1e7,0};'''        
        return self.dll.RDDigitalSPItRateSet(self.handle,c_double(rate))
    def DigitalSPItDIOSet(self,CSDIO=0,CLKDIO=1,DQ0=2,DQ1=3):
        '''DigitalIO Out (i2c) dio is 0 to 15 '''        
        return self.dll.RDDigitalSPItTxRxIOSet(self.handle,c_int(CSDIO),c_int(CLKDIO),c_int(DQ0),c_int(DQ1))
    def DigitalSPItTx(self,data=[]):
        '''DigitalIO Out (i2c) data size is max 255, each value 0~255  '''   
        arr = (ctypes.c_uint8 * len(data))(*data)
        return self.dll.RDDigitalSPItTx(self.handle,byref(arr),c_int(len(data)))
    def DigitalSPItRx(self,size=8192):
        '''DigitalIO Out (i2c) read rx data '''        
        self.SPItbacksize=c_int(0)
        fParity=c_int(0)
        self.SPItdata=(c_uint8*size)()
        return self.dll.RDDigitalSPItRx(self.handle, byref(self.SPItdata),c_int(size),byref(self.SPItbacksize),byref(fParity))

 
if __name__ == "__main__":
    a=RD()
    a.DeviceEnumLists()
    print(a.devicelist)
    print(a.DeviceOpen(0))
    print(a.AnalogOutNodeEnableSet(0,0,True))
    print(a.AnalogOutNodeFunctionSet(0,0,1))
    print(a.AnalogOutNodeFrequencySet(0,0,2000))
    print(a.AnalogOutNodeOffsetAmpSet(0,0,0,2.0))
    print(a.AnalogOutNodeSymmetrySet(0,0,50))
    print(a.AnalogOutNodePhaseSet(0,0,0))
    print(a.AnalogOutConfigure(0,True))    
    time.sleep(1)
    print(a.AnalogOutConfigure(0,False))
    
    print(a.DeviceClose())