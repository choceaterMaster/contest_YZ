#include "instrumentsplayground.h"
#include <windows.h>
#include <stdio.h>
#include <iostream>

int main(int carg, char **szarg){
    FT_HANDLE ftHandle;
    FT_STATUS status;
    uint  staicIO;
    printf("Open first device\n");
    status=RDdeviceOpen(0, &ftHandle);
    if(status) {
        printf("Device open failed\n\t%s", status);
        return 0;
    }

    //Static IO config
    RDDigitalIOOutputEnableSet(ftHandle,0x01 ); //使能静态输出接口set IO0 to Output
    RDDigitalIOOutputSet(ftHandle, 0x01);     //设置静态输出电平set IO0 Output high
    RDDigitalIOInputStatus(ftHandle,&staicIO);//读取静态IO状态read IOs
    printf("status:%d",staicIO);

    printf("done\n");

    RDDigitalIOOutputEnableSet(ftHandle,0x00);//关闭所有静态IO输出
    // close the device
    RDdeviceClose(ftHandle);//关闭设备
}