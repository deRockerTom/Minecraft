from Screenshot import Screenshot
from Images import Images
from time import sleep
from Fish import Fish
import win32gui
import win32api
import win32con
import keyboard
from constants.constants import (
    FISHING_ROD__TOP,
    FISHING_ROD__HEIGHT,
    FISHING_ROD__LEFT,
    FISHING_ROD__WIDTH,
    AQUARIUM_BAR__TOP,
    AQUARIUM_BAR__HEIGHT,
    AQUARIUM_BAR__LEFT,
    AQUARIUM_BAR__WIDTH,
    AQUARIUM__TOP,
    AQUARIUM__HEIGHT,
    AQUARIUM__LEFT,
    AQUARIUM__WIDTH,
    FISHING_ROD_PATHS,
    AQUARIUM_PATH,
    TMP_AQUARIUM_PATH,
)

imagesHelper = Images()
fishHelper = Fish()

exitProgram = False


def quit():
    global exitProgram
    exitProgram = True


keyboard.add_hotkey("ctrl+q", lambda: quit())


def is_in_ui() -> bool:
    """
    Check if the player is in theaquarium ui.
    """
    imagesHelper = Images()
    aquarium_screenshot = Screenshot(
        path="screenshots\\aquarium_bar_screenshot.png",
        top=AQUARIUM_BAR__TOP,
        left=AQUARIUM_BAR__LEFT,
        width=AQUARIUM_BAR__WIDTH,
        height=AQUARIUM_BAR__HEIGHT,
    )

    aquarium_screenshot.take()

    return imagesHelper.is_close(
        reference=AQUARIUM_PATH, image=aquarium_screenshot.path
    )


def is_fishing() -> bool:
    """
    Check if the player is fishing.
    """
    fishing_rod_screenshot = Screenshot(
        path="screenshots\\fishing_rod_screenshot.png",
        top=FISHING_ROD__TOP,
        left=FISHING_ROD__LEFT,
        width=FISHING_ROD__WIDTH,
        height=FISHING_ROD__HEIGHT,
    )

    fishing_rod_screenshot.take()

    closest_fishing_rod = imagesHelper.find_nearest(
        reference=fishing_rod_screenshot.path, images=FISHING_ROD_PATHS
    )

    return closest_fishing_rod == FISHING_ROD_PATHS[0]


def take_aquarium_screenshot() -> None:
    """
    Take a screenshot of the aquarium.
    """
    aquarium_screenshot = Screenshot(
        path=TMP_AQUARIUM_PATH,
        top=AQUARIUM__TOP,
        left=AQUARIUM__LEFT,
        width=AQUARIUM__WIDTH,
        height=AQUARIUM__HEIGHT,
    )

    aquarium_screenshot.take()


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

    win32gui.SendMessage(window, win32con.WM_RBUTTONDOWN, win32con.MK_RBUTTON, lParam)
    win32gui.SendMessage(window, win32con.WM_RBUTTONUP, win32con.MK_RBUTTON, lParam)


while not exitProgram:
    sleep(0.1)
    is_ui = is_in_ui()

    if not is_ui:
        fishing = is_fishing()
        if not fishing:
            print("Not fishing, clicking")
            click()

    if is_ui:
        take_aquarium_screenshot()
        should_click = fishHelper.should_fish(TMP_AQUARIUM_PATH)
        if should_click:
            print("Should fish, clicking")
            click()
