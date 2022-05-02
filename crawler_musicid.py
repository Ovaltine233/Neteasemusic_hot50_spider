########
# 用于获取歌手的最热门50歌的ID和名字

# 爬取网易云音乐 歌手的前50首歌曲的ID和名称
import requests
from lxml import etree

headers = {
    'Referer': 'http://music.163.com',
    'Host': 'music.163.com',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'User-Agent': 'Chrome/10'
}


# 得到指定歌手 热门前50的歌曲ID，歌曲名
def get_songs(artist_id):
    page_url = 'https://music.163.com/artist?id=' + artist_id
    # 获取对应HTML
    res = requests.request('GET', page_url, headers=headers)
    # XPath解析 前50的热门歌曲
    html = etree.HTML(res.text)
    href_xpath = "//*[@id='hotsong-list']//a/@href"
    name_xpath = "//*[@id='hotsong-list']//a/text()"
    hrefs = html.xpath(href_xpath)
    names = html.xpath(name_xpath)
    # 设置热门歌曲的ID，歌曲名称
    song_ids = []
    song_names = []
    for href, name in zip(hrefs, names):
        song_ids.append(href[9:])
        # song_ids.append(href)

        song_names.append(name)
        # print(href[9:], ' ', name)
    return song_ids, song_names


# if __name__ == "__main__":
#     # 设置歌手ID，陈奕迅为2116
#     artist_id = '2116'
#     [song_ids, song_names] = get_songs(artist_id)
