#include "instrumentsplayground.h"
#include <windows.h>
#include <stdio.h>
#include <iostream>

int main(int carg, char **szarg){
    FT_HANDLE ftHandle;
    FT_STATUS status;
    int cSamples=2048;
    uchar  calArr[14];
    printf("Open first device\n");
    status=RDdeviceOpen(0, &ftHandle);
    if(status) {
        printf("Device open failed\n\t%s", status);
        return 0;
    }
    //read calibration
    RDCalibrationRead(ftHandle, calArr);
    //power supplies config
    RDAnalogIOChannelNodeSet(ftHandle, 0, 3.3,calArr); //设置正极电压positive 3.3V
    RDAnalogIOChannelEnableSet(ftHandle, 0, true);     //打开正极电压open positive supply
    RDAnalogIOChannelNodeSet(ftHandle, 1, -3.3,calArr);//设置负极电压negative -3.3V
    RDAnalogIOChannelEnableSet(ftHandle, 1, true);     //打开负极电压open negative supply

    Sleep(2);
    printf("done\n");
    
    //stop
    RDAnalogIOChannelEnableSet(ftHandle, 0, false);//positive
    RDAnalogIOChannelEnableSet(ftHandle, 1, false);//negative

    // close the device
    RDdeviceClose(ftHandle);//关闭设备
}