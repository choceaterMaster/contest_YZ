#include "instrumentsplayground.h"
#include <windows.h>
#include <stdio.h>
#include <iostream>

int main(int carg, char **szarg){
    FT_HANDLE ftHandle;//设备句柄
    FT_STATUS status;//返回状态
    RDState sts;//数字通道状态
    uint16_t RxBuffer[512] ;//数字通道返回数组
    bool diostatus[16][512];//数字16路通道每个采样点对于状态
    int backsize;//返回数组大小
    int div=40e6/1e6;//分频
    int buffersize=512;//数组大小
    uchar CHEnable=0xFF;//启用输入通道
    int trigsrc=RDTRIGSRCDetectorDigitalIn;//触发源为数字输入
    int slope=RDTriggerSlopeRise;//上升沿触发
    int times=1;//延时1秒
    uchar fsEdgeRise=0xFF;//上升沿触发通道使能
    uchar fsEdgeFall=0xFF;//下降沿触发通道使能
    printf("Open first device\n");
    status=RDdeviceOpen(0, &ftHandle);
    if(status) {
        printf("Device open failed\n\t%s", status);
        return 0;
    }
    //DigitalIn config

    RDDigitalInDividerSet(ftHandle,div);//数字输入分频div=40MHz/samplerate  -->1MHz
    RDDigitalInBufferSizeSet(ftHandle,buffersize);//数字输入采样数量
    RDDigitalInChannelSet(ftHandle,CHEnable);//通道使能set DigitalIn's IOs

    RDDigitalInTriggerSourceSet(ftHandle,trigsrc);//设置触发源0=None
    RDDigitalInTriggerTypeSet(ftHandle,0);//设置触发类型triggerType
    RDDigitalInTriggerSlopeSet(ftHandle,slope);//设置上升沿触发
    RDDigitalInTriggerTimeoutSet(ftHandle,times);//使能边沿触发的数字通道 when source!=None ,wait times. if times=0 , wait forever

    RDDigitalInTriggerSet(ftHandle,fsEdgeRise,fsEdgeFall);//DigitalIn Trigger Channle Edge enable

    status=RDDigitalInConfigure(ftHandle,true);//Run

    //DigitalIn status read
    RDDigitalInStatus(ftHandle,&sts);
    int i=0;
    while((sts!=2)&&(i++<10)){
        RDDigitalInStatus(ftHandle,&sts);//读取采集状态
        i=i+1;
    }
    //DigitalIn data read
    if(sts==2)
    {
        RDDigitalInRead(ftHandle,buffersize,RxBuffer,&backsize);//读取数据
        printf("count is %d",backsize);
        for (int i=0;i<16;i++)
        {
            for (int j=0;j<backsize;j++)
                diostatus[i][j]=(RxBuffer[j]>>i)&0x01;//数据处理
        }
    }


    printf("done\n");
    
    //stop
    RDDigitalInConfigure(ftHandle, false);//关闭数字输入采样

    // close the device
    RDdeviceClose(ftHandle);//关闭设备
}