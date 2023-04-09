#include "instrumentsplayground.h"
#include <windows.h>
#include <stdio.h>
#include <iostream>

int main(int carg, char **szarg){
    FT_HANDLE ftHandle;//设备句柄
    FT_STATUS status;//返回状态
    int div=(20e6/1e3);//max=40MHz

    RDTRIGSRC trigsrc=0;
    RDTriggerSlope slope=RDTriggerSlopeRise;
    uchar chEnables[16]={1,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0};//digtial io 0 enable
    uchar chTypes[16]={RDDigitalOutTypePulse,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0};//digtial io 0 enable
    uchar divs[16]={div,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0};//分频
    uchar idles[16]={0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0};//空闲电平高低
    uchar divinit[16]={0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0};//初始状态保持时间的div个数
    uchar counter_l[16]={1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};//高电平计数
    uchar counter_h[16]={1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};//低电平计数
    printf("Open first device\n");
    status=RDdeviceOpen(0, &ftHandle);
    if(status) {
        printf("Device open failed\n\t%s", status);
        return 0;
    }
    //DigitalOut config


    RDDigitalOutTriggerSourceSet(ftHandle,trigsrc);//0=None 不启用触发
    //RDDigitalOutTriggerSlopeSet(ftHandle,slope);//边沿触发方向
    RDDigitalOutEnableSet(ftHandle,0x01);//ch1 output enable

    int temp=0;
    for(int i=0;i<16;i++)
    {
        temp|=chEnables[i]<<i;//
        if (chEnables[i]==0)    continue;
        RDDigitalOutTypeSet(ftHandle,i,chTypes[i]);//设置输出类型
        RDDigitalOutIdleSet(ftHandle,i, idles[i]);//设置空闲电平
        RDDigitalOutDividerSet(ftHandle,i, divs[i]);//设置分频
        if(chTypes[i]==RDDigitalOutTypePulse)
        {         
            RDDigitalOutCounterInitSet(ftHandle,i, idles[i], divinit[i]);////设置初始counter电平和持续时间 divinit/40Mhz*div
            RDDigitalOutCounterSet(ftHandle,i,  counter_l[i],counter_h[i]);//设置高低电平的计数 比如频率为1khz的时候 counter_l=counter_h=1 则为一个500hz的占空比50%的方波信号   
        }   
        else if(chTypes[i]==RDDigitalOutTypeCustom)   
        {
            RDDigitalOutCounterInitSet(ftHandle,i,0, divinit[i]);//
            // RDDigitalOutDataSet(ftHandle,i, rgdSamples[i], countOfBits[i])//  
        }  
        else if(chTypes[i]==RDDigitalOutTypeRandom)   
        {
            RDDigitalOutCounterSet(ftHandle,i,1, 1);//
        }
    }

        
    RDDigitalOutRun(ftHandle,true);//启动数字输出
    Sleep(2);

    printf("done\n");
    
    //stop
    RDDigitalOutRun(ftHandle, false);//stop DigitalOut

    // close the device
    RDdeviceClose(ftHandle);//关闭设备
}
