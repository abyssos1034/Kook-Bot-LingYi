import requests, time, os

from khl import Bot

from .init import *

def splitExpr(expr: str) -> list:
    output = []
    tmp = expr.replace('and', '&').split('&')
    for i in tmp:
        output.append(i.replace('or', '|').split('|'))
    return output

async def img_upload(img_url: str, bot: Bot) -> str:
    t = int(time.time())
    header = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'}
    re = requests.get(url=img_url, headers=header)
    path = f'.{os.sep}images{os.sep}pic{os.sep}{t}.jpg'
    with open(path, 'wb') as f:
        for chunk in re.iter_content(chunk_size=128):
            f.write(chunk)
    addLog(f'[FIL]已创建新文件"{path}"')
    i_url = await bot.client.create_asset(path)
    return i_url
