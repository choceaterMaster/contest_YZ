import base64

import serial
import serial.tools.list_ports

class mySerial():
    global ser
    def findSerial(self):
        str = ''
        str2 = ''
        ports_list = list(serial.tools.list_ports.comports())
        if len(ports_list) <= 0:
            str = "无串口设备。"
        else:
            str = "可用的串口设备如下："
            for comport in ports_list:
                str2 = list(comport)[0], list(comport)[1]
        return str, str2


    def openSerial(COM):  # 默认波特率115200
        # 方式1：调用函数接口打开串口时传入配置参数
        tmp = ''
        ser = serial.Serial(COM, 115200)  # 打开COM17，将波特率配置为115200，其余参数使用默认值
        if ser.isOpen():  # 判断串口是否成功打开
            # print("打开串口成功。")
            # print(ser.name)  # 输出串口号
            tmp = ser.name  # 返回串口号
        else:
            tmp = False
        return tmp

    def closeSerial(self):
        ser.close()
        if ser.isOpen():  # 判断串口是否关闭
            print("串口未关闭。")
        else:
            print("串口已关闭。")
    def write(str):
        # 串口发送 ABCDEFG，并输出发送的字节数。
        write_len = ser.write(str.encode('utf-8'))
        print("串口发出{}个字节。".format(write_len))
    def read(self):#方案一                             ###还没写完！！！！！！！！！！！！！
        tmp=''
        while True:
            com_input = ser.read(10)
            if com_input:  # 如果读取结果非空，则输出
                tmp=tmp+com_input

    def recv(serial):#方案二
        while True:
            data = serial.read_all()
            if data == '':
                continue
            else:
                break
            sleep(0.02)
        return data
