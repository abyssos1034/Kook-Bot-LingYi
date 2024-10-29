import requests, json, os

from khl import Bot

from .globals import KOOK_API_BASE, TOKEN, MUSIC
from .exceptions import ResponseError

KOOK_VOICE_API = f'{KOOK_API_BASE}voice/'
QQMUSIC_SEARCH_API = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?p=1&w='
QQMUSIC_CLIENT_SONG_API = 'https://u.y.qq.com/cgi-bin/musicu.fcg'
QQMUSIC_SONG_BASICURL = 'http://dl.stream.qqmusic.qq.com/'
QQMUSIC_SONG_COVER = 'http://y.qq.com/music/photo_new/T002R300x300M000{id}.jpg'

def searchMusic(music_name: str) -> list[dict[str, ]]:
    output = list()
    r = requests.get(url=f'{QQMUSIC_SEARCH_API}{music_name}')
    content: dict = json.loads(r.content.decode('utf-8')[9:-1])
    if content.get('code', -1) == 0:
        for m in content['data']['song']['list']:
            music_info: dict = m
            singer = str()
            for s in music_info.get('singer', [{'name': '未知歌手'}]):
                singer += s['name'] + '/'
            singer = singer[:-1]
            output.append({
                'music_name': music_info.get('songname', '未知歌曲'),
                'music_id': music_info.get('songmid', ''),
                'singer': singer,
                'interval': music_info.get('interval', 0) * 1000,
                'album_name': music_info.get('albumname', '未知专辑'),
                'album_id': music_info.get('albummid', '')
            })
        return output
    else:
        raise ResponseError(content.get('code', -1))

async def getMusic(bot: Bot, music_name: str) -> dict[str, ]:
    music_list = searchMusic(music_name)
    for music_info in music_list:
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
            purl = content['vkey.GetVkeyServer']['data']['midurlinfo'][0]['purl']
            if purl:
                music_url = QQMUSIC_SONG_BASICURL + purl
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

DATA = {'channel_id': MUSIC}
HEADERS = {'Authorization': f'Bot {TOKEN}',
           'Content-type': 'application/json;'}

def joinVoice() -> dict[str, ]:
    r = requests.post(url=f'{KOOK_VOICE_API}join/', data=json.dumps(DATA, ensure_ascii=False), headers=HEADERS)
    content: dict = json.loads(r.content)
    if content.get('code', -1) == 0:
        return content.get('data')
    else:
        raise ResponseError(content.get('code', -1))

def leaveVoice() -> dict[str, ]:
    r = requests.post(url=f'{KOOK_VOICE_API}leave/', data=json.dumps(DATA, ensure_ascii=False), headers=HEADERS)
    content: dict = json.loads(r.content)
    if content.get('code', -1) == 0:
        return content.get('data')
    else:
        raise ResponseError(content.get('code', -1))

def playMusic(url: str,
              ip: str,
              port: str,
              rtcp_port: str,
              rtcp_mux: bool,
              bitrate: int,
              audio_ssrc: str,
              audio_pt: str) -> None:
    if rtcp_mux:
        os.system(f".\\ffmpeg\\ffmpeg -i \"{url}\" -re -map \"0:a:0\" -acodec libopus -ab {bitrate} -ac 2 -ar {bitrate} -filter:a \"volume=0.8\" -f tee \"[select=a:f=rtp:ssrc={audio_ssrc}:payload_type={audio_pt}]rtp://{ip}:{port}\"")
    else:
        os.system(f".\\ffmpeg\\ffmpeg -i \"{url}\" -re -map \"0:a:0\" -acodec libopus -ab {bitrate} -ac 2 -ar {bitrate} -filter:a \"volume=0.8\" -f tee \"[select=a:f=rtp:ssrc={audio_ssrc}:payload_type={audio_pt}]rtp://{ip}:{port}?rtcpport={rtcp_port}\"")
