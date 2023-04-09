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

    //SPI config
    RDDigitalSPITxRxIOSet(ftHandle,0,1,2,3 ); //scDIO:0 clockDIO:1 DQ0:2 DQ1:3
    RDDigitalSPIRateSet(ftHandle, 400);     //400hz rate
    RDDigitalSPITx(ftHandle,new uchar[2]{0x01,0x01},2);//send data
    RDDigitalSPIRx(ftHandle,RxBuffer,2,&backsize,&fparity);     //read data
    printf("done\n");

    // close the device
    RDdeviceClose(ftHandle);//关闭设备
}