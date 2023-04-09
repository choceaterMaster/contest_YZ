#ifndef INSTRUMENTSPLAYGROUND_H
#define INSTRUMENTSPLAYGROUND_H

//#include "InstrumentsPlayground_global.h"
#include <ctime>
#include <cmath>
#include "ftd2xx.h"
#ifndef RDAPI
    #if defined(WIN32)
        #if defined(__cplusplus)
            #define    RDAPI extern "C" __declspec(dllimport)
        #else
            #define    RDAPI __declspec(dllimport)
        #endif
    #else
        #if defined(__cplusplus)
            #define RDAPI extern "C"
        #else
            #define RDAPI
        #endif
    #endif
#endif
typedef unsigned char uchar;
typedef unsigned short uint16_t;
typedef unsigned int uint;

typedef signed short int16_t;
typedef signed int int32_t;

// trigger source
typedef BYTE RDTRIGSRC;
const RDTRIGSRC RDTRIGSRCNone                  = 0;
const RDTRIGSRC RDTRIGSRCDetectorAnalogInCH1   = 1;
const RDTRIGSRC RDTRIGSRCDetectorAnalogInCH2   = 2;
const RDTRIGSRC RDTRIGSRCAnalogOut1            = 3;
const RDTRIGSRC RDTRIGSRCAnalogOut2            = 4;
const RDTRIGSRC RDTRIGSRCDetectorDigitalIn     = 5;
const RDTRIGSRC RDTRIGSRCDigitalOut            = 6;
const RDTRIGSRC RDTRIGSRCManule                = 7;
const RDTRIGSRC RDTRIGSRCExternal1             = 8;
const RDTRIGSRC RDTRIGSRCExternal2             = 9;
const RDTRIGSRC RDTRIGSRCDigitalIn              =10;


// instrument states:
typedef BYTE RDState;
const RDState RDStateReady        = 0;
const RDState RDStateConfig       = 4;
const RDState RDStatePrefill      = 5;
const RDState RDStateArmed        = 1;
const RDState RDStateWait         = 7;
const RDState RDStateTriggered    = 3;//6
const RDState RDStateRunning      = 3;
const RDState RDStateDone         = 2;


// acquisition modes:
typedef int RDACQMODE;
const RDACQMODE RDACQMODESingle     = 0;
const RDACQMODE RDACQMODEScanShift  = 1;
const RDACQMODE RDACQMODEScanScreen = 2;
const RDACQMODE RDACQMODERecord     = 3;
const RDACQMODE RDACQMODEOvers      = 4;
const RDACQMODE RDACQMODESingle1    = 5;

// analog acquisition RDFILTER:
typedef int RDFILTER;
const RDFILTER RDFILTERDecimate = 0;
const RDFILTER RDFILTERAverage  = 1;
const RDFILTER RDFILTERMinMax   = 2;

// analog acquisition RDFILTER:
typedef int RDTriggerSlope;
const RDTriggerSlope RDTriggerSlopeRise   = 0;
const RDTriggerSlope RDTriggerSlopeFall   = 1;
const RDTriggerSlope RDTriggerSlopeEdge   = 2;

// analog in trigger mode:
typedef int RDTRIGTYPE;
const RDTRIGTYPE RDTRIGTYPEEdge         = 0;
const RDTRIGTYPE RDTRIGTYPEPulse        = 1;
const RDTRIGTYPE RDTRIGTYPETransition   = 2;


// analog in trigger length condition
typedef int RDTRIGLEN;
const RDTRIGLEN RDTRIGLENLess       = 0;
const RDTRIGLEN RDTRIGLENTimeout    = 1;
const RDTRIGLEN RDTRIGLENMore       = 2;

