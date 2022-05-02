import os

import jieba
import pymysql
import pandas as pd
import numpy as np
from snownlp import SnowNLP
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from pyecharts.charts import Bar, Pie, Line
from pyecharts import options as opts
import config

from pyecharts.faker import Faker
from pyecharts.options.global_options import ThemeType
from imageio import imread

import collections

import time
start = time.time()

plt.style.use('ggplot')
# plt.rcParams['font.sans-serif'] = ['msyh']
plt.rcParams['axes.unicode_minus'] = False

if not os.path.exists(r'./output'):
    os.mkdir(r'./output')

def getText():
    conn = pymysql.connect(host=config.HOST, user=config.USER, passwd=config.PASSWD, db=config.DATABASE,
                           charset='utf8mb4')
    sql = 'SELECT id,content FROM ' + config.TABLE_COMMENTS
    # sql = 'SELECT id,content FROM ' + config.TABLE_COMMENTS + ' WHERE songName="%s"'
    text = pd.read_sql(sql, con=conn)
    return text


def getSemi(text):
    text['content'] = text['content'].apply(lambda x: round(SnowNLP(x).sentiments, 2))
    semiscore = text.id.groupby(text['content']).count()

    bar = (
        Bar({"theme": ThemeType.DARK})
        .add_xaxis(semiscore.index.values.tolist())
        .add_yaxis("情感得分", semiscore.values.tolist(), category_gap=0, color=Faker.rand_color(), gap="20%")
        .set_global_opts(title_opts=opts.TitleOpts(title="评论情感得分"))
            .set_series_opts(
            label_opts=opts.LabelOpts(is_show=False),
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="min", name="最小值"),
                    opts.MarkPointItem(type_="max", name="最大值"),
                    opts.MarkPointItem(type_="average", name="平均值"),
                ]
            ),
        )
    )
    bar.render(r'./output/' +config.SINGERNAME + '情感得分分析.html')

    text['content'] = text['content'].apply(lambda x: 1 if x > 0.5 else -1)
    semilabel = text.id.groupby(text['content']).count()
    bar = (
        Bar({"theme": ThemeType.DARK})
        .add_xaxis(semilabel.index.values.tolist())
        .add_yaxis("情感标签", semilabel.values.tolist(), category_gap=0, color=Faker.rand_color(), gap="20%")
        .set_global_opts(title_opts=opts.TitleOpts(title="评论情感标签"))
    )
    bar.render(r'./output/' + config.SINGERNAME + '情感标签分析.html')


def getWordcloud(text):
    text = ''.join(str(s) for s in text['content'] if s)
    word_list = jieba.lcut(text, cut_all=False)
    stopwords = [line.strip() for line in open(r'./StopWords.txt', 'r', encoding='UTF-8').readlines()]
    clean_list = [seg for seg in word_list if seg not in stopwords]  # 去除停用词
    clean_text = ' '.join(clean_list)
    # 生成词云
    mk = imread("Eason.jpg")
    cloud = WordCloud(
        font_path=r'C:/Windows/Fonts/msyh.ttc',
        background_color='white',
        max_words=800,
        # font_step=2,
        # max_font_size=100,
        collocations=False,
        scale=10,
        mask=mk
    )

    # word_count = collections.Counter(clean_text)
    # word_cloud = cloud.generate_from_frequencies(word_count)
    word_cloud = cloud.generate(clean_text)
    word_cloud.to_file('./output/EasonCloud.png')
    # 绘制词云
    plt.figure(figsize=(12, 12))
    plt.imshow(word_cloud)
    plt.axis('off')
    plt.show()


if __name__ == '__main__':
    text = getText()
    getSemi(text)
    end = time.time()
    print(str(end - start))

    text = getText()
    getWordcloud(text)
    end = time.time()
    print(str(end - start))

