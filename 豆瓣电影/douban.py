#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Time    : 2022/3/27 0027 22:13
# @Author  : captain
# @File    : 01.豆瓣爬虫.py
# @Software: PyCharm


import requests
import json
import pprint
import csv
import time


headers = {
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
}
with open('./douban.csv','w',newline='',encoding='utf-8') as fp:  # newline='' :去掉换行
    writer = csv.writer(fp)
    writer.writerow(["标题", "演员", "评分", "排名", "地区", "影片类型", "评论数", "封面图片地址"])
    for i in range(0,11):  # 分页爬取
        try:
            url = "https://movie.douban.com/j/chart/top_list?type=24&interval_id=100%3A90&action=&start={}&limit=20".format(str(i*20))
            res = requests.get(url=url,headers=headers)
            if res.status_code == 200:
                list = res.json()
                for li in list:
                    actors = li["actors"][0]  # 演员
                    src_url = li["cover_url"]  # 封面图片地址
                    rank = li["rank"]  # 排名
                    rating = str(li['score'])  # 评分
                    regions = li["regions"][0]  # 地区
                    title = li['title']  # 标题
                    vote_count = str(li["vote_count"])  # 评论数
                    types = ''.join(li['types'])  # 影片类型
                    writer.writerow([title, actors, rating, rank, regions, types, vote_count, src_url])
        except Exception as e:
            print("爬取出错！")
        print("第%d页爬取完成！"%i)
        time.sleep(2)
print("全部爬取完成！")




