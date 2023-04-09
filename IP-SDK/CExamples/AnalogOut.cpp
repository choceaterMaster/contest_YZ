#include "instrumentsplayground.h"
#include <windows.h>
#include <stdio.h>
#include <iostream>

int main(int carg, char **szarg){
    FT_HANDLE ftHandle;//设备句柄
    FT_STATUS status;//返回状态
    int idxChannel=0;//模拟输出通道1
    uchar  calArr[14];//校准数组
    printf("Open first device\n");
    status=RDdeviceOpen(0, &ftHandle);//打开设备
    if(status) {
        printf("Device open failed\n\t%s", status);
        return 0;
    }
    //read calibration
    RDCalibrationRead(ftHandle, calArr);//读取校准数组
    //analogout config
    RDAnalogOutNodeEnableSet(ftHandle, idxChannel, RDAnalogOutNodeCarrier, true);//使能模拟输出通道1
    RDAnalogOutNodeFunctionSet(ftHandle, idxChannel, RDAnalogOutNodeCarrier, RDFUNCSine);//设置通道1波形为sine wave
    RDAnalogOutNodeFrequencySet(ftHandle, idxChannel, RDAnalogOutNodeCarrier, 2000);//设置通道1频率2k Hz frequence
    RDAnalogOutNodeOffsetAmpSet(ftHandle, idxChannel, RDAnalogOutNodeCarrier, 0,5,calArr);//设置通道1偏置电压和幅值 offset:0V amplitude:5V
    RDAnalogOutNodeSymmetrySet(ftHandle,idxChannel,RDAnalogOutNodeCarrier,50);//设置通道1对称性 Symmetry
    RDAnalogOutNodePhaseSet(ftHandle,idxChannel,RDAnalogOutNodeCarrier,0);//设置通道1初始相位为0 phase

    RDAnalogOutConfigure(ftHandle,idxChannel, true);//打开模拟输出通道

    Sleep(2);
    printf("done\n");
    
    //stop
    RDAnalogOutConfigure(ftHandle,idxChannel, false);////关闭模拟输出通道

    // close the device
    RDdeviceClose(ftHandle);//关闭设备
}