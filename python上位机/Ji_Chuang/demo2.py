# -*- coding: utf-8 -*-
"""
http://blog.csdn.net/chenghit
"""
import wx
import os

class MainWindow(wx.Frame):
    """We simply derive a new class of Frame."""
    def __init__(self, parent, title):
        self.dirname = ''

        # "-1"这个尺寸参数意味着通知wxWidget使用默认的尺寸
        # 在这个例子中，我们使用200像素的宽度，和默认的高度
        wx.Frame.__init__(self, parent, title = title, size = (200, -1))
        self.control = wx.TextCtrl(self, style = wx.TE_MULTILINE)
        self.CreateStatusBar()    # 创建位于窗口的底部的状态栏

        # 设置菜单
        filemenu = wx.Menu()

        # wx.ID_ABOUT和wx.ID_EXIT是wxWidgets提供的标准ID
        menuOpen = filemenu.Append(wx.ID_OPEN, "&Open", " Open a file")
        menuAbout = filemenu.Append(wx.ID_ABOUT, "&About", \
            " Information about this program")    # (ID, 项目名称, 状态栏信息)
        filemenu.AppendSeparator()
        menuExit = filemenu.Append(wx.ID_EXIT, "E&xit", \
            " Terminate the program")    # (ID, 项目名称, 状态栏信息)

        # 创建菜单栏
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File")    # 在菜单栏中添加filemenu菜单
        self.SetMenuBar(menuBar)    # 在frame中添加菜单栏

        # 设置events
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)

        # 设置sizers
        self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.buttons = []
        for i in range(0, 6):
            self.buttons.append(wx.Button(self, -1, "Button &" + str(i)))
            self.sizer2.Add(self.buttons[i], 1, wx.SHAPED)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.control, 1, wx.EXPAND)
        self.sizer.Add(self.sizer2, 0, wx.GROW)

        # 激活sizer
        self.SetSizer(self.sizer)
        self.SetAutoLayout(True)
        self.sizer.Fit(self)
        self.Show(True)

    def OnAbout(self, e):
        # 创建一个带"OK"按钮的对话框。wx.OK是wxWidgets提供的标准ID
        dlg = wx.MessageDialog(self, "A small text editor.", \
            "About Sample Editor", wx.OK)    # 语法是(self, 内容, 标题, ID)
        dlg.ShowModal()    # 显示对话框
        dlg.Destroy()    # 当结束之后关闭对话框

    def OnExit(self, e):
        self.Close(True)    # 关闭整个frame

    def OnOpen(self, e):
        """ open a file. """
        # wx.FileDialog语法：(self, parent, message, defaultDir, defaultFile,
        #                    wildcard, style, pos)
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*",
                            wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            f = open(os.path.join(self.dirname, self.filename), 'r') # 暂时只读
            self.control.SetValue(f.read())
            f.close()
        dlg.Destroy()

app = wx.App(False)
frame = MainWindow(None, title = "Small editor")
app.MainLoop()