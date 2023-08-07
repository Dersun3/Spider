# -*- coding: utf-8 -*-
# @ author:爱分享的山哥
# @ time:2022/3/9 0009:19:21

import requests
import re
from lxml import etree
import os
import time
import random


def getHeaders():
    '''user_agent简单伪装'''
    user_agent_list = [\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1" \
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6", \
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", \
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", \
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", \
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", \
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]
    UserAgent = random.choice(user_agent_list)
    headers = {'User-Agent': UserAgent}
    return headers
headers = getHeaders()  # 调用函数，随机选出一个headers


def song_down(sort_id,save_path):
    # 歌曲路径
    try:
        filename = save_path + '\\'
        if not os.path.exists(filename):
            os.mkdir(filename)
    except:
        print('文件无法创建！')

    try:
        # 歌曲下载
        url = 'https://music.163.com/discover/toplist?id={}'.format(sort_id)
        # ,proxies={"https":'222.110.147.50:3128'}
        res = requests.get(url=url,headers=headers).text
        ex = '<li><a href="/song\?id=(\d+)">(.*?)</a></li>'
        data = re.findall(ex,res)
        for id,name in data:
            music_url = f'http://music.163.com/song/media/outer/url?id={id}.mp3'  # 音乐下载接口
            music_data = requests.get(url=music_url,headers=headers).content
            with open(filename+name+'.mp3',mode='wb') as fp:
                fp.write(music_data)
            print('%s-------下载完毕！'%name)
            time.sleep(1)  # 避免下载时间过快
    except:
        print('%s无法下载!'%name)


def user_server():
    '''用户操作区'''
    print('=====================网易云音乐下载===============================')
    print("""    0:飙升榜                 1:新歌榜             2:原创榜       =                 
    3:热歌榜                 4:云音乐说唱榜       5:云音乐ACG榜  =       
    6:云音乐国电榜           7:云音乐欧美热歌榜   8:网络热歌榜   =       
    9:中文DJ榜                                                   =""")
    print('=' * 66)

    num = int(input('请输入要下载榜单对应的数字：'))     # 榜单id
    save_path = input("请输入要保存的路径:")           # 下载路径
    print(save_path)
    # 存储各个歌榜的ID
    id_list = ['19723756', '3779629', '2884035', '3778678', '991319590', '71385702', '10520166', '2809513713',
               '6723173524', '6886768100']

    for i in range(0, 10):
        try:
            if num == i:
                song_down(id_list[i],save_path)
            else:
                print('你的输入有误！')
                break
        except Exception as e :
            print('你的输入有误！',e)
            continue



if __name__=='__main__':
    user_server()
