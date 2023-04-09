#include "instrumentsplayground.h"
#include <windows.h>
#include <stdio.h>
#include <iostream>

int main(int carg, char **szarg){
    FT_HANDLE ftHandle;
    FT_STATUS status;
    uchar  RxBuffer[10];
    int backsize,fparity;
    printf("Open first device\n");
    status=RDdeviceOpen(0, &ftHandle);
    if(status) {
        printf("Device open failed\n\t%s", status);
        return 0;
    }

    //IIC config
    RDDigitalI2CTxRxIOSet(ftHandle,0,1 ); //设置IO接口scl:0 sda:1
    RDDigitalI2CRateSet(ftHandle, 400);     //设置通信速率400hz rate
    RDDigitalI2CTx(ftHandle,0x57,new uchar[2]{0x01,0x01},2);//发送数据send data
    RDDigitalI2CRx(ftHandle,0x57,RxBuffer,2,&backsize,&fparity);     //读取数据read data
    printf("done\n");

    // close the device
    RDdeviceClose(ftHandle);//关闭设备
}