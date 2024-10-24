import json

from khl import User

with open('config.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
NAME : str  = data['name']
VER  : str  = data['version']
TOKEN: str  = data['token']
ADMIN: list = data['admin']
DEBUG: str  = data['debug_channel']
MUSIC: str  = data['music_channel']

del data

lucky_list: dict[User, int]= {}
