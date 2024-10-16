import json

from khl import User

with open('config.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
g_name : str  = data['name']
g_ver  : str  = data['version']
g_token: str  = data['token']
g_admin: list = data['admin']
g_debug: str  = data['debug_channel']
g_music: str  = data['music_channel']

del data

g_lucky: dict[User, int]= {}
