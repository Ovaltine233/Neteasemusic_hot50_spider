 # -*- coding=utf-8 -*-
import json
from datetime import datetime
import requests
import config
import pymysql
import gevent
from gevent import monkey

from lxml import etree

from crawler_musicid import get_songs

# monkey.patch_all()


ROOT_URL = 'http://music.163.com/api/v1/resource/comments/R_SO_4_' + '%s' + '?limit=' + str(
    config.LIMIT_NUM) + '&offset=%s'


class Crawler(object):
    def run(self, url, songid, song_name):
        print('crawl ', url)
        self.parse_page(url, songid, song_name)

    def down(self, url):
        try:
            return requests.get(url=url, headers=config.HEADERS).text
        except Exception as e:
            print('down err>>>', e)

    def parse_page(self, url, songid, song_name):
        content = self.down(url)
        js = json.loads(content)
        datas = []
        for c in js['comments']:
            data = {}
            try:
                data['commentId'] = c['commentId']
                data['content'] = config.PATTERN.sub('', c['content'])
                data['likedCount'] = int(c['likedCount'])
                data['time'] = datetime.fromtimestamp(c['time'] // 1000)
                data['userId'] = c['user']['userId']
                datas.append(data)
            except Exception as e:
                print('解析js出错>>>', e)
        self.save(datas, songid, song_name)

    def save(self, datas, songid, song_name):
        conn = pymysql.connect(host=config.HOST, user=config.USER, passwd=config.PASSWD, db=config.DATABASE,
                               charset='utf8mb4')  # 注意字符集要设为utf8mb4，以支持存储评论中的emoji表情
        cursor = conn.cursor()
        sql = 'insert into ' + config.TABLE_COMMENTS + ' (commentId,content,likedCount,time,userId,songId,songName) VALUES (%s,%s,%s,%s,%s,%s,%s)'
        for data in datas:
            try:
                # cursor.execute('SELECT max(id) FROM '+config.TABLE_COMMENTS)
                # s = cursor.fetchone()[0]
                # if s:
                #   id_ = s+1
                # else:
                #   id_ = 1
                # cursor.execute(sql, (
                #     data['commentId'], data['content'], data['likedCount'], data['time'], data['userId'], config.SONGID,
                #     config.SONGNAME))
                cursor.execute(sql, (
                    data['commentId'], data['content'], data['likedCount'], data['time'], data['userId'], songid,
                    song_name))
                conn.commit()
            except Exception as e:
                print('存储错误>>>', e)
        cursor.close()
        conn.close()

    def main(self, pages, songid, song_name):
        url_list = [ROOT_URL % (songid, num * config.LIMIT_NUM) for num in range(0, pages // config.LIMIT_NUM + 1)]
        job_list = [gevent.spawn(self.run(url, songid, song_name)) for url in url_list]
        gevent.joinall(job_list)


def getTotal(songid):
    try:
        # req = requests.get(ROOT_URL % (songid) % (0), headers=config.HEADERS).text
        req = requests.get(ROOT_URL % (songid, 0), headers=config.HEADERS).text
        js = json.loads(req)
        return js['total']
    except Exception as e:
        print(e)
    return None


if __name__ == "__main__":
    # 爬歌手的hot50歌曲ID
    # 设置歌手ID，陈奕迅为2116
    artist_id = '2116'  # 歌手的ID
    [song_ids, song_names] = get_songs(artist_id)
    for songid, song_name in zip(song_ids, song_names):
        # print(songid, song_name)
        total = getTotal(songid)
        print(total)
        total = 3000
        spider = Crawler()
        spider.main(total, songid, song_name)
