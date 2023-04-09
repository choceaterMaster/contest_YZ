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

    //Uart config
    RDDigitalUartTxRxIOSet(ftHandle,0,1 ); //设置接口TX:0 RX:1
    RDDigitalUartRateSet(ftHandle, 9600);     //设置波特率9600Hz rate
    RDDigitalUartTx(ftHandle,new uchar[4]{0xfd,0x00,0xcc,0xdf},4);//发送串口数据send data
    RDDigitalUartRx(ftHandle,RxBuffer,4,&backsize,&fparity);     //读取串口数据read data
    printf("done\n");

    // close the device
    RDdeviceClose(ftHandle);//关闭设备
}