import os
import math
import re
from pythmc import ChatLink
from random import random
import time

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


def cheat():
    chat = ChatLink()
    while True:
        message = get_history(3)
        reponse = 0
        toSend = ""
        toConsider = True
        for i in message:
            if reponse != 0:
                print(i.content)
                if reponse == 1:
                    toSend = i.content[1:len(i.content)-1]
                if reponse == 2:
                    toSend = str(
                        eval(i.content[1:len(i.content)-1].replace("x", "*")))
                if reponse == 3:
                    toSend = i.content[1:len(i.content)-1][::-1]
                break
            if "Le premier à taper la suite de" in i.content:
                print(i.id)
            if "caractères suivantes gagne!" in i.content:
                print(i.id)
                reponse = 1
            if "Le premier à taper le mot suivant gagne!" in i.content:
                print(i.id)
                reponse = 1
            if "Le premier à résoudre ce calcul gagne!" in i.content:
                print(i.id)
                reponse = 2
            if "Le premier à déchiffrer le mot suivant" in i.content:
                print(i.id)
                toConsider = False
            if "Le premier à démêler et à remettre dans" in i.content:
                print(i.id)
                toConsider = False
            if "Le premier à remettre les mots suivants" in i.content:
                print(i.id)
                toConsider = False
            elif i.content == "gagne!":
                if toConsider:
                    print(i.id)
                    reponse = 3
                else:
                    toConsider = True
                    time.sleep(300)
        if toSend != "":
            print(toSend)
            rand = random()
            time.sleep(max(len(toSend)*0.15 + rand/5, 1.5 + rand))
            print(rand)
            chat.send(toSend)
            break


if __name__ == "__main__":
    cheat()
    # messages = get_history(100)
    # for i in messages:
    #     print(i.content)
