from khl import Bot

from .init import *
from .lucky import *
from .image import *

def initCrons(bot: Bot) -> None:
    @bot.task.add_cron(timezone='Asia/Shanghai', hour=0, minute=0, second=0)
    async def resetLucky():
        global g_lucky
        g_lucky.clear()
        addLog('[SCH]已重置今日人品')
