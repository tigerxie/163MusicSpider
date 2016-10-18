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

    # biuld search
    def biuld_search(self, s, stype, limit):
        data = self.search(s, stype, limit)

        dig_data = []
        dig_type = ""

        if (stype == 1):
            # 通过 ids 获得歌曲 songs 详细
            song_ids = []
            for i in range(0, len(data['result']['songs']) ):
                song_ids.append( data['result']['songs'][i]['id'] )
            dig_data = self.songs_detail(song_ids)
            dig_type = 'songs'

        elif (stype == 10):
            # dig albums
            if 'albums' in data['result']:
                dig_data = data['result']['albums']
                dig_type = 'albums'

        elif (stype == 100):
            # dig artists
            if 'artists' in data['result']:
                dig_data = data['result']['artists']
                dig_type = 'artists'

        # else : return []z

        # 挖数据
        datalist = self.dig_info(dig_data, dig_type)
        return datalist

    # 搜索单曲(1)，专辑(10)，歌手(100)
    def search(self, s, stype=1, offset=0, total="true", limit=10):
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

            f = open("./src/proxy")
            lines = f.readlines()
            proxys = []
            for i in range(0,len(lines)):
                ip = lines[i].strip("\n").split("\t")
                proxy_host = "http://"+ip[0]+":"+ip[1]
                # print proxy_host
                proxy_temp = {"http":proxy_host}
                # print proxy_temp
                proxys.append(proxy_temp)

            for proxy in proxys:
                try:
                    connection = requests.get(url, headers=self.header, proxies=proxy, timeout=default_timeout)
                    
                except Exception,e:
                    print proxy
                    print e
                    continue

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
    def dig_info(self, dig_data ,dig_type):
        temp = []
        
        if (dig_type == 'songs'):
            for i in range(0, len(dig_data) ):
                song_info = {
                    'song_id': dig_data[i]['id'],
                    'artist': [],
                    'song_name': dig_data[i]['name'],
                    'album_name': dig_data[i]['album']['name'],
                    'mp3_url': dig_data[i]['mp3Url']   
                }
                if 'artist' in dig_data[i]:
                    song_info['artist'] = dig_data[i]['artist']
                elif 'artists' in dig_data[i]:
                    for j in range(0, len(dig_data[i]['artists']) ):
                        song_info['artist'].append( dig_data[i]['artists'][j]['name'] )
                    song_info['artist'] = ', '.join( song_info['artist'] )
                else:
                    song_info['artist'] = '未知艺术家'

                temp.append(song_info)

            return temp

        # elif (dig_type == 'albums'):

        # elif (dig_type == 'artists'): 

        # else return []
    
###############################################################################
netEase = NetEase()
log = Log.getLogger('MusicSpider')



# 搜索歌曲, 专辑，歌手 
s = "imagine"
stype = 1
limit = 10
musics = netEase.search(s, stype, limit)
log.info("==================musics================")
log.info(musics)

# 通过 ids 获得歌曲 songs 详细


# song_ids = []
# for i in range(0, len(musics['result']['songs']) ):
#     song_ids.append( musics['result']['songs'][i]['id'] )
# songs = netEase.songs_detail(song_ids)

# # 挖歌曲中的数据
# datalist = netEase.dig_info(songs, 'songs')
# log.info("==================datalist================")
# log.info(datalist)