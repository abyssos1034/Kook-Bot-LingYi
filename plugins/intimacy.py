import requests, json
from .globals import g_token as token

KOOK_INTIMACY_API = 'https://www.kookapp.cn/api/v3/intimacy/'
HEADERS = {'Authorization': f'Bot {token}',
           'Content-type': 'application/json;'}

def intimacyGet(user_id: str) -> int:
    r = requests.get(url=f'{KOOK_INTIMACY_API}index?user_id={user_id}', headers=HEADERS)
    content: dict = json.loads(r.content)
    if content.get('code', -1) == 0:
        score = content['data']['score']
        return score
    else:
        raise Exception(content.get('message', 'UnknownError'))

def intimacyUpdate(user_id: str,
                   social_info: str = 'default',
                   score: int = 0,
                   img_id: int = 0) -> None:
    data = locals()
    r = requests.post(url=f'{KOOK_INTIMACY_API}update', headers=HEADERS, data=json.dumps(data, ensure_ascii=False))
    content: dict = json.loads(r.content)
    if content.get('code', -1) == 0:
        pass
    else:
        raise Exception(content.get('message', 'UnknownError'))
