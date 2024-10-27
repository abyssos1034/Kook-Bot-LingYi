from khl import Message, command
from khl.card import Card, CardMessage, Module, Element
from khl.command.exception import Exceptions

from .log import *

class TestException(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class ResponseError(Exception):
    def __init__(self, *args):
        super().__init__(*args)

def excHandler() -> dict: return {Exception: catchException}

async def catchException(cmd: command.Command,
                         exc: Exception,
                         msg: Message) -> None:
    if isinstance(exc, Exceptions.Lexer.NotMatched): return
    elif isinstance(exc, ResponseError):
        addLog(f'[EXC]Raised {str(type(exc))[8:-2]} when executing command "{cmd.name}".')
        c = Card(Module.Header(Element.Text('发生网络错误')),
                 Module.Divider(),
                 Module.Section(Element.Text(f'发生网络错误，错误码：{exc}。')),
                 Module.Section(Element.Text('由于发生了一个网络错误，刚才的操作未能成功执行，请重试。')),
                 color='#dd3333')
    else:
        addLog(f'[EXC]Raised {str(type(exc))[8:-2]} when executing command "{cmd.name}".')
        c = Card(Module.Header(Element.Text('发生了一个未知错误')),
                 Module.Divider(),
                 Module.Section(Element.Text(f'发生了一个未知错误：{str(type(exc))[8:-2]}。')),
                 Module.Section(Element.Text('请重试。如果无法解决，请联系开发者。')),
                 color='#dd3333')
    await msg.reply(CardMessage(c), use_quote=False)