// error codes for RD Public API:
typedef int RDERC;
const   RDERC RDercNoErc                  = 0;        //  No error occurred
const   RDERC RDercUnknownError           = 1;        //  API waiting on pending API timed out
const   RDERC RDercApiLockTimeout         = 2;        //  API waiting on pending API timed out
const   RDERC RDercAlreadyOpened          = 3;        //  Device already opened
const   RDERC RDercNotSupported           = 4;        //  Device not supported
const   RDERC RDercInvalidParameter0      = 0x10;     //  Invalid parameter sent in API call
const   RDERC RDercInvalidParameter1      = 0x11;     //  Invalid parameter sent in API call
const   RDERC RDercInvalidParameter2      = 0x12;     //  Invalid parameter sent in API call
const   RDERC RDercInvalidParameter3      = 0x13;     //  Invalid parameter sent in API call
const   RDERC RDercInvalidParameter4      = 0x14;     //  Invalid parameter sent in API call

// analog out signal types
typedef BYTE RDFUNC;
const RDFUNC RDFUNCDC       = 0;
const RDFUNC RDFUNCSine     = 1;
const RDFUNC RDFUNCSquare   = 2;
const RDFUNC RDFUNCTriangle = 3;
const RDFUNC RDFUNCRampUp   = 4;
const RDFUNC RDFUNCRampDown = 5;
const RDFUNC RDFUNCNoise    = 6;
const RDFUNC RDFUNCPulse    = 7;
const RDFUNC RDFUNCTrapezium= 8;
const RDFUNC RDFUNCSinePower= 9;
const RDFUNC RDFUNCCustom   = 10;
const RDFUNC RDFUNCPlay     = 31;

// analog io channel node types
typedef BYTE RDANALOGIO;
const RDANALOGIO RDANALOGIOEnable       = 1;
const RDANALOGIO RDANALOGIOVoltage      = 2;
const RDANALOGIO RDANALOGIOCurrent      = 3;
const RDANALOGIO RDANALOGIOPower        = 4;
const RDANALOGIO RDANALOGIOTemperature  = 5;

typedef int RDAnalogOutNode;
const RDAnalogOutNode RDAnalogOutNodeCarrier  = 0;
const RDAnalogOutNode RDAnalogOutNodeFM       = 1;
const RDAnalogOutNode RDAnalogOutNodeAM       = 2;

typedef int RDAnalogOutMode;
const RDAnalogOutMode RDAnalogOutModeVoltage  = 0;
const RDAnalogOutMode RDAnalogOutModeCurrent  = 1;

typedef int RDAnalogOutIdle;
const RDAnalogOutIdle RDAnalogOutIdleDisable  = 0;
const RDAnalogOutIdle RDAnalogOutIdleOffset   = 1;
const RDAnalogOutIdle RDAnalogOutIdleInitial  = 2;

typedef int RDDigitalInClockSource;
const RDDigitalInClockSource RDDigitalInClockSourceInternal = 0;
const RDDigitalInClockSource RDDigitalInClockSourceExternal = 1;

typedef int RDDigitalInSampleMode;
const RDDigitalInSampleMode RDDigitalInSampleModeSimple   = 0;
// alternate samples: noise|sample|noise|sample|...
// where noise is more than 1 transition between 2 samples
const RDDigitalInSampleMode RDDigitalInSampleModeNoise    = 1;

typedef int RDDigitalOutOutput;
const RDDigitalOutOutput RDDigitalOutOutputPushPull   = 0;
const RDDigitalOutOutput RDDigitalOutOutputOpenDrain  = 1;
const RDDigitalOutOutput RDDigitalOutOutputOpenSource = 2;
const RDDigitalOutOutput RDDigitalOutOutputThreeState = 3; // for custom and random

typedef int RDDigitalOutType;
const RDDigitalOutType RDDigitalOutTypePulse      = 0;
const RDDigitalOutType RDDigitalOutTypeCustom     = 1;
const RDDigitalOutType RDDigitalOutTypeRandom     = 2;
const RDDigitalOutType RDDigitalOutTypeFSM        = 3;

typedef int RDDigitalOutIdle;
const RDDigitalOutIdle RDDigitalOutIdleInit     = 0;
const RDDigitalOutIdle RDDigitalOutIdleLow      = 1;
const RDDigitalOutIdle RDDigitalOutIdleHigh     = 2;
const RDDigitalOutIdle RDDigitalOutIdleZet      = 3;

