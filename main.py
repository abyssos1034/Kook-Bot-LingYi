from khl import Bot

from plugins.globals import TOKEN
from plugins.commands import initCommands
from plugins.crontasks import initCrons
from plugins.log import addLog

bot = Bot(token=TOKEN)

@bot.on_startup
async def botInit(bot: Bot):
    addLog(f'[BOT]Bot已开启')
    initCommands(bot)
    initCrons(bot)

if __name__ == '__main__':
    bot.run()
