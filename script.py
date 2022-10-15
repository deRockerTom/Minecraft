import mouse
import time
from pythmc import GameLink
import math
import re
import os

client = GameLink()

client.DROP = "a"
client.WALK_FWD = "z"
client.WALK_BWD = "s"
client.WALK_LEFT = "q"
client.WALK_RIGHT = "d"

client.HOTBAR_1 = "&"
client.HOTBAR_2 = "é"
client.HOTBAR_3 = '"'
client.HOTBAR_4 = "'"
client.HOTBAR_5 = "("
client.HOTBAR_6 = "-"
client.HOTBAR_7 = "è"
client.HOTBAR_8 = "_"
client.HOTBAR_9 = "ç"

client.HOTBAR_SLOTS = [client.HOTBAR_1, client.HOTBAR_2, client.HOTBAR_3, client.HOTBAR_4,
                       client.HOTBAR_5, client.HOTBAR_6, client.HOTBAR_7, client.HOTBAR_8, client.HOTBAR_9]

FLAGS = re.MULTILINE


class Message:

    def __init__(self, *args):

        self.content = args[0]
        self.id = args[1]


def get_history(limit=math.factorial(16)):
    # with open("2022-10-08-3.li")
    with open(os.path.join(os.getenv("APPDATA"), ".minecraft", "logs", "latest.log"), errors='replace') as log_file:
        log_history = log_file.readlines()
    message_list = parse_chat_messages(log_history, limit)
    return message_list


def parse_chat_messages(log_history, limit):
    requested_messages = list()
    counter = 0
    for line in reversed(log_history):
        if counter >= limit:
            break
        if not re.search("\[(.*(CHAT))\]", line, flags=FLAGS):
            continue

        message = re.split("\[(.*(CHAT))\]", line, flags=FLAGS)[-1].strip()
        if not message:
            continue
        line_number = log_history.index(line) + 1

        requested_messages.append(Message(message, line_number))
        counter += 1

    if not requested_messages:
        return None
    return reversed(requested_messages)


for i in range(60*60):
    for message in get_history(1):
        if message.content == "Pong !":
            exit()
    for message in get_history(2):
        if "Téléportation" in message.content or "téléporté" in message.content:
            exit()
    client.attack()
    time.sleep(0.5)
    if i % 300 == 0 and i != 0:
        mouse._os_mouse.move_relative(5, 0)
        time.sleep(0.5)
        mouse._os_mouse.move_relative(-5, 0)
        client.hotbar(2)
        client.use(2)
        client.hotbar(5)
