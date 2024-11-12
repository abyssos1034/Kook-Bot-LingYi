import time
from functools import wraps
from typing import Callable

from khl import Message, GuildUser

def logger(func: Callable):
    @wraps(func)
    async def wrapper(msg: Message, *args):
        heads = {'cmd': '[CMD]'}
        author: GuildUser = msg.author
        head = heads.get(func.__name__[:3], '[DEB]')
        addLog(f'{head}{author.nickname}({author.id}): 调用函数{func.__name__}()，附加信息为\"{" ".join(args)}\"')
        try:
            result = await func(msg, *args)
            return result
        except Exception as e:
            raise e
    return wrapper

def logName() -> str: return time.strftime(f"%Y-%m-%d", time.localtime())

def addLog(log: str) -> None:
    with open(f'.\\log\\{logName()}.log', 'a', encoding='utf-8') as f:
        n_time = time.strftime(f"%H:%M:%S", time.localtime())
        f.write(f'[{n_time}]{log}\n')
    print(f'[{n_time}]{log}')
