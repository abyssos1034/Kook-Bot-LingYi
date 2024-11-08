import json

with open('config.json', 'r', encoding='utf-8') as f:
    data: dict = json.load(f)
NAME : str  = data.get('name', '凌依喵')
DESCR: str  = data.get('description')
VER  : str  = data.get('version')
DEV  : str  = data.get('developer', '[落云Rowin](https://github.com/RowinNyan)')
TOKEN: str  = data.get('token')
ADMIN: list = data.get('admin')
DEBUG: str  = data.get('debug_channel')
del data

KOOK_API_BASE = 'https://www.kookapp.cn/api/v3/'
