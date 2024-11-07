from khl import Message, command
from khl.card import Card, CardMessage, Module, Element
from khl.command.exception import Exceptions

from .log import addLog
from .error import Error

async def catchException(cmd: command.Command,
                         exc: Exception,
                         msg: Message) -> None:
    if isinstance(exc, Exceptions.Lexer.NotMatched): return
    elif isinstance(exc, Error.BaseError):
        print(type(exc))
        if isinstance(exc, Error.ResponseError):
            addLog(f'[EXC]Raised ResponseError when executing command "{cmd.name}".')
            c = Card(Module.Header(Element.Text('发生网络错误')),
                     Module.Divider(),
                     Module.Section(Element.Text(f'发生网络错误，错误码：`{exc}`。')),
                     Module.Section(Element.Text('由于发生网络错误，刚才的命令未能成功执行，请重试。')),
                     color='#dd3333')
        elif isinstance(exc, Error.ParameterError):
            c = Card(Module.Header(Element.Text('命令传参格式错误')),
                     Module.Divider(),
                     Module.Section(Element.Text(f'命令传参格式错误，应当传入参数的类型为：`{exc}`。')),
                     Module.Section(Element.Text('由于命令传参格式错误，刚才的命令未能正确执行，请更换参数后重试。')),
                     color='#dd3333')
        elif isinstance(exc, Error.TerminalError):
            c = Card(Module.Header(Element.Text('终端指令执行错误')),
                     Module.Divider(),
                     Module.Section(Element.Text(f'终端指令执行错误，错误信息：`{exc}`。')),
                     Module.Section(Element.Text('由于终端指令执行错误，刚才的命令未能执行，请重试。')),
                     color='#dd3333')
    else:
        addLog(f'[EXC]Raised {str(type(exc))[8:-2]} when executing command "{cmd.name}".')
        c = Card(Module.Header(Element.Text('发生了一个未知错误')),
                 Module.Divider(),
                 Module.Section(Element.Text(f'发生了一个未知错误：`{str(type(exc))[8:-2]}`。')),
                 Module.Section(Element.Text(f'错误信息：{exc}。')),
                 Module.Section(Element.Text('请重试。如果无法解决，请联系开发者。')),
                 color='#dd3333')
    await msg.reply(CardMessage(c), use_quote=False)

default_exc_handler = {Exception: catchException}
