# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os


class ZhaobiaoproPipeline:
    def process_item(self, item, spider):
        projectName = item["projectName"]
        date = item["date"]
        context = item["context"]
        value = item["value"]
        html = """
                            <!DOCTYPE html>
                                <html lang="en">
                                <head>
                                  <meta charset="UTF-8">
                                  <title>Title</title>
                                </head>
                                <body>
                                {}<br>{}
                                </body>
                                </html>
                        """.format(projectName + " : " + date, context)

        # 获取当前的文件目录
        base_dir = os.getcwd()
        All_Path = base_dir+"\\项目文件"
        if not os.path.exists(All_Path):
            os.makedirs(All_Path)

        # 分类
        Branch_Path = All_Path + "\\"+value
        if not os.path.exists(Branch_Path):
            os.makedirs(Branch_Path)

        # 数据存储
        File_Name = Branch_Path + "\\"+projectName+'.html'
        with open( File_Name, 'w',encoding='utf-8') as fp:
            fp.write(html)
            print("{}.html下载完毕!".format(projectName))
        return item

