Crawl songs' comments from music.163.com and analysis



# 网易云歌曲评论爬取及数据可视化分析



# Config

需要先创建mysql数据库, 配置好该文件



# Crawl

1.爬取歌手网易云的hot50歌曲（调用crawl_musicid.py），获得songId 和歌曲名（修改歌手id,可以爬不同歌手的hot50）

2.将songid传到爬取歌曲评论的函数（总体使用crawl.py爬取），爬完会存入到指定数据库的数据表



# WordCloud

1. getText()读取数据库的数据

2. getSemi()获取评论的情感分析

3. getWordcloud()生成词云



# Output

最终得到两个情感分析的html,和词云图

