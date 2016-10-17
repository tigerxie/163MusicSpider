# import urllib.request
# import re
import requests
import json
# from bs4 import BeautifulSoup 
from Logger import Log
default_timeout = 100 

class NetEase:
    def __init__(self):
        self.header = {
            'Accept': '*/*',
            'Accept-Encoding': 'deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'music.163.com',
            'Referer': 'http://music.163.com/search/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36'
        }

    def search(self, s, stype=1, offset=0, total='true', limit=1):
        action = 'http://music.163.com/api/search/get/web'
        data = {
            's': s,
            'type': stype,
            'offset': offset,
            'total': total,
            'limit': limit
        }
        return self.httpRequest('POST', action, data)
    
    # song ids --> song urls ( details )
    def songs_detail(self, ids, offset=0):
        action = 'http://music.163.com/api/song/detail?ids=[' + (',').join(map(str, ids)) + ']'
        print(action)
        try:
            data = self.httpRequest('GET', action)
#             print(data)
            return data['songs']
        except:
            return []

    def httpRequest(self, method, action, query=None, urlencoded=None, callback=None, timeout=None):    
        if(method == 'GET'):
            url = action if (query == None) else (action + '?' + query)
            connection = requests.get(url, headers=self.header, timeout=default_timeout)

        elif(method == 'POST'):
            connection = requests.post(
                action,
                data=query,
                headers=self.header,
                timeout=default_timeout
            )

        connection.encoding = "utf-8"
        connection = json.loads(connection.text)
        return connection

    # 挖数据
    def dig_info(self, data ,dig_type):
        temp = []
        if dig_type == 'songs':
            for i in range(0, len(data) ):
                song_info = {
                    'song_id': data[i]['id'],
                    'artist': [],
                    'song_name': data[i]['name'],
                    'album_name': data[i]['album']['name'],
                    'mp3_url': data[i]['mp3Url']   
                }
                if 'artist' in data[i]:
                    song_info['artist'] = data[i]['artist']
                elif 'artists' in data[i]:
                    for j in range(0, len(data[i]['artists']) ):
                        song_info['artist'].append( data[i]['artists'][j]['name'] )
                    song_info['artist'] = ', '.join( song_info['artist'] )
                else:
                    song_info['artist'] = '未知艺术家'

                temp.append(song_info)

        elif dig_type == 'artists':
            temp = []
            for i in range(0, len(data) ):
                artists_info = {
                    'artist_id': data[i]['id'],
                    'artists_name': data[i]['name'],
                    'alias': ''.join(data[i]['alias'])
                }
                temp.append(artists_info)

            return temp

        elif dig_type == 'albums':
            for i in range(0, len(data) ):
                albums_info = {
                    'album_id': data[i]['id'],
                    'albums_name': data[i]['name'],
                    'artists_name': data[i]['artist']['name']
                }
                temp.append(albums_info)

        elif dig_type == 'playlists':
            for i in range(0, len(data) ):
                playlists_info = {
                    'playlist_id': data[i]['id'],
                    'playlists_name': data[i]['name'],
                    'creator_name': data[i]['creator']['nickname']
                }
                temp.append(playlists_info)        


        elif dig_type == 'channels':
            channel_info = {
                'song_id': data['id'],
                'song_name': data['name'],
                'artist': data['artists'][0]['name'],
                'album_name': 'DJ节目',
                'mp3_url': data['mp3Url']
                }
            temp = channel_info    

        return temp
    
###############################################################################
netEase = NetEase()
log = Log.getLogger('MusicSpider')
# 搜索歌曲
musics = netEase.search("imagine", stype=1, limit=10)

# 通过 ids 获得歌曲 songs 详细
song_ids = []
for i in range(0, len(musics['result']['songs']) ):
    song_ids.append( musics['result']['songs'][i]['id'] )
songs = netEase.songs_detail(song_ids)

# 挖歌曲中的数据
datalist = netEase.dig_info(songs, 'songs')
print("==================datalist================")
print(datalist)