RDAPI int RDEnumDeviceCount(DWORD * count);
RDAPI int RDEnumDeviceInfo (int i, char* Description,char* SerialNumber,FT_HANDLE *handle);
RDAPI int RDdeviceOpen(int i,FT_HANDLE *ftHandle);
RDAPI int RDdeviceClose(FT_HANDLE ftHandle);


RDAPI int RDAnalogInStatus(FT_HANDLE handle,RDState* sts);
RDAPI int RDAnalogInFrequencySet(FT_HANDLE handle,int fre);
RDAPI int RDAnalogInChannelRangeSet(FT_HANDLE handle,int channel,double range);
RDAPI int RDAnalogInChannelEnableSet(FT_HANDLE handle,int channel,bool enable);
RDAPI int RDAnalogInTriggerAutoTimeoutSet(FT_HANDLE handle, int timeout);//0
RDAPI int RDAnalogInTriggerSourceSet(FT_HANDLE handle,RDTRIGSRC trigsrc );//RDTRIGSRCDetectorAnalogIn
RDAPI int RDAnalogInTriggerTypeSet(FT_HANDLE handle, RDTRIGTYPE trigtype);
//        RDAnalogInTriggerChannelSet(ftHandle, m_scopeconfig.trigch);
RDAPI int RDAnalogInTriggerLevelSet(FT_HANDLE handle, double voltsLevel,int range);
RDAPI int RDAnalogInTriggerConditionSet(FT_HANDLE handle, RDTriggerSlope trigcond);
RDAPI int RDAnalogInBufferSizeSet(FT_HANDLE handle, int buffersize);
//        RDAnalogInTriggerHoldOffSet(ftHandle,m_scopeconfig.holdoff);
//        RDAnalogInTriggerHysteresisSet(ftHandle,m_scopeconfig.HysteresisLevel);
RDAPI int RDAnalogInConfigure(FT_HANDLE handle,bool run);
RDAPI int RDAnalogOutNodeEnableSet(FT_HANDLE handle,int ch, RDAnalogOutNode node, bool enable);
RDAPI int RDAnalogOutNodeFunctionSet(FT_HANDLE handle, int ch, RDAnalogOutNode node, RDFUNC func);
RDAPI int RDAnalogOutNodeFrequencySet(FT_HANDLE handle, int ch, RDAnalogOutNode node, int hzFrequency);
//RDAPI int RDAnalogOutNodeAmplitudeSet(FT_HANDLE handle, int ch, RDAnalogOutNode node, double vAmplitude);

//RDAPI int RDAnalogOutNodeOffsetSet(FT_HANDLE handle, int ch, RDAnalogOutNode node, double vOffset);//如果不加 void RDAnalogInStatus 会卡
RDAPI int RDAnalogOutNodeOffsetAmpSet(FT_HANDLE handle, int ch, RDAnalogOutNode node, double vOffset,double amp,uchar* CalArray);
RDAPI int RDAnalogOutNodeSymmetrySet(FT_HANDLE handle,int ch,RDAnalogOutNode node,double percentageSymmetry);
RDAPI int RDAnalogOutNodePhaseSet(FT_HANDLE handle,int ch,RDAnalogOutNode node,double degreePhase);
RDAPI int RDAnalogOutConfigure(FT_HANDLE handle, int ch, bool output);
RDAPI int RDAnalogOutNodeDataSet(FT_HANDLE handle,  int ch, RDAnalogOutNode node, double *rgdData, int cdData);

RDAPI int RDAnalogIOChannelNodeSet(FT_HANDLE handle,int ch,double value,uchar* CalArray) ;
RDAPI int RDAnalogIOChannelEnableSet(FT_HANDLE handle,int ch,int enable) ;

RDAPI int RDCalibrationWrite(FT_HANDLE handle,uchar *CalArray);
RDAPI int RDCalibrationRead(FT_HANDLE handle,uchar *CalArray);

