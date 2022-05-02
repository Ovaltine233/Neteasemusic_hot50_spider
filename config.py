# -*- coding:utf-8 -*-
import re

# SONGID = '190449'
SINGERNAME = '陈奕迅'
# LIMIT_NUM = 100  # 限制一次爬多少条
LIMIT_NUM = 20  # 限制一次爬多少条

PATTERN = re.compile(r'[\n\t\r\/]')  # 替换掉评论中的特殊字符以防插入数据库时报错

DATABASE = 'nbc_comments'
TABLE_COMMENTS = 'nbc_comments2'
TABLE_USERS = '****'
HOST = '127.0.0.1'
USER = 'root'
PASSWD = 'root123'

# ROOT_URL = 'http://music.163.com/api/v1/resource/comments/R_SO_4_' + SONGID + '?limit=' + str(LIMIT_NUM) + '&offset=%s'



HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.44',
    'Host': 'music.163.com',
    'Cookie': 'WM_TID=MycNB38YfKlABRBAEEd+balQoV4Ccb3C; NMTID=00Omn7LXVF_8-_KlUq3hDHRyQ_CRxEAAAF24MMOIQ; _ntes_nuid=ea51e598694143d9cb6c4e64d0e23880; nts_mail_user=Ovaltine2333@163.com:-1:1; _iuqxldmzr_=32; _ntes_nnid=ea51e598694143d9cb6c4e64d0e23880,1650469247218; WNMCID=wfazgk.1650469251072.01.0; WEVNSM=1.0.0; WM_NI=TzsCQoVgfYlTnKEILcBMLwfzEoKPxdDMPYPleEtCrqsGuK1Fi2c2cAQiVTWa4m7/NmTIzfY4eRRiJGPOBwZgA0cpAcwHzu/2oBtPxwTuOWa2kUrUaC+IYheoaXOV1wOsYXY=; WM_NIKE=9ca17ae2e6ffcda170e2e6eeabf862b79783ccd149fbb08ba6d85f968f8b82c45a8c8d0084cc6d868fa6a3b72af0fea7c3b92a98a6bda4d46596b9aabaef60ae958baacf6982938498e57287b185b1fb708893a0bad368a79bbca4f17bb199bbacb44eabeeadd3e24b93b79ab5d66bf8b3f9d0cd679897b687dc40a78e9e8ac94d94918e98d96d83f0ad91c469b598b696ae3aad9ebcb1fb7d98ab81b8e43aa98bbeb6e449e9979789e865a38881b7b47d8dad97b9dc37e2a3; JSESSIONID-WYYY=F6Mj+BH2bt\mqiw9h9DxEtR4d\z26XSB23lvNjb+Sgt1\K9Iu7/KWCpCD2zY+cS6SvwBZR92Oj8EKYWByrb9DxsJe/+K8jzIMQOM54mZ52Djl74vvayBepG3zWOTD3U8YS295ezYQ\zSt/GepBQMD1cT64127JgVRBDJnmViUl8KrDyR:1650612269426',
}
# HEADERS = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
#     'Host': 'music.163.com',
#     'Cookie': '****',
# }