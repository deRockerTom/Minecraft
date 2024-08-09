import win32gui
import win32api
import win32con
import keyboard
from time import sleep

exitProgram = False

CLICK_TIMING = 0.8


def quit():
    global exitProgram
    exitProgram = True


keyboard.add_hotkey("ctrl+q", lambda: quit())


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

    win32gui.SendMessage(window, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
    win32gui.SendMessage(window, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, lParam)


while not exitProgram:
    click()
    sleep(CLICK_TIMING)
