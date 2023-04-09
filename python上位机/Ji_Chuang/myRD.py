from pyRD import RD
from pyRD.core.RDconstant import *
import matplotlib.pyplot as plt
import numpy as np
import time
import sys, os
import pathlib

py_path, py_name = os.path.split(os.path.abspath(__file__))

base_dir = pathlib.Path(py_path).absolute().parent  # sys.argv[0]

if sys.path.count(base_dir) == 0:
    sys.path.append(str(base_dir))
class myRD():

    def __init__(self):
        self.rd = RD()
        self.rd.DeviceEnumLists()
        print("初始化成功")

    def getDeviceList(self):
        return self.rd.devicelist

    def openDevice(self): #成功则返回句柄，失败返回"error"
        try:
            status = self.rd.DeviceOpen(0)
            return status
        except:
            return "error"
