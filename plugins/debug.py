import sys
from functools import wraps
from typing import Callable

from khl import Bot, Message, MessageTypes

from .globals import ADMIN, DEBUG
from .logger import logger, logName, addLog
from .exceptions import default_exc_handler, Exceptions

def permission(lvl: list, description: str):
    def decorator(func: Callable):
        @wraps(func)
        async def wrappper(msg: Message, *args):
            if msg.author_id not in lvl: raise Exceptions.PermissionException(description)
            result = await func(msg, *args)
            return result
        return wrappper
    return decorator

def debug_command(bot: Bot) -> None:
    @bot.command(name='debug',
                 case_sensitive=False,
                 prefixes=['//'],
                 exc_handlers=default_exc_handler)
    @logger
    @permission(ADMIN, '管理员')
    async def debugFunc(msg: Message, *args):
        debug_channel = await bot.client.fetch_public_channel(DEBUG)
        if args:
            arg = args[0]
            if arg == 'log':
                log_url = await bot.client.create_asset(f'.\\log\\{logName()}.log')
                err_url = await bot.client.create_asset(f'.\\log\\error.txt')
                await debug_channel.send('已生成日志。')
                await debug_channel.send(log_url, type=MessageTypes.FILE)
                await debug_channel.send(err_url, type=MessageTypes.FILE)
            elif arg == 'off':
                await debug_channel.send('Bot 已成功下线。')
                await bot.client.offline()
                addLog(f'[BOT]Bot已关闭\n')
                sys.exit()
            elif arg == 'error':
                raise Exceptions.DebugException(' '.join(args[1:]))
            else:
                raise Exceptions.DebugException()
        else:
            raise Exceptions.DebugException()
