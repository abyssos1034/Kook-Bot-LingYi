import requests, json

from khl import Bot

QQMUSIC_SEARCH_API = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?p=1&w='
QQMUSIC_CLIENT_SONG_API = 'https://u.y.qq.com/cgi-bin/musicu.fcg'
QQMUSIC_SONG_BASICURL = 'http://dl.stream.qqmusic.qq.com/'
QQMUSIC_SONG_COVER = 'http://y.qq.com/music/photo_new/T002R300x300M000{id}.jpg'

def searchMusic(music_name: str) -> dict[str, ]:
    r = requests.get(url=f'{QQMUSIC_SEARCH_API}{music_name}')
    content: dict = json.loads(r.content.decode('utf-8')[9:-1])
    if content.get('code', -1) == 0:
        music_info: dict = content['data']['song']['list'][0]
        singer = str()
        for s in music_info.get('singer', [{'name': '未知歌手'}]):
            singer += s['name'] + '/'
        singer = singer[:-1]
        return {
            'music_name': music_info.get('songname', '未知歌曲'),
            'music_id': music_info.get('songmid', ''),
            'singer': singer,
            'interval': music_info.get('interval', 0) * 1000,
            'album_name': music_info.get('albumname', '未知专辑'),
            'album_id': music_info.get('albummid', '')
        }
    else:
        raise Exception(content.get('message', 'UnknownError'))

async def getMusic(bot: Bot, music_name: str) -> dict[str, ]:
    music_info = searchMusic(music_name)
    data = {
        'vkey.GetVkeyServer': {
        'method': 'CgiGetVkey',
        'module': 'vkey.GetVkeyServer',
        'param': {
                'guid': '0',
                'songmid': [
                    music_info['music_id']
                ],
                'uin': '0'
            }
        }
    }
    r = requests.post(url=QQMUSIC_CLIENT_SONG_API, data=json.dumps(data, ensure_ascii=False))
    content: dict = json.loads(r.content)
    if content.get('code', -1) == 0:
        music_url = QQMUSIC_SONG_BASICURL + content['vkey.GetVkeyServer']['data']['midurlinfo'][0]['purl']
        kwargs = {'id': music_info['album_id']}
        cover_url = QQMUSIC_SONG_COVER.format(**kwargs)
        return {
            'music_name': music_info['music_name'],
            'music_id': music_info['music_id'],
            'singer': music_info['singer'],
            'interval': music_info['interval'],
            'album': music_info['album_name'],
            'url': music_url,
            'cover': cover_url
        }
    else:
        raise Exception(content.get('message', 'UnknownError'))
