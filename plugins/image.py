import requests, json, os

from khl import Bot

from .log import addLog

def splitExpr(expr: str) -> list[list]:
    output = []
    tmp = expr.replace('and', '&').replace('&&', '&').split('&')
    for i in tmp:
        output.append(i.replace('or', '|').replace('||', '|').split('|'))
    return output

async def imgUpload(bot: Bot, img_url: str, img_name: str) -> str:
    header = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'}
    re = requests.get(url=img_url, headers=header)
    path = f'.\\temp\\image\\{img_name}.jpg'
    if not os.path.exists(path):
        with open(path, 'wb') as f:
            for chunk in re.iter_content(chunk_size=128):
                f.write(chunk)
        addLog(f'[FIL]已创建新文件"{path}"')
    i_url = await bot.client.create_asset(path)
    return i_url

def getImage(tags: list[list]) -> dict[str, str]:
    data = {'tag': tags}
    r = requests.post(url='https://api.lolicon.app/setu/v2',
                      headers={'Content-Type': 'application/json'}, 
                      data=json.dumps(data, ensure_ascii=False))
    content: dict = json.loads(r.content)
    return {'pid': content['data'][0]['pid'],
            'tags': '、'.join(content['data'][0]['tags']),
            'url': content['data'][0]['urls']['original']}
