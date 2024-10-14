import json

from khl import User

g_name: str = str()
g_version: str = str()
g_token: str = str()
g_admin: list = []

with open('config.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
g_name    = data['name']
g_version = data['version']
g_token   = data['token']
g_admin.extend(data['admin'])

g_lucky: dict[User, int]= {}
