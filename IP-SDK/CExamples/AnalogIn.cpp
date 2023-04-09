#include "instrumentsplayground.h"
#include <windows.h>
#include <stdio.h>
#include <iostream>

int main(int carg, char **szarg){
    FT_HANDLE ftHandle;//设备句柄
    FT_STATUS status;//返回状态
    RDState sts;//采集状态
    double* rgdSamples;//回读数组
    int cSamples=2048;//采样数
    int range=5;//电压量产
    double trigLevel=1.0;//触发电平
    uchar  calArr[14];//校准数组
    int backsize;//回读值
    DWORD devicecount;
    RDEnumDeviceCount(&devicecount);//查询设备数量
    if(devicecount==0)
    {
        printf("No device found!");
        return 0;
    }
    printf("Open first device\n");
    status=RDdeviceOpen(0, &ftHandle);//打开第一个设备
    if(status) {
        printf("Device open failed\n\t%s", status);
        return 0;
    }
    //read calibration
    RDCalibrationRead(ftHandle, calArr);//读取校准数组
    
    // enable channels
    RDAnalogInChannelEnableSet(ftHandle, 0, true);//模拟输入通道使能
    RDAnalogInChannelEnableSet(ftHandle, 1, true);

    // set 5V pk2pk input range for all channels
    RDAnalogInChannelRangeSet(ftHandle, 0, range);//设置模拟输入电压量程5V
    RDAnalogInChannelRangeSet(ftHandle, 1, range);

    // 20MHz sample rate
    RDAnalogInFrequencySet(ftHandle, 20000000);//设置模拟输入频率 20MHz
    
    rgdSamples = new double[cSamples];

    // configure trigger
    RDAnalogInTriggerSourceSet(ftHandle, RDTRIGSRCDetectorAnalogInCH1);//模拟输入通道1
    RDAnalogInTriggerAutoTimeoutSet(ftHandle, 10.0);//10s超时
    RDAnalogInTriggerTypeSet(ftHandle, RDTRIGTYPEEdge);//触发类型：边沿触发
    RDAnalogInTriggerLevelSet(ftHandle, trigLevel,range);//触发电平
    RDAnalogInTriggerConditionSet(ftHandle, RDTriggerSlopeEdge);//边沿触发方向 双边

    // wait at 1 s
    Sleep(1);

    // start
    RDAnalogInConfigure(ftHandle,  true);//模拟输入启动
    
    printf("Waiting for triggered or auto acquisition\n");
    do{
        RDAnalogInStatus(ftHandle, &sts);//询问模拟输入状态
    }while(sts != RDStateReady);
    
    // get the samples for each channel
    
    RDAnalogInRead(ftHandle, 0,cSamples,range, rgdSamples, calArr,&backsize);//读取模拟输入通道1结果
    printf("ch1 data count:%s\n",backsize);
    RDAnalogInRead(ftHandle, 1,cSamples,range, rgdSamples, calArr,&backsize);//读取模拟输入通道2结果
    printf("ch1 data count:%s\n",backsize);

    
    printf("done\n");
    
    //stop
    RDAnalogInConfigure(ftHandle,  false);//关闭模拟输入通道

    // close the device
    RDdeviceClose(ftHandle);//关闭设备

}