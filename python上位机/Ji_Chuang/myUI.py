import wx
from mySerial import *
import myRD

frame_width = 1200
frame_height = 800


class ExamplePanel(wx.Panel):
    def __init__(self, parent):
        self.rd = myRD.myRD()

        wx.Panel.__init__(self, parent)
        self.quote = wx.StaticText(self, label="文本在这", pos=(60, 30))
        font = wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.quote.SetFont(font)
        # A multiline TextCtrl - This is here to show how the events work in this program, don't pay too much attention to it
        self.logger = wx.TextCtrl(self, pos=(60, 560), size=(1200 - 20 - 40 - 40, 160),
                                  style=wx.TE_MULTILINE | wx.TE_READONLY)
        font = wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        # button1
        self.button1 = wx.Button(self, label="获取设备信息", pos=(800, 40))
        self.Bind(wx.EVT_BUTTON, self.OnClickButton1, self.button1)
        self.button1.SetFont(font)
        self.button1.SetSize((140,50))
        # button2
        self.button2 = wx.Button(self, label="打开", pos=(800, 120))
        self.Bind(wx.EVT_BUTTON, self.OnClickButton2, self.button2)
        self.button2.SetFont(font)
        self.button2.SetSize((140, 50))
        # button3
        self.button3 = wx.Button(self, label="button3", pos=(800, 200))
        self.Bind(wx.EVT_BUTTON, self.OnClickButton3, self.button3)
        self.button3.SetFont(font)
        self.button3.SetSize((140, 50))

    def OnClickButton1(self, e):
        str = self.rd.getDeviceList()
        self.logger.AppendText('DeviceList: %s\n'  % str)
        print("str=",str)
    def OnClickButton2(self, e):
        str1=self.rd.openDevice()
        self.logger.AppendText('open status: %s\n' % str1)
        print("str1=",str1)
    def OnClickButton3(self, e):
        pass


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
        pass

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
