from Screenshot import Screenshot
from Images import Images
from time import sleep
from Fish import Fish
import win32gui
import win32api
import win32con
import keyboard

FISHING_ROD__TOP = 1315
FISHING_ROD__HEIGHT = 70
FISHING_ROD__LEFT = 925
FISHING_ROD__WIDTH = 70

AQUARIUM_BAR__TOP = 675
AQUARIUM_BAR__HEIGHT = 700
AQUARIUM_BAR__LEFT = 2230
AQUARIUM_BAR__WIDTH = 50

AQUARIUM__TOP = 710
AQUARIUM__HEIGHT = 100
AQUARIUM__LEFT = 300
AQUARIUM__WIDTH = 1975

FISHING_ROD_PATHS = [
    "data\\launched_fishing_rod.png",
    "data\\unlaunched_fishing_rod.png",
]

AQUARIUM_PATH = "data\\aquarium.png"

TMP_AQUARIUM_PATH = "screenshots\\aquarium_screenshot.png"

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


def click() -> None:
    """
    Click the mouse on the minecraft window
    """
    window = win32gui.FindWindow(None, "Minecraft 1.21 - Blocaria - Boxed")
    lParam = win32api.MAKELONG(100, 100)

    win32gui.SendMessage(window, win32con.WM_RBUTTONDOWN, win32con.MK_RBUTTON, lParam)
    win32gui.SendMessage(window, win32con.WM_RBUTTONUP, win32con.MK_RBUTTON, lParam)


# take_aquarium_screenshot()
while not exitProgram:
    sleep(0.2)
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
