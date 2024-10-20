import requests, json, os

from khl import Bot, Message, MessageTypes
from khl.card import Card, CardMessage, Module, Element, Types

from .init import *
from .lucky import *
from .image import *
from .dice import *

def initCommands(bot: Bot) -> None:
    @bot.command(name='帮助', aliases=['help', '机器人帮助'], case_sensitive=False)
    async def showHelp(msg: Message, *args: str):
        if not args:
            c = Card(Module.Header(Element.Text('Bot 指令帮助')),
                     Module.Divider(),
                     Module.Section(Element.Text('`/帮助 <指令名称或别名>`')),
                     Module.Section(Element.Text('别名：Help、机器人帮助')),
                     Module.Section(Element.Text('查看 Bot 指令帮助，或查看关于某指令的详细帮助。')),
                     Module.Divider(),
                     Module.Section(Element.Text('`/今日人品`')),
                     Module.Section(Element.Text('查询今日人品。')),
                     Module.Divider(),
                     Module.Section(Element.Text('`/点歌 <歌曲名>`')),
                     Module.Section(Element.Text('~~（本功能暂未实现，抱歉！）~~')),
                     Module.Section(Element.Text('~~将指定歌曲加入播放列表中。~~')),
                     Module.Divider(),
                     Module.Section(Element.Text('`/随机涩图 <表达式>`')),
                     Module.Section(Element.Text('别名：随机色图、来点图图、来点色图、来点涩图')),
                     Module.Section(Element.Text('让 Bot 发送随机涩图，或通过表达式让 Bot 发送指定Tag的涩图。')),
                     Module.Divider(),
                     Module.Section(Element.Text('`/扔骰子 [4|6|8|10|12|20|100]`')),
                     Module.Section(Element.Text('别名：Dice、掷骰子')),
                     Module.Section(Element.Text('扔出指定面数的骰子，默认掷出六面骰。')),
                     Module.Divider(),
                     Module.Section(Element.Text('`/关于`')),
                     Module.Section(Element.Text('别名：About')),
                     Module.Section(Element.Text('查看关于 Bot 的详细信息。')),
                     Module.Divider(),
                     color='#dddddd')
        else:
            arg = args[0].lower()
            if arg in ['帮助', 'help', '机器人帮助']:
                c = Card(Module.Header(Element.Text('指令：/帮助 <指令名称或别名>')),
                         Module.Section(Element.Text('别名：Help、机器人帮助')),
                         Module.Section(Element.Text('接受参数类型：`None|str`')),
                         Module.Section(Element.Text('查看 Bot 指令帮助，或查看关于某指令的详细帮助。')),
                         color='#dddddd')
            elif arg in ['今日人品']:
                c = Card(Module.Header(Element.Text('指令：/今日人品')),
                         Module.Section(Element.Text('接受参数类型：`None`')),
                         Module.Section(Element.Text('查询今日人品，返回值为0-100的随机整数，当天某特定用户的数值不变。')),
                         color='#dddddd')
            elif arg in ['点歌']:
                c = Card(Module.Header(Element.Text('指令：/点歌 <歌曲名>')),
                         Module.Section(Element.Text('~~接受参数类型：`str|tuple`~~')),
                         Module.Section(Element.Text('~~示例：`/点歌 春日影`~~')),
                         Module.Section(Element.Text('~~将指定歌曲加入播放列表中。~~')),
                         Module.Context(Element.Text('~~（本功能暂未实现，抱歉！）~~')),
                         color='#dddddd')
            elif arg in ['导入歌单']:
                c = Card(Module.Header(Element.Text('指令：/导入歌单 <歌单的url>')),
                         Module.Section(Element.Text('~~接受参数类型：`str`~~')),
                         Module.Section(Element.Text('~~示例：`/导入歌单 `~~')),
                         Module.Section(Element.Text('~~将指定歌曲加入播放列表中。~~')),
                         Module.Context(Element.Text('~~（本功能暂未实现，抱歉！）~~')),
                         color='#dddddd')
            elif arg in ['随机涩图', 'setu', '随机色图', '来点图图', '来点色图', '来点涩图']:
                c = Card(Module.Header(Element.Text('指令：/随机涩图 <表达式>')),
                         Module.Section(Element.Text('别名：Setu、随机色图、来点图图、来点色图、来点涩图')),
                         Module.Section(Element.Text('接受参数类型：`None|str|tuple`')),
                         Module.Section(Element.Text('示例：`/随机涩图 原神|明日方舟&白丝|黑丝`')),
                         Module.Section(Element.Text('注1：为简易起见，此处的**或运算**比**与运算**的优先级更高，且不支持使用小括号。')),
                         Module.Section(Element.Text('注2：支持的**或运算符**：`|、||、or`，支持的**与运算符**：`&、&&、and`')),
                         Module.Section(Element.Text('让 Bot 发送随机涩图，或通过表达式让 Bot 发送指定Tag的随机涩图。')),
                         Module.Section(Element.Text('此处使用`https://api.lolicon.app/setu/v2`这一api。')),
                         color='#dddddd')
            elif arg in ['扔骰子', 'dice', '掷骰子']:
                c = Card(Module.Header(Element.Text('指令：/扔骰子 [4|6|8|10|12|20|100]')),
                         Module.Section(Element.Text('别名：Dice、掷骰子')),
                         Module.Section(Element.Text('接受参数类型：`None|int`')),
                         Module.Section(Element.Text('扔出指定面数的骰子，默认掷出六面骰。')),
                         color='#dddddd')
            elif arg in ['关于', 'about']:
                c = Card(Module.Header(Element.Text('指令：/关于')),
                         Module.Section(Element.Text('别名：About')),
                         Module.Section(Element.Text('接受参数类型：`None`')),
                         Module.Section(Element.Text('查看关于 Bot 的详细信息。')),
                         color='#dddddd')
            else:
                c = Card(Module.Section(Element.Text(f'不存在关于`{arg}`的指令帮助。')),
                         color='#dddddd')
        await msg.reply(CardMessage(c), use_quote=False)
        addLog(f'[CMD]用户{msg.author_id}：帮助，传参为{args}')

    @bot.command(name='今日人品', case_sensitive=False)
    async def getLucky(msg: Message, *args):
        d_lucky = lucky(Message.author)
        await msg.reply(luckyText(d_lucky))
        addLog(f'[CMD]用户{msg.author_id}：今日人品，传参为{args}')

    @bot.command(name='点歌', case_sensitive=False)
    async def getMusic(msg: Message, *args):
        await msg.reply('该功能暂未实现，抱歉！', use_quote=False)
        music_name = " ".join(args)
        if music_name:
            # Code Here.
            ...
            # Code Here.
        else:
            msg.reply('歌曲名不能为空！', use_quote=False)
        addLog(f'[CMD]用户{msg.author_id}：点歌，传参为{args}')

    @bot.command(name='随机涩图', aliases=['setu', '随机色图', '来点图图', '来点色图', '来点涩图'], case_sensitive=False)
    async def getPic(msg: Message, *args):
        expr = ''.join(args)
        tags = splitExpr(expr)
        content = requests.post(url='https://api.lolicon.app/setu/v2',
                                headers={'Content-Type': 'application/json'}, 
                                data=json.dumps({'tag': tags}))
        content = json.loads(content.content)
        img_pid = content['data'][0]['pid']
        img_tags = content['data'][0]['tags']
        img_url = content['data'][0]['urls']['original']
        img_info = f'**图片Pid**：{img_pid}\n**图片Tag**：\n' + '、'.join(img_tags)
        i_url = await img_upload(img_url, bot)
        await msg.reply(i_url, type=MessageTypes.IMG, use_quote=False)
        await msg.reply(img_info, use_quote=False)
        addLog(f'[CMD]用户{msg.author_id}：随机涩图，传参为{args}')

    @bot.command(name='扔骰子', aliases=['dice', '掷骰子'], case_sensitive=False)
    async def getDice(msg: Message, *args):
        if args:
            try:
                n = int(args[0])
                t = newDice(n)
            except:
                t = '不存在这种骰子。'
        else:
            t = newDice()
        await msg.reply(t, use_quote=False)
        addLog(f'[CMD]用户{msg.author_id}：扔骰子，传参为{args}')

    @bot.command(name='关于', aliases=['about'], case_sensitive=False)
    async def getAbout(msg: Message, *args):
        img_url = await bot.client.create_asset(f'.{os.sep}images{os.sep}rowin.jpg')
        c = Card(Module.Header(Element.Text(f'关于 {g_name} Bot')),
                 Module.Divider(),
                 Module.Section(Element.Text(f'**Version:** {g_ver}\n**Creator:** 落云Rowin'),
                                Element.Image(src=img_url)),
                 color='#dddddd')
        await msg.reply(CardMessage(c), use_quote=False)
        addLog(f'[CMD]用户{msg.author_id}：关于，传参为{args}')

    @bot.command(name='机器人下线', aliases=['exit'], case_sensitive=False)
    async def offBot(msg: Message, *args):
        if msg.author_id in g_admin:
            await msg.reply('Bot 已成功下线。', use_quote=False)
            await bot.client.offline()
            addLog(f'[CMD]用户{msg.author_id}：机器人下线，传参为{args}')
            addLog(f'[BOT]Bot已关闭\n')
            os._exit(0)
        else:
            await msg.reply('杂鱼～你觉得你有权限吗？')
            addLog(f'[CMD]用户{msg.author_id}：机器人下线，传参为{args}')
            addLog(f'[ERR]用户权限不足')

    @bot.command(name='debug', aliases=['test'], case_sensitive=False, prefixes=['//'])
    async def debugFunc(msg: Message, *args):
        if msg.author_id in g_admin:
            addLog(f'[DEB]"debugFunc()" was called by {msg.author_id}, with args {args}.".')
            debug_channel = await bot.client.fetch_public_channel(g_debug)
            log_url = await bot.client.create_asset(f'.{os.sep}log{os.sep}{logName()}.log')
            await debug_channel.send(log_url, type=MessageTypes.FILE)
