import scrapy
import json
from scrapy.http import JsonRequest,FormRequest
from scrapy import Request
from zhaobiaoPro.items import ZhaobiaoproItem


class ZhaobiaoSpider(scrapy.Spider):
    name = 'zhaobiao'
    # allowed_domains = ['www.baidu.com']
    # start_urls = ["https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyzyCenter/jyInfo/gcjs/getTenserPlanList"]
    # 招标
    zhao_url = "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyzyCenter/jyInfo/gcjs/getTenserPlanList"
    # 中标
    zhong_url = "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyzyCenter/jyInfo/gcjs/getZbJgGgList"
    lis = ["招标","中标"]

    def start_requests(self):
        for li in self.lis:
            if li == "招标":
                url = self.zhao_url
                value = li
            else:
                url = self.zhong_url
                value = "中标"

            # 分页(爬取前两页
            for i in range(1, 2):
                data = {
                    "childType":"",
                    "cityId":"018",
                    "endTime":"",
                    "industryCode":"",
                    "pageNum":str(i),
                    "pageSize":"10",
                    "startTime":"",
                    "title":"",
                    "tradeType":"gcjs"
                }
                print("获取{}第{}页完毕！".format(value,i))
                yield JsonRequest(url=url,data=data,callback = self.get_id,meta={'value':value})


    def get_id(self, response):
        id_list = []
        res = json.loads(response.text)
        li_list = res["value"]["list"]
        value = response.meta['value']
        for li in li_list:
            if value == "招标":
                url = "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyzyCenter/jyInfo/gcjs/getTenserPlanDetail?guid={}"
            else:  # 中标
                url = "https://ggzy.yn.gov.cn/ynggfwpt-home-api/jyzyCenter/jyInfo/gcjs/findZbJgGgByGuid?guid={}"
            detail_url = url.format(li["guid"])
            yield Request(url=detail_url, callback=self.get_data,meta={'value':value})


    def get_data(self,response):
        res = json.loads(response.text)
        value = response.meta['value']
        if value == "招标":
            projectName = res["value"]["projectName"]
            date = res["value"]["blockBaseDTO"]["time"]
            context = res["value"]["content"]
        else:
            projectName = res["value"]["bulletinname"]
            date = res["value"]["bulletinissuetime"]
            context = res["value"]["bulletincontent"]

        item = ZhaobiaoproItem()
        item['projectName'] = projectName
        item['date'] = date
        item['context'] = context
        item['value'] = value
        yield item


