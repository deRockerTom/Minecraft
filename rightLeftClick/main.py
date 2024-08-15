import win32gui
import win32api
import win32con
import keyboard
from time import sleep

exitProgram = False
launch = False

CLICK_TIMING = 0.1


def quit():
    global exitProgram
    exitProgram = True


def launch_click():
    global launch
    launch = not launch


keyboard.add_hotkey("ctrl+q", lambda: quit())
keyboard.add_hotkey("²", lambda: launch_click())


def find_minecraft_process(hwnd, process_ids):
    text = win32gui.GetWindowText(hwnd)
    if "Minecraft 1." in text:
        process_ids.append(hwnd)


win32gui.EnumWindows(find_minecraft_process, process_id := [])

if len(process_id) == 0:
    print("Minecraft not found")
    exit(1)

if len(process_id) > 1:
    print("Multiple minecraft instances found, using the first one")

print(f"Using process {win32gui.GetWindowText(process_id[0])}")

window = process_id[0]


def click() -> None:
    """
    Click the mouse on the minecraft window
    """
    lParam = win32api.MAKELONG(100, 100)
    win32gui.SendMessage(window, win32con.WM_RBUTTONDOWN, win32con.MK_LBUTTON, lParam)
    win32gui.SendMessage(window, win32con.WM_RBUTTONUP, win32con.MK_LBUTTON, lParam)
    sleep(CLICK_TIMING)
    win32gui.SendMessage(window, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
    win32gui.SendMessage(window, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, lParam)


while not exitProgram:
    sleep(0.1)
    if launch:
        print("Launching")
        for i in range(0x31, 0x3A):
            lParam = win32api.MAKELONG(100, 100)
            win32api.SendMessage(window, win32con.WM_KEYDOWN, i, 0)
            win32api.SendMessage(window, win32con.WM_KEYUP, i, 0)
            sleep(CLICK_TIMING)
            for j in range(64):
                click()
                sleep(CLICK_TIMING)
                if exitProgram or not launch:
                    break
            if exitProgram or not launch:
                break
        launch = False
