import wx
from mySerial import *
import myRD

frame_width = 1200
frame_height = 800


class ExamplePanel(wx.Panel):
    def __init__(self, parent):
        self.rd = myRD.myRD()
        wx.Panel.__init__(self, parent)
        # self.quote = wx.StaticText(self, label="文本在这", pos=(60, 30))
        font = wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        # self.quote.SetFont(font)
        # button0
        self.button0 = wx.Button(self, label="打开视频流", pos=(60, 30))
        self.Bind(wx.EVT_BUTTON, self.OnClickButton0, self.button0)
        self.button0.SetFont(font)
        self.button0.SetSize((140, 50))

            # A multiline TextCtrl - This is here to show how the events work in this program, don't pay too much attention to it
        self.logger = wx.TextCtrl(self, pos=(60, 560), size=(1200 - 20 - 40 - 40, 160),
                                  style=wx.TE_MULTILINE | wx.TE_READONLY)
        font = wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        # button1
        self.button1 = wx.Button(self, label="获取设备信息", pos=(800, 40))
        self.Bind(wx.EVT_BUTTON, self.OnClickButton1, self.button1)
        self.button1.SetFont(font)
        self.button1.SetSize((140, 50))
        # button2
        self.button2 = wx.Button(self, label="打开设备", pos=(800, 120))
        self.Bind(wx.EVT_BUTTON, self.OnClickButton2, self.button2)
        self.button2.SetFont(font)
        self.button2.SetSize((140, 50))
        # button3
        self.button3 = wx.Button(self, label="关闭", pos=(800, 200))
        self.Bind(wx.EVT_BUTTON, self.OnClickButton3, self.button3)
        self.button3.SetFont(font)
        self.button3.SetSize((140, 50))
        # button4
        self.button4 = wx.Button(self, label="处理(FPGA)", pos=(800, 280))
        self.Bind(wx.EVT_BUTTON, self.OnClickButton4, self.button4)
        self.button4.SetFont(font)
        self.button4.SetSize((140, 50))
        # button5
        self.button5 = wx.Button(self, label="处理(上位机)", pos=(980, 280))
        self.Bind(wx.EVT_BUTTON, self.OnClickButton5, self.button5)
        self.button5.SetFont(font)
        self.button5.SetSize((140, 50))
        # button6
        self.button6 = wx.Button(self, label="中断视频流", pos=(800, 360))
        self.Bind(wx.EVT_BUTTON, self.OnClickButton6, self.button6)
        self.button6.SetFont(font)
        self.button6.SetSize((140, 50))

    def OnClickButton0(self, e):
        str = self.rd.openCamera()
        self.logger.AppendText('open ov5640 status: %s\n' % str)
        print("open ov5640 status:", str)
    def OnClickButton1(self, e):
        str = self.rd.getDeviceList()
        self.logger.AppendText('DeviceList: %s\n' % str)
        print("DeviceList:", str)

    def OnClickButton2(self, e):
        str1 = self.rd.openDevice()
        self.logger.AppendText('open status: %s\n' % str1)
        print("open status: ", str1)

    def OnClickButton3(self, e):
        int1 = self.rd.closeDevice()
        self.logger.AppendText(('close device status: %d\n' % int1))
        print("close device status:", int1)

    def OnClickButton4(self, e):
        tmp = self.rd.imageProcess_FPGA()
        self.logger.AppendText(('image process status(FPGA): %s \n' % tmp))
        print("image process status(FPGA): ", tmp)

    def OnClickButton5(self, e):
        tmp = self.rd.imageProcess_cv()
        self.logger.AppendText(('image process status(cv): %s \n' % tmp))
        print("image process status(cv): ", tmp)

    def OnClickButton6(self, e):
        tmp = self.rd.shutStream()
        self.logger.AppendText(('shut down stream status: %s \n' % tmp))
        print("shut down stream status: ", tmp)

class MainWindow(wx.Frame):
    """We simply derive a new class of Frame."""
    _info = ''
    _device = ''

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(frame_width, frame_height))

        # 串口信息
        _info, _device = mySerial.findSerial(None)

        # 设置菜单
        filemenu = wx.Menu()

        # wx.ID_ABOUT和wx.ID_EXIT是wxWidgets提供的标准ID
        menuOpenSerial = filemenu.Append(wx.ID_OPEN, "检测串口", "check COM")
        menuAbout = filemenu.Append(wx.ID_ABOUT, "&About", " Information about this program")  # (ID, 项目名称, 状态栏信息)
        filemenu.AppendSeparator()
        menuExit = filemenu.Append(wx.ID_EXIT, "E&xit", " Terminate the program")  # (ID, 项目名称, 状态栏信息)

        # 创建菜单栏
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File")  # 在菜单栏中添加filemenu菜单
        self.SetMenuBar(menuBar)  # 在frame中添加菜单栏

        # 设置events
        self.Bind(wx.EVT_MENU, self.OnFindSerial, menuOpenSerial)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)

    def OnAbout(self, e):
        dlg=wx.MessageDialog(self,"小组：摸鱼大队\n成员：宗圣康，谢旭杰，夏俊韬","队伍信息",wx.OK)
        dlg.ShowModal()

    def OnFindSerial(self, e):
        _info, _device = mySerial.findSerial(None)
        dlg = wx.MessageDialog(self, "串口信息如下：" + _info, "标题" + _device, wx.OK)
        dlg.ShowModal()  # 显示对话框
        # dlg.Destroy()  # 当结束之后关闭对话框

    def OnExit(self, e):
        self.Close(True)  # 关闭整个frame


app = wx.App(False)
frame = MainWindow(None, "frame")
panel = ExamplePanel(frame)
frame.Show()
app.MainLoop()
