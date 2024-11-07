import time, os
from functools import wraps
from typing import Callable

from khl import Bot, Message

def log(func: Callable):
    @wraps(func)
    async def wrapper(msg: Message, *args):
        if 'cmd' in func.__name__:
            addLog(f'[CMD]用户{msg.author_id}：调用函数{func.__name__}()，传参为{args}')
        else:
            addLog(f'[DEB]用户{msg.author_id}: 调用函数{func.__name__}()，传参为{args}')
        try:
            result = await func(msg, *args)
            return result
        except Exception as e:
            raise e
    return wrapper

def logName() -> str:
    n_time = time.strftime(f"%Y-%m-%d", time.localtime())
    return n_time

def addLog(log: str) -> None:
    with open(f'.{os.sep}log{os.sep}{logName()}.log', 'a', encoding='utf-8') as f:
        n_time = time.strftime(f"%Y-%m-%d %H:%M:%S", time.localtime())
        f.write(f'[{n_time}]{log}\n')
    print(f'[{n_time}]{log}')

async def findUser(bot: Bot, gid: str, aid: str) -> str:
    voice_channel_ = await bot.client.gate.request('GET', 'channel-user/get-joined-channel',
                                                   params={'guild_id': gid, 'user_id': aid})
    voice_channel = voice_channel_["items"]
    if voice_channel:
        vcid = voice_channel[0]['id']
        return vcid