import random

from .exceptions import ParameterError

dices: dict[int, str] = {4: '四', 6: '六', 8: '八', 10: '十', 12: '十二', 20: '二十', 100: '一百'}

def newDice(*args) -> str:
    if len(args) > 1:
        raise ParameterError('None|int')
    elif len(args) == 0:
        r = random.randint(1, 6)
        return f'使用六面骰，掷出了：{r}。'
    else:
        arg = args[0]
        if arg not in dices:
            raise ParameterError('None|int')
        else:
            r = random.randint(1, arg)
            return f'使用{dices[arg]}面骰，掷出了：{r}。'
