import win32gui
import win32api
import win32con
import keyboard
from time import sleep

exitProgram = False


def quit():
    global exitProgram
    exitProgram = True


keyboard.add_hotkey("ctrl+q", lambda: quit())


window = win32gui.FindWindow(None, "Minecraft 1.21 - Blocaria - Boxed")
lParam = win32api.MAKELONG(100, 100)

win32gui.SendMessage(window, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)

while not exitProgram:
    sleep(0.1)

win32gui.SendMessage(window, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, lParam)
