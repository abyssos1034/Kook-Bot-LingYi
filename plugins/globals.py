import json

from khl import User

with open('config.json', 'r', encoding='utf-8') as f:
    data: dict = json.load(f)
NAME : str  = data.get('name')
DESCR: str  = data.get('description')
VER  : str  = data.get('version')
DEV  : str  = data.get('developer')
TOKEN: str  = data.get('token')
ADMIN: list = data.get('admin')
DEBUG: str  = data.get('debug_channel')
MUSIC: dict = data.get('music_channel')
del data

lucky_list: dict[User, int] = {}
music_playing: bool = False
