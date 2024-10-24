import requests

# QQMUSIC_SEARCH_API = "https://c.y.qq.com/soso/fcgi-bin/client_search_cp?p=1&w="
# QQ音乐客户端抓包获得
QQMUSIC_CLIENT_SEARCH_API = "https://u.y.qq.com/cgi-bin/musicu.fcg"
QQMUSIC_CLIENT_SONG_API = "https://u.y.qq.com/cgi-bin/musicu.fcg"
# QQMUSIC_SONG_API = "https://u.y.qq.com/cgi-bin/musicu.fcg?data="
QQMUSIC_SONG_BASICURL = "http://dl.stream.qqmusic.qq.com/"
# QQMUSIC_SONG_DETAILBASIC = "https://y.qq.com/n/ryqq/songDetail/"
QQMUSIC_SONG_COVER = "http://y.qq.com/music/photo_new/T00{singerOrMusic}R300x300M000{id}.jpg"

async def searchMusic(music_name: str):
    query_data = {
        "music.search.SearchCgiService": {
            "method": "DoSearchForQQMusicDesktop",
            "module": "music.search.SearchCgiService",
            "param": {
                "num_per_page": 5,
                "page_num": 1,
                "query": music_name,
                "search_type": 0
            }
        }
    }
    # Code Here.
    ...
    # Code Here.
