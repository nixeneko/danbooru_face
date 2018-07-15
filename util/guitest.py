#!/usr/bin/env python3
# coding: utf-8

import sys, io
import wx

#stdoutがutf-8でないときに対応するおまじない
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,
                              encoding=sys.stdout.encoding, 
                              errors='backslashreplace', 
                              line_buffering=sys.stdout.line_buffering)

#! /usr/bin/env python

# rename.py

import wx

ID_QUIT = 1

class Annotator(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(800, 600))
            # TODO: Size should be of the last execution
        
        #font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)
        
        # Menu Bar
        menubar = wx.MenuBar()
        
        #File menu
        file = wx.Menu()
        quit = wx.MenuItem(file, ID_QUIT, '&Quit\tCtrl+Q')
        file.Append(quit)
        self.Bind(wx.EVT_MENU, self.OnQuit, id = ID_QUIT)
        menubar.Append(file, '&File')

        self.SetMenuBar(menubar)
        
        # Main Panel
        panel = wx.Panel(self, -1)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        
        # Left panel to show an image
        #img_panel = wx.ScrolledWindow(panel)
        img_panel = wx.TextCtrl(self, -1)
        hbox.Add(img_panel, 1, wx.EXPAND | wx.ALL, 5)
        
        # Right panel to show settings and info
        sett_panel = wx.Panel(self, -1)
        vbox1 = wx.BoxSizer(wx.VERTICAL)
        st1 = wx.StaticText(sett_panel, -1, 'Rectangles:')
        
        vbox1.Add(st1, 0, wx.RIGHT, 0)
        sett_panel.SetSizer(vbox1)
        
        hbox.Add(sett_panel, 0)
        
        
        self.statusbar = self.CreateStatusBar()

        panel.SetSizer(hbox)
        self.Centre()
        self.Show(True)
        
    def OnQuit(self, event):
        # TODO: Must confirm to save or discard some changes
        self.Close()



if __name__ == '__main__':
    
    app = wx.App()
    Annotator(None, -1, 'Annotator')
    app.MainLoop()
    