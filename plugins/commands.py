import requests, json, os

from khl import Bot, Message, MessageTypes
from khl.card import Card, CardMessage, Module, Element, Types

from .init import *
from .lucky import *
from .image import *
from .dice import *
from .music import *

def initCommands(bot: Bot) -> None:
    @bot.command(name='help', aliases=['帮助', '机器人帮助'], case_sensitive=False)
    async def cmdHelp(msg: Message, *args: str):
        addLog(f'[CMD]用户{msg.author_id}：帮助，传参为{args}')
        if not args:
            c = Card(Module.Header(Element.Text('Bot 指令帮助')),
                     Module.Divider(),
                     Module.Section(Element.Text('`/help <指令名称或别名>`')),
                     Module.Section(Element.Text('别名：帮助、机器人帮助')),
                     Module.Section(Element.Text('查看 Bot 指令帮助，或查看关于某指令的详细帮助。')),
                     Module.Divider(),
                     Module.Section(Element.Text('`/fortune`')),
                     Module.Section(Element.Text('别名：lucky、今日人品')),
                     Module.Section(Element.Text('查询今日人品。')),
                     Module.Divider(),
                     Module.Section(Element.Text('`/music [开|关|on|off]|<歌曲名>`')),
                     Module.Section(Element.Text('别名：点歌')),
                     Module.Section(Element.Text('~~将指定歌曲加入播放列表中。~~')),
                     Module.Section(Element.Text('~~（本功能暂未实现，抱歉！）~~')),
                     Module.Divider(),
                     Module.Section(Element.Text('`/setu <表达式>`')),
                     Module.Section(Element.Text('别名：随机涩图、随机色图、来点图图、来点色图、来点涩图')),
                     Module.Section(Element.Text('让 Bot 发送随机涩图，或通过表达式让 Bot 发送指定Tag的涩图。')),
                     Module.Divider(),
                     Module.Section(Element.Text('`/dice [4|6|8|10|12|20|100]`')),
                     Module.Section(Element.Text('别名：扔骰子、掷骰子')),
                     Module.Section(Element.Text('扔出指定面数的骰子，默认掷出六面骰。')),
                     Module.Divider(),
                     Module.Section(Element.Text('`/about`')),
                     Module.Section(Element.Text('别名：关于')),
                     Module.Section(Element.Text('查看关于 Bot 的详细信息。')),
                     Module.Divider(),
                     color='#dddddd')
        else:
            arg = ' '.join(args).lower()
            if arg in ['help', '帮助', '机器人帮助']:
                c = Card(Module.Header(Element.Text('指令：/help <指令名称或别名>')),
                         Module.Section(Element.Text('别名：帮助、机器人帮助')),
                         Module.Section(Element.Text('接受参数类型：`None|str`')),
                         Module.Section(Element.Text('查看 Bot 指令帮助，或查看关于某指令的详细帮助。')),
                         color='#dddddd')
            elif arg in ['fortune', 'lucky', '今日人品']:
                c = Card(Module.Header(Element.Text('指令：/今日人品')),
                         Module.Section(Element.Text('接受参数类型：`None`')),
                         Module.Section(Element.Text('查询今日人品，返回值为0-100的随机整数，当天某特定用户的数值不变。')),
                         color='#dddddd')
            elif arg in ['music', '点歌']:
                c = Card(Module.Header(Element.Text('指令：/点歌 <歌曲名>')),
                         Module.Section(Element.Text('~~接受参数类型：`str|tuple`~~')),
                         Module.Section(Element.Text('~~示例：`/点歌 春日影`~~')),
                         Module.Section(Element.Text('~~将指定歌曲加入播放列表中。~~')),
                         Module.Context(Element.Text('~~（本功能暂未实现，抱歉！）~~')),
                         color='#dddddd')
            elif arg in ['setu', '随机涩图', '随机色图', '来点图图', '来点色图', '来点涩图']:
                c = Card(Module.Header(Element.Text('指令：/setu <表达式>')),
                         Module.Section(Element.Text('别名：随机涩图、随机色图、来点图图、来点色图、来点涩图')),
                         Module.Section(Element.Text('接受参数类型：`None|str|tuple`')),
                         Module.Section(Element.Text('示例：`/setu 原神|明日方舟&白丝|黑丝`')),
                         Module.Section(Element.Text('注1：为简易起见，此处的**或运算**比**与运算**的优先级更高，且不支持使用小括号。')),
                         Module.Section(Element.Text('注2：支持的**或运算符**：`|、||、or`，支持的**与运算符**：`&、&&、and`')),
                         Module.Section(Element.Text('让 Bot 发送随机涩图，或通过表达式让 Bot 发送指定Tag的随机涩图。')),
                         Module.Section(Element.Text('此处使用`https://api.lolicon.app/setu/v2`这一api。')),
                         color='#dddddd')
            elif arg in ['dice', '扔骰子', '掷骰子']:
                c = Card(Module.Header(Element.Text('指令：/dice [4|6|8|10|12|20|100]')),
                         Module.Section(Element.Text('别名：扔骰子、掷骰子')),
                         Module.Section(Element.Text('接受参数类型：`None|int`')),
                         Module.Section(Element.Text('扔出指定面数的骰子，默认掷出六面骰。')),
                         color='#dddddd')
            elif arg in ['about', '关于']:
                c = Card(Module.Header(Element.Text('指令：/about')),
                         Module.Section(Element.Text('别名：关于')),
                         Module.Section(Element.Text('接受参数类型：`None`')),
                         Module.Section(Element.Text('查看关于 Bot 的详细信息。')),
                         color='#dddddd')
            else:
                c = Card(Module.Section(Element.Text(f'不存在关于`{arg}`的指令帮助。')),
                         color='#dddddd')
        await msg.reply(CardMessage(c), use_quote=False)

    @bot.command(name='fortune', aliases=['lucky', '今日人品'], case_sensitive=False)
    async def cmdLucky(msg: Message, *args):
        addLog(f'[CMD]用户{msg.author_id}：今日人品，传参为{args}')
        d_lucky = lucky(Message.author)
        await msg.reply(luckyText(d_lucky))

    @bot.command(name='music', aliases=['点歌'], case_sensitive=False)
    async def cmdMusic(msg: Message, *args):
        addLog(f'[CMD]用户{msg.author_id}：点歌，传参为{args}')
        await msg.reply('该功能暂未实现，抱歉！', use_quote=False)
        music_name = ' '.join(args)
        if music_name:
            if not music_playing:
                if music_name.lower() in ['关', 'off']:
                    await msg.reply('你无法关闭本来就已经关闭的东西。ヽ(#`Д´)ﾉ', use_quote=False)
                elif music_name.lower() in ['开', 'on']:
                    music_playing = True
                    # Code Here.
                    ...
                    # Code Here.
                    await msg.reply('点歌模式已开启，输入`/music <歌曲名>`进行点歌。', use_quote=False)
                else:
                    await msg.reply('当前点歌模式暂未开启，请输入`/music on`以启用点歌模式。', use_quote=False)
            else:
                if music_name.lower() in ['关', 'off']:
                    music_playing = False
                    # Code Here.
                    ...
                    # Code Here.
                    await msg.reply('点歌模式已关闭。', use_quote=False)
                elif music_name.lower() in ['开', 'on']:
                    await msg.reply('你无法打开本来就已经打开的东西。ヽ(#`Д´)ﾉ', use_quote=False)
                else:
                    music_info = await getMusic(bot, music_name)
                    c = Card(Module.Section(Element.Text(f'已将歌曲 **{music_info.get("music_name")}** 加入播放列表。'),
                                            Element.Text(f'**歌手：**{music_info.get("singer")}'),
                                            Element.Text(f'**时长：**{music_info.get("interval")}'),
                                            Element.Text(f'**专辑：**{music_info.get("album")}'),
                                            Element.Image(src='')),
                             color='#dddddd')
                    await msg.reply(c, use_quote=False)
        else:
            await msg.reply('歌曲名不能为空！', use_quote=False)

    @bot.command(name='setu', aliases=['随机涩图', '随机色图', '来点图图', '来点色图', '来点涩图'], case_sensitive=False)
    async def cmdPic(msg: Message, *args):
        addLog(f'[CMD]用户{msg.author_id}：随机涩图，传参为{args}')
        expr = ''.join(args)
        tags = splitExpr(expr)
        content = requests.post(url='https://api.lolicon.app/setu/v2',
                                headers={'Content-Type': 'application/json'}, 
                                data=json.dumps({'tag': tags}, ensure_ascii=False))
        content = json.loads(content.content)
        img_pid = content['data'][0]['pid']
        img_tags = content['data'][0]['tags']
        img_url = content['data'][0]['urls']['original']
        img_info = f'**图片Pid**：{img_pid}\n**图片Tag**：\n' + '、'.join(img_tags)
        i_url = await img_upload(bot, img_url)
        await msg.reply(i_url, type=MessageTypes.IMG, use_quote=False)
        await msg.reply(img_info, use_quote=False)

    @bot.command(name='dice', aliases=['扔骰子', '掷骰子'], case_sensitive=False)
    async def cmdDice(msg: Message, *args):
        addLog(f'[CMD]用户{msg.author_id}：扔骰子，传参为{args}')
        if args:
            try:
                n = int(args[0])
                t = newDice(n)
            except:
                t = '不存在这种骰子。'
        else:
            t = newDice()
        await msg.reply(t, use_quote=False)

    @bot.command(name='about', aliases=['关于'], case_sensitive=False)
    async def cmdAbout(msg: Message, *args):
        addLog(f'[CMD]用户{msg.author_id}：关于，传参为{args}')
        c = Card(Module.Header(Element.Text(f'关于 {NAME} Bot')),
                 Module.Divider(),
                 Module.Section(Element.Text(f'{DESCR}', type=Types.Text.PLAIN),
                                Element.Image(src='https://img.kookapp.cn/assets/2024-10/tKYazD9l6i0k00k0.png')),
                 Module.Divider(),
                 Module.Section(Element.Text(f'**版本：**{VER}**\n制作：**{DEV}'),
                                Element.Image(src='https://img.kookapp.cn/attachments/2024-10/10/lXwQbUcYOe0dw0dw.jpeg')),
                 color='#dddddd')
        await msg.reply(CardMessage(c), use_quote=False)

    @bot.command(name='exit', aliases=['机器人下线'], case_sensitive=False)
    async def cmdOffline(msg: Message, *args):
        addLog(f'[CMD]用户{msg.author_id}：机器人下线，传参为{args}')
        if msg.author_id in ADMIN:
            await msg.reply('Bot 已成功下线。', use_quote=False)
            await bot.client.offline()
            addLog(f'[BOT]Bot已关闭\n')
            os._exit(0)
        else:
            await msg.reply('杂鱼～你觉得你有权限吗？')
            addLog(f'[ERR]用户权限不足')

    @bot.command(name='debug', aliases=['test'], case_sensitive=False, prefixes=['//'])
    async def debugFunc(msg: Message, *args):
        if msg.author_id in ADMIN:
            addLog(f'[DEB]"debugFunc()" was called by {msg.author_id}, with args = {args}.".')
            debug_channel = await bot.client.fetch_public_channel(DEBUG)
            log_url = await bot.client.create_asset(f'.{os.sep}log{os.sep}{logName()}.log')
            await debug_channel.send(log_url, type=MessageTypes.FILE)
