# -*- coding:utf8 -*-

import pandas as pd
from pyecharts.charts import Line
from pyecharts import options as opts
import os
# import jieba
# import jieba.analyse
# from wordcloud import wordcloud,ImageColorGenerator
import pymysql
import re
import config

pattern = re.compile(r'')


def city_group(cityCode):
    city_map = {
        '11': '北京',
        '12': '天津',
        '31': '上海',
        '50': '重庆',
        '5e': '重庆',
        '81': '香港',
        '82': '澳门',
        '13': '河北',
        '14': '山西',
        '15': '内蒙古',
        '21': '辽宁',
        '22': '吉林',
        '23': '黑龙江',
        '32': '江苏',
        '33': '浙江',
        '34': '安徽',
        '35': '福建',
        '36': '江西',
        '37': '山东',
        '41': '河南',
        '42': '湖北',
        '43': '湖南',
        '44': '广东',
        '45': '广西',
        '46': '海南',
        '51': '四川',
        '52': '贵州',
        '53': '云南',
        '54': '西藏',
        '61': '陕西',
        '62': '甘肃',
        '63': '青海',
        '64': '宁夏',
        '65': '新疆',
        '71': '台湾',
        '10': '其他',
    }
    code = str(cityCode)[:2]
    return city_map[code]


conn = pymysql.connect(host=config.HOST, user=config.USER, passwd=config.PASSWD, db=config.DATABASE, charset='utf8')
# sql_comments = 'SELECT userId FROM '+TABLE_COMENTS+' WHERE songName="%s"'%(SONGNAME)
# coments_datas = pd.read_sql(sql_comments, con=conn)
# del datas['id']
# del datas['commentId']
# del datas['content']
# del datas['likedCount']
# del datas['time']
# del datas['songId']
# del datas['songName']

if not os.path.exists(r'./output'):
    os.mkdir(r'./output')

# # 评论用户分析
# # 多表关联查询
# sql_users = 'SELECT '+config.TABLE_USERS+'.id,gender,age,city FROM '+config.TABLE_USERS+','+config.TABLE_COMMENTS+' WHERE '+config.TABLE_USERS+'.userId='+config.TABLE_COMMENTS+'.userId and '+config.TABLE_COMMENTS+'.songName="%s"'
# users_datas = pd.read_sql(sql_users%(config.SONGNAME), con=conn)
# age = users_datas[users_datas['age']>1]
# age = age.id.groupby(age['age']).count()
# bar = Bar('用户年龄分布')
# bar.use_theme('dark')
# bar.add(
#     '',
#     age.index.values,
#     age.values,
#     is_fill=True,
# )
# bar.render(r'./output/'+config.SONGNAME.replace(r'/', '-')+'用户年龄分布.html')

# gender = users_datas.id.groupby(users_datas['gender']).count()
# pie = Pie('用户性别分布图')
# pie.add(
#     '',
#     ['保密', '男', '女'],
#     gender.values,
#     is_label_show=True,
#     )
# pie.render(r'./output/'+config.SONGNAME.replace(r'/','-')+'用户性别分布.html')

# users_datas['city'] = users_datas['city'].apply(city_group)
# city = users_datas.id.groupby(users_datas['city']).count()
# map1 = Map('用户地区分布图')
# map1.add(
#     '',
#     city.index.values,
#     city.values,
#     maptype='china',
#     is_visualmap=True,
#     visual_text_color="#000",
#     is_label_show=True,
# )
# map1.render(r'./output/'+config.SONGNAME.replace(r'/', '-')+'用户地区分布.html')


# 评论时间分析
sql_comments = 'SELECT id,time FROM ' + config.TABLE_COMMENTS
# sql_comments = 'SELECT id,time FROM ' + config.TABLE_COMMENTS + ' WHERE songName="%s"' % (config.SONGNAME)

comments_datas = pd.read_sql(sql_comments, con=conn)
comments_datas['time1'] = comments_datas['time'].dt.dayofweek
num_date = comments_datas.id.groupby(comments_datas['time1']).count()
line1 = (
    Line()
        .set_global_opts(
        title_opts=opts.TitleOpts(title="评论数时间(星期)分布"),
        tooltip_opts=opts.TooltipOpts(is_show=False),
        xaxis_opts=opts.AxisOpts(type_="category"),
        yaxis_opts=opts.AxisOpts(
            type_="value",
            axistick_opts=opts.AxisTickOpts(is_show=True),
            splitline_opts=opts.SplitLineOpts(is_show=True),
        )
    )
        .add_xaxis(xaxis_data=num_date.index.values.tolist(), )
        .add_yaxis('评论数',
                   y_axis=num_date.values.tolist(),
                   symbol="emptyCircle",
                   is_symbol_show=True,
                   label_opts=opts.LabelOpts(is_show=True),
                   itemstyle_opts=opts.ItemStyleOpts(
                       border_width=3, border_color="yellow", color="blue"
                   )
                   )
)
line1.render(r'./output1/' + config.SINGERNAME.replace(r'/', '-') + '评论数时间(星期)分布.html')

comments_datas['time2'] = comments_datas['time'].dt.hour
num_date = comments_datas.id.groupby(comments_datas['time2']).count()
line2 = (
    Line()
        .set_global_opts(
        title_opts=opts.TitleOpts(title="评论数时间（小时）分布"),
        tooltip_opts=opts.TooltipOpts(is_show=False),
        xaxis_opts=opts.AxisOpts(type_="category"),
        yaxis_opts=opts.AxisOpts(
            type_="value",
            axistick_opts=opts.AxisTickOpts(is_show=True),
            splitline_opts=opts.SplitLineOpts(is_show=True),
        )
    )
        .add_xaxis(xaxis_data=num_date.index.values.tolist(), )
        .add_yaxis('评论数',
                   y_axis=num_date.values.tolist(),
                   symbol="emptyCircle",
                   is_symbol_show=True,
                   label_opts=opts.LabelOpts(is_show=True),
                   itemstyle_opts=opts.ItemStyleOpts(
                       border_width=3, border_color="yellow", color="blue"
                   )
                   )
)
line2.render(r'./output/' + config.SINGERNAME.replace(r'/', '-') + '评论数时间（小时）分布.html')

comments_datas['time3'] = comments_datas['time'].dt.date
num_date = comments_datas.id.groupby(comments_datas['time3']).count()
line3 = (
    Line()
        .set_global_opts(
        title_opts=opts.TitleOpts(title="评论数时间(天)分布"),
        tooltip_opts=opts.TooltipOpts(is_show=False),
        xaxis_opts=opts.AxisOpts(type_="category"),
        yaxis_opts=opts.AxisOpts(
            type_="value",
            axistick_opts=opts.AxisTickOpts(is_show=True),
            splitline_opts=opts.SplitLineOpts(is_show=True),
        )
    )
        .add_xaxis(xaxis_data=num_date.index.values.tolist(), )
        .add_yaxis('评论数',
                   y_axis=num_date.values.tolist(),
                   symbol="emptyCircle",
                   is_symbol_show=True,
                   label_opts=opts.LabelOpts(is_show=True),
                   itemstyle_opts=opts.ItemStyleOpts(
                       border_width=3, border_color="yellow", color="blue"
                   )
                   )
)
line3.render(r'./output/' + config.SINGERNAME.replace(r'/', '-') + '评论数时间(天)分布.html')
