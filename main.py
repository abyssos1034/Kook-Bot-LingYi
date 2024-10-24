from khl import Bot

from plugins.commands import *
from plugins.crontasks import *

bot = Bot(token=TOKEN)

@bot.on_startup
async def botInit(bot: Bot):
    addLog(f'[BOT]Bot已开启')
    initCommands(bot)
    initCrons(bot)

if __name__ == '__main__':
    bot.run()
