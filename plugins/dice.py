import random

dices: dict[int, str] = {4: '四', 6: '六', 8: '八', 10: '十', 12: '十二', 20: '二十', 100: '一百'}

def newDice(n: int = 6) -> str:
    r = random.randint(1, n)
    return f'使用{dices[n]}面骰，掷出了：{r}。'
