# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 16:42:42 2022

@author: jackscl
"""

#typedef BYTE RDTRIGSRC;
RDTRIGSRCNone                  = 0;
RDTRIGSRCDetectorAnalogInCH1   = 1;
RDTRIGSRCDetectorAnalogInCH2   = 2;
RDTRIGSRCAnalogOut1            = 3;
RDTRIGSRCAnalogOut2            = 4;
RDTRIGSRCDetectorDigitalIn     = 5;
RDTRIGSRCDigitalOut            = 6;
RDTRIGSRCManule                = 7;
RDTRIGSRCExternal1             = 8;
RDTRIGSRCExternal2             = 9;
RDTRIGSRCDigitalIn              =10;


# instrument states:
#typedef BYTE RDState;
RDStateReady        = 0;
RDStateConfig       = 4;
RDStatePrefill      = 5;
RDStateArmed        = 1;
RDStateWait         = 7;
RDStateTriggered    = 3;
RDStateRunning      = 3;
RDStateDone         = 2;


# acquisition modes:
#typedef int RDACQMODE;
RDACQMODESingle     = 0;
RDACQMODEScanShift  = 1;
RDACQMODEScanScreen = 2;
RDACQMODERecord     = 3;
RDACQMODEOvers      = 4;
RDACQMODESingle1    = 5;

# analog acquisition RDFILTER:
#typedef int RDFILTER;
RDFILTERDecimate = 0;
RDFILTERAverage  = 1;
RDFILTERMinMax   = 2;

# analog acquisition RDFILTER:
#typedef int RDTriggerSlope;
RDTriggerSlopeRise   = 0;
RDTriggerSlopeFall   = 1;
RDTriggerSlopeEdge   = 2;

# analog in trigger mode:
#typedef int RDTRIGTYPE;
RDTRIGTYPEEdge         = 0;
RDTRIGTYPEPulse        = 1;
RDTRIGTYPETransition   = 2;


# analog in trigger length condition
#typedef int RDTRIGLEN;
RDTRIGLENLess       = 0;
RDTRIGLENTimeout    = 1;
RDTRIGLENMore       = 2;

# error codes for RD Public API:
#typedef int RDERC;
RDercNoErc                  = 0;        #  No error occurred
RDercUnknownError           = 1;        #  API waiting on pending API timed out
RDercApiLockTimeout         = 2;        #  API waiting on pending API timed out
RDercAlreadyOpened          = 3;        #  Device already opened
RDercNotSupported           = 4;        #  Device not supported
RDercInvalidParameter0      = 0x10;     #  Invalid parameter sent in API call
RDercInvalidParameter1      = 0x11;     #  Invalid parameter sent in API call
RDercInvalidParameter2      = 0x12;     #  Invalid parameter sent in API call
RDercInvalidParameter3      = 0x13;     #  Invalid parameter sent in API call
RDercInvalidParameter4      = 0x14;     #  Invalid parameter sent in API call

# analog out signal types
#typedef BYTE RDFUNC;
RDFUNCDC       = 0;
RDFUNCSine     = 1;
RDFUNCSquare   = 2;
RDFUNCTriangle = 3;
RDFUNCRampUp   = 4;
RDFUNCRampDown = 5;
RDFUNCNoise    = 6;
RDFUNCPulse    = 7;
RDFUNCTrapezium= 8;
RDFUNCSinePower= 9;
RDFUNCCustom   = 10;
RDFUNCPlay     = 31;

# analog io channel node types
#typedef BYTE RDANALOGIO;
RDANALOGIOEnable       = 1;
RDANALOGIOVoltage      = 2;
RDANALOGIOCurrent      = 3;
RDANALOGIOPower        = 4;
RDANALOGIOTemperature  = 5;

#typedef int RDAnalogOutNode;
RDAnalogOutNodeCarrier  = 0;
RDAnalogOutNodeFM       = 1;
RDAnalogOutNodeAM       = 2;

#typedef int RDAnalogOutMode;
RDAnalogOutModeVoltage  = 0;
RDAnalogOutModeCurrent  = 1;

#typedef int RDAnalogOutIdle;
RDAnalogOutIdleDisable  = 0;
RDAnalogOutIdleOffset   = 1;
RDAnalogOutIdleInitial  = 2;

#typedef int RDDigitalInClockSource;
RDDigitalInClockSourceInternal = 0;
RDDigitalInClockSourceExternal = 1;

#typedef int RDDigitalInSampleMode;
RDDigitalInSampleModeSimple   = 0;
# alternate samples: noise|sample|noise|sample|...
# where noise is more than 1 transition between 2 samples
RDDigitalInSampleModeNoise    = 1;

#typedef int RDDigitalOutOutput;
RDDigitalOutOutputPushPull   = 0;
RDDigitalOutOutputOpenDrain  = 1;
RDDigitalOutOutputOpenSource = 2;
RDDigitalOutOutputThreeState = 3; # for custom and random

#typedef int RDDigitalOutType;
RDDigitalOutTypePulse      = 0;
RDDigitalOutTypeCustom     = 1;
RDDigitalOutTypeRandom     = 2;
RDDigitalOutTypeFSM        = 3;

#typedef int RDDigitalOutIdle;
RDDigitalOutIdleInit     = 0;
RDDigitalOutIdleLow      = 1;
RDDigitalOutIdleHigh     = 2;
RDDigitalOutIdleZet      = 3;