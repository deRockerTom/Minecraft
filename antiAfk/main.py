from time import sleep
import keyboard
import mouse
from random import randint

exitProgram = False


def quit():
    global exitProgram
    exitProgram = True


keyboard.add_hotkey("ctrl+q", lambda: quit())

while not exitProgram:
    sleep(60)
    x = randint(5, 15)
    y = randint(5, 15)
    print("Checking")
    for j in range(max(x, y)):
        mouse._os_mouse.move_relative(j < x and 2 or 0, j < y and -2 or 0)
        sleep(0.02)
    sleep(0.2)
    for j in range(max(x, y)):
        mouse._os_mouse.move_relative(j < x and -2 or 0, j < y and 2 or 0)
        sleep(0.02)