RDAPI int AnalogInRead(FT_HANDLE handle,int ch,int size,char* RxBuffer,int *backsize);
RDAPI int RDAnalogInRead(FT_HANDLE handle,int ch, int size,double range, double *RxBuffer,uchar* CalArray,int *backsize);

//    int  RDDigitalInReset(FT_HANDLE handle);
//    int  RDDigitalInClockSourceSet(FT_HANDLE handle,RDDigitalInClockSource clocksource);
RDAPI int RDDigitalInDividerSet(FT_HANDLE handle,uint div);//div=MaxHz/samplerate
//    int  RDDigitalInSampleFormatSet(FT_HANDLE handle,int nBits);//nBits
//    int  RDDigitalInInputOrderSet(FT_HANDLE handle,int order);//# for Digital Discovery bit order: DIO24:39; with 32 bit sampling [DIO24:39 + DIN0:15]
RDAPI int RDDigitalInBufferSizeSet(FT_HANDLE handle,int buffersize);
RDAPI int RDDigitalInChannelSet(FT_HANDLE handle,int channel);

//    int  RDDigitalInSampleModeSet(FT_HANDLE handle,int samplemode);
//    int  RDDigitalInSampleSensibleSet(FT_HANDLE handle,int fs); //compression
//    int  RDDigitalInAcquisitionModeSet(FT_HANDLE handle,RDACQMODE acqmode);

RDAPI int RDDigitalInTriggerSourceSet(FT_HANDLE handle,RDTRIGSRC trigsrc);//RDDigitalInBufferSizeSet
RDAPI int RDDigitalInTriggerTypeSet(FT_HANDLE handle, RDTRIGTYPE type);//type=0 for slope 1 for future
RDAPI int RDDigitalInTriggerSlopeSet(FT_HANDLE handle,RDTriggerSlope slope);
RDAPI int RDDigitalInTriggerSet(FT_HANDLE handle,uint Rais,uint Fall);
RDAPI int RDDigitalInTriggerTimeoutSet(FT_HANDLE handle, int enable);

//    int  RDDigitalInTriggerPositionSet(FT_HANDLE handle,int cSamplesAfterTrigger);
//    int  RDDigitalInTriggerPrefillSet(FT_HANDLE handle,int cSamplesBeforeTrigger);
//    int  RDDigitalInTriggerAutoTimeoutSet(FT_HANDLE handle,int secTimeout);
//    int  RDDigitalInTriggerSet(FT_HANDLE handle,int fsLevelLow,int fsLevelHigh,int fsEdgeRise,int fsEdgeFall);

//    int  RDDigitalInTriggerResetSet( FT_HANDLE handle,int fsLevelLow,int fsLevelHigh,int fsEdgeRise,int fsEdgeFall);
//    int  RDDigitalInTriggerCountSet( FT_HANDLE handle, int cCount, int fRestart);
//    int  RDDigitalInTriggerLengthSet( FT_HANDLE handle, int secMin,int secMax,int idxSync);
//    int  RDDigitalInTriggerMatchSet( FT_HANDLE handle,int iPin, int fsMask,int fsValue, int cBitStuffing);
RDAPI int  RDDigitalIOOutputEnableSet(FT_HANDLE handle,uint outputs);
RDAPI int  RDDigitalIOOutputSet(FT_HANDLE handle,uint sets);
RDAPI int  RDDigitalIOInputStatus(FT_HANDLE handle,uint* reads);
RDAPI int  RDDigitalInConfigure(FT_HANDLE handle,bool enable);
RDAPI int  RDDigitalInStatus(FT_HANDLE handle,RDState* sts);
RDAPI int  RDDigitalInRead(FT_HANDLE handle,int size,UINT16* RxBuffer,int *backsize);

//RDAPI int RDDigitalOutReset(FT_HANDLE handle);
RDAPI int RDDigitalOutRun(FT_HANDLE handle,bool enable);//run
//RDDigitalOutStatus(FT_HANDLE handle, DwfState *psts);

    // Configuration:
