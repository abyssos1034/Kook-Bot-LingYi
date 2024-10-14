import random

from khl import User

from .globals import *

def lucky(user: User) -> int:
    global g_lucky
    lucky_value = -1
    if user in g_lucky:
        lucky_value = g_lucky[user]
    else:
        lucky_value = random.randint(0, 100)
        g_lucky[user] = lucky_value
    return lucky_value

def luckyText(num: int) -> str:
    text = f'你今天的人品值为：{num}'
    if num == 0:
        text += '？！'
    elif num <= 10:
        text += '……（是百分制哦）'
    elif num <= 50:
        text += '。'
    elif num < 100:
        text += '！'
    else:
        text += '！100！100！'
    return text
