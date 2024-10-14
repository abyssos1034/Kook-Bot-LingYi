import requests, json, os

from khl import Bot, Message, MessageTypes
from khl.card import Card, CardMessage, Module, Element, Types

from .init import *
from .lucky import *
from .image import *

def initCommands(bot: Bot) -> None:
    @bot.command(name='帮助', aliases=['help', '机器人帮助'], case_sensitive=False)
    async def showHelp(msg: Message, *args: str):
        if not args:
            c = Card(Module.Header(Element.Text('Bot 指令帮助')),
                     Module.Divider(),
                     Module.Section(Element.Text('`/帮助 ([指令名称或别名])`')),
                     Module.Section(Element.Text('别名：Help、机器人帮助')),
                     Module.Section(Element.Text('查看 Bot 指令帮助，或查看关于某指令的详细帮助。')),
                     Module.Divider(),
                     Module.Section(Element.Text('`/今日人品`')),
                     Module.Section(Element.Text('查询今日人品。')),
                     Module.Divider(),
                     Module.Section(Element.Text('`/点歌 [歌曲名]`')),
                     Module.Section(Element.Text('~~（本功能暂未实现，抱歉！）~~')),
                     Module.Section(Element.Text('~~将指定歌曲加入播放列表中。~~')),
                     Module.Divider(),
                     Module.Section(Element.Text('`/随机涩图 ([或-与表达式])`')),
                     Module.Section(Element.Text('别名：随机色图、来点图图、来点色图、来点涩图')),
                     Module.Section(Element.Text('让 Bot 发送随机涩图，或通过表达式让 Bot 发送指定Tag的涩图。')),
                     Module.Divider(),
                     Module.Section(Element.Text('`/关于`')),
                     Module.Section(Element.Text('别名：About')),
                     Module.Section(Element.Text('查看关于 Bot 的详细信息。')),
                     Module.Divider(),
                     Module.Section(Element.Text('`/机器人下线`')),
                     Module.Section(Element.Text('别名：Exit')),
                     Module.Section(Element.Text('下线 Bot ，仅限管理员使用。')),
                     color='#dddddd')
        else:
            arg = args[0].lower()
            if arg in ['帮助', 'help', '机器人帮助']:
                c = Card(Module.Header(Element.Text('指令：/帮助')),
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
                c = Card(Module.Header(Element.Text('指令：/点歌')),
                         Module.Section(Element.Text('~~接受参数类型：`str|tuple`~~')),
                         Module.Section(Element.Text('~~将指定歌曲加入播放列表中。~~')),
                         Module.Context(Element.Text('~~（本功能暂未实现，抱歉！）~~')),
                         color='#dddddd')
            elif arg in ['随机涩图', 'setu', '随机色图', '来点图图', '来点色图', '来点涩图']:
                c = Card(Module.Header(Element.Text('指令：/随机涩图')),
                         Module.Section(Element.Text('别名：Setu、随机色图、来点图图、来点色图、来点涩图')),
                         Module.Section(Element.Text('接受参数类型：`None|str|tuple`')),
                         Module.Section(Element.Text('让 Bot 发送随机涩图，或通过表达式让 Bot 发送指定Tag的涩图。')),
                         Module.Section(Element.Text('此处使用`https://api.lolicon.app/setu/v2`这一api。')),
                         color='#dddddd')
            elif arg in ['关于', 'about']:
                c = Card(Module.Header(Element.Text('指令：/关于')),
                         Module.Section(Element.Text('别名：About')),
                         Module.Section(Element.Text('接受参数类型：`None|tuple`')),
                         Module.Section(Element.Text('查看关于 Bot 的详细信息。')),
                         color='#dddddd')
            elif arg in ['机器人下线', 'exit']:
                c = Card(Module.Header(Element.Text('指令：/机器人下线')),
                         Module.Section(Element.Text('别名：Exit')),
                         Module.Section(Element.Text('接受参数类型：`None|tuple`')),
                         Module.Section(Element.Text('下线 Bot ，仅限管理员使用。')),
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
        addLog(f'[CMD]用户{msg.author_id}：今日人品，传参为{args}，返回{d_lucky}')

    @bot.command(name='点歌', case_sensitive=False)  # 待实现！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
    async def getMusic(msg: Message, *args):
        await msg.reply('~~该功能暂未实现，抱歉！~~', use_quote=False)
        music_name = " ".join(args)
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

    @bot.command(name='关于', aliases=['about'], case_sensitive=False)
    async def getAbout(msg: Message, *args):
        img_url = await bot.client.create_asset(f'.{os.sep}images{os.sep}rowin.jpg')
        c = Card(Module.Header(Element.Text(f'关于 {g_name} Bot')),
                 Module.Divider(),
                 Module.Section(Element.Text(f'**Version:** {g_version}\n**Creator:** 落云Rowin'),
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

    @bot.command(name='test', case_sensitive=False)
    async def testFunc(msg: Message, *args):
        if msg.author_id in g_admin or True:
            log_url = await bot.client.create_asset(f'.{os.sep}log{os.sep}{logName()}.log')
            await msg.reply(log_url, type=MessageTypes.FILE, use_quote=False)
            addLog(f'[DEB]"testFunc()" was called by {msg.author_id}, with args {args}.".')
