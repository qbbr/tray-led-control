#!/usr/bin/env python3

from builtins import staticmethod

import wx
import wx.adv
import argparse

import const
from arduino import send, start_reading_loop, init_serial, stop
from helpers import d


class TaskBarIcon(wx.adv.TaskBarIcon):
    def __init__(self, frame):
        wx.adv.TaskBarIcon.__init__(self)
        self.myapp_frame = frame
        self.set_icon(const.TRAY_ICON)
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)

    def set_icon(self, path):
        icon = wx.Icon(wx.Bitmap(path))
        self.SetIcon(icon, const.TRAY_TOOLTIP)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        self.create_menu_item(menu, "Set color", -1, self.on_set_color)
        self.create_menu_item(menu, "Set mode", -1, self.on_set_mode)
        self.create_menu_item(menu, "Set brightness", -1, self.on_set_brightness)
        self.create_menu_item(menu, "Set speed", -1, self.on_set_speed)
        self.create_menu_item(menu, "Send custom CMD", -1, self.on_send_custom_cmd)
        menu.AppendSeparator()
        self.create_menu_item(menu, "Exit", -1, self.on_exit)
        return menu

    @staticmethod
    def create_menu_item(menu, label, id, func):
        item = wx.MenuItem(menu, id, label)
        menu.Bind(wx.EVT_MENU, func, id=item.GetId())
        menu.Append(item)
        return item

    @staticmethod
    def on_left_down(event):
        d("Tray icon was left-clicked.")

    def on_set_color(self, event):
        dlg = wx.ColourDialog(self.myapp_frame)
        dlg.GetColourData().SetChooseFull(True)
        dlg.GetColourData().SetColour(const.CURRENT_COLOR)
        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetColourData()
            rgb = data.GetColour().Get()
            const.CURRENT_COLOR[0] = rgb[0]
            const.CURRENT_COLOR[1] = rgb[1]
            const.CURRENT_COLOR[2] = rgb[2]
            # hex_color = "%02x%02x%02x" % rgb[:3]
            color = "%d.%d.%d" % rgb[:3]
            send("c %s" % color)
        dlg.Destroy()

    def on_set_mode(self, event):
        choices = list(const.Modes.get_all_const().keys())
        dlg = wx.SingleChoiceDialog(self.myapp_frame, "Modes", "Set mode", choices)
        dlg.SetSelection(const.CURRENT_MODE)
        if dlg.ShowModal() == wx.ID_OK:
            choice = dlg.GetStringSelection()
            const.CURRENT_MODE = getattr(const.Modes, choice)
            send("m %d" % const.CURRENT_MODE)
        dlg.Destroy()

    def on_set_brightness(self, event):
        dlg = wx.NumberEntryDialog(self.myapp_frame, "Enter brightness", "Value", "Enter brightness",
                                   const.CURRENT_BRIGHTNESS, 0, 255)
        if dlg.ShowModal() == wx.ID_OK:
            const.CURRENT_BRIGHTNESS = dlg.GetValue()
            send("b %s" % const.CURRENT_BRIGHTNESS)
        dlg.Destroy()

    def on_set_speed(self, event):
        dlg = wx.NumberEntryDialog(self.myapp_frame, "Enter speed", "Value", "Enter speed", const.CURRENT_SPEED, 10,
                                   65535)
        if dlg.ShowModal() == wx.ID_OK:
            const.CURRENT_SPEED = dlg.GetValue()
            send("s %s" % const.CURRENT_SPEED)
        dlg.Destroy()

    def on_send_custom_cmd(self, event):
        dlg = wx.TextEntryDialog(self.myapp_frame, "Custom CMD", "CMD")
        if dlg.ShowModal() == wx.ID_OK:
            send(dlg.GetValue())
        dlg.Destroy()

    def on_exit(self, event):
        d("exit btn clicker")
        self.myapp_frame.Close()


class MyApplication(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "", size=(1, 1))
        # panel = wx.Panel(self)
        self.myapp = TaskBarIcon(self)
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def on_close(self, event):
        d("destroy app")
        stop()
        self.myapp.RemoveIcon()
        self.myapp.Destroy()
        self.Destroy()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tray App for control LED strip WS2812B over Arduino serial port.")
    parser.add_argument("--port", help="arduino serial port (default: %s)" % const.ARDUINO_PORT, default=const.ARDUINO_PORT)
    parser.add_argument("--debug", help="enable debug output to console", action='count', default=0)
    args = parser.parse_args()

    const.ARDUINO_PORT = args.port

    if args.debug:
        const.DEBUG_CONSOLE_OUTPUT = True

    init_serial()
    start_reading_loop()

    MyApp = wx.App()
    MyApplication()
    MyApp.MainLoop()