RDAPI int RDDigitalOutTriggerSourceSet(FT_HANDLE handle, RDTRIGSRC trigsrc);
//RDDigitalOutRunSet(FT_HANDLE handle, m_patternconfig.secRun);
//RDDigitalOutWaitSet(FT_HANDLE handle, m_patternconfig.secWait);
//RDDigitalOutRepeatSet(FT_HANDLE handle, m_patternconfig.cRepeat);
RDAPI int RDDigitalOutTriggerSlopeSet(FT_HANDLE handle, RDTriggerSlope slope);
//RDAPI int RDDigitalOutRepeatTriggerSet(FT_HANDLE handle,m_patternconfig.fRepeatTrigger);
//RDAPI int RDDigitalOutCount(FT_HANDLE handle, &m_patternconfig.pcChannel);
RDAPI int RDDigitalOutEnableSet(FT_HANDLE handle, uint chs);
    //RDDigitalOutOutputSet(FT_HANDLE handle,i, m_patternconfig.output.at(i));
RDAPI int RDDigitalOutTypeSet(FT_HANDLE handle,int ch,RDDigitalOutType type);
RDAPI int RDDigitalOutIdleSet(FT_HANDLE handle,int ch, RDDigitalOutIdle idle);
RDAPI int RDDigitalOutDividerInitSet(FT_HANDLE handle,int ch, uint divinit);
RDAPI int RDDigitalOutDividerSet(FT_HANDLE handle,int ch, uint div);
RDAPI int RDDigitalOutCounterInitSet(FT_HANDLE handle,int ch,int initlevel,uint counter); //1 counter=25ns
RDAPI int RDDigitalOutCounterSet(FT_HANDLE handle,int ch,  uint counter_l,uint counter_h);
//RDAPI int RDDigitalOutDataSet(FT_HANDLE handle,int ch, uchar* rgdSamples ,uint countOfBits);

RDAPI int RDDigitalUartRateSet(FT_HANDLE handle, double rate); // 9.6kHz
RDAPI int RDDigitalUartTxRxIOSet(FT_HANDLE handle, int TxDIO, int RxDIO); // RX = DIO-0
RDAPI int RDDigitalUartBitsSet(FT_HANDLE handle, int bits); // 8 bits
RDAPI int RDDigitalUartParitySet(FT_HANDLE handle, int parity); // 0 none, 1 odd, 2 even
RDAPI int RDDigitalUartStopSet(FT_HANDLE handle, double stop); // 1 bit stop length
RDAPI int RDDigitalUartTx(FT_HANDLE handle, uchar* data, int length);
RDAPI int RDDigitalUartRx(FT_HANDLE handle, uchar* rgRX, int length, int * rxcount, int *fParity);
RDAPI int RDDigitalI2CRateSet(FT_HANDLE handle, double rate); //
RDAPI int RDDigitalI2CTxRxIOSet(FT_HANDLE handle, int SCLDIO, int SDADIO); // SCLDIO = DIO-0
RDAPI int RDDigitalI2CTx(FT_HANDLE handle,uchar addr, uchar* data, int length);
RDAPI int RDDigitalI2CRx(FT_HANDLE handle,uchar addr, uchar* rgRX, int length, int * rxcount, int *fParity);
RDAPI int RDDigitalSPIRateSet(FT_HANDLE handle, double rate); //
RDAPI int RDDigitalSPITxRxIOSet(FT_HANDLE handle, int CSDIO,int ClockDIO,int DQ0, int DQ1); // RX = DIO-0
RDAPI int RDDigitalSPITx(FT_HANDLE handle, uchar* data, int length);
RDAPI int RDDigitalSPIRx(FT_HANDLE handle, uchar* rgRX, int length, int * rxcount, int *fParity);

RDAPI int write(FT_HANDLE handle, uchar *data, int count);
RDAPI int read(FT_HANDLE handle, uchar *data, int *count, int msTimeout=0);


#endif // INSTRUMENTSPLAYGROUND_H
