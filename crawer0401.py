import requests
from lxml import etree
import json

class TiebaSpider():
    def __init__(self,tieba_name):
        #1. start_url
        self.start_url ="http://tieba.baidu.com/mo/q---7112720F93F044C1D5F86BE78568340B%3AFG%3D1-sz%40320_240%2C-1-3-0--2--wapp_1533811534530_135/m?kw={}&lp=5011".format(tieba_name)
        self.headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Mobile Safari/537.36"}
        self.part_url = "http://tieba.baidu.com/mo/q---7112720F93F044C1D5F86BE78568340B%3AFG%3D1-sz%40320_240%2C-1-3-0--2--wapp_1533811534530_135"

    # 2.发送请求获取数据
    def parse_url(self,url):
        print(url)
        response = requests.get(url,headers=self.headers)
        return response.content

    # 3.提取数据
    def get_content_list(self,html_str):
        html = etree.HTML(html_str)
        div_list = html.xpath("//body/div/div[contains(@class,'i')]")
        content_list = []
        for div in div_list:
            item = {}
            item["href"] = self.part_url+div.xpath("./a/@href")[0]
            item["title"] = div.xpath("./a/text()")[0]
            item["img_list"] = self.get_img_list(item["href"],[])
            content_list.append(item)

        # 提取下一页的url地址
        next_url = html.xpath("//a[text()='下一页']/@href")
        next_url = self.part_url + next_url[0] if len(next_url) > 0 else None
        return content_list, next_url


    # 获取图片的列表
    def get_img_list(self,detail_url,img_list):
        # 1.发送请求,获取响应
        detail_html_str = self.parse_url(detail_url)
        # 2.提取数据
        detail_html = etree.HTML(detail_html_str)
        img_list += detail_html.xpath("//img[@class='BDE_Image']/@src")


        # 3.获取下一页的url地址,然后加以保存
        next_url = detail_html.xpath("//a[text()='下一页']/@href")
        next_url = self.part_url + next_url[0] if len(next_url) > 0 else None
        if next_url is not None: #当存在详情页的下一页，请求
            return self.get_img_list(next_url,img_list)

        img_list = [requests.utils.unquote(i).split("src=")[-1] for i in img_list]

        # 4. 保存
        with open("tbtupian.txt", "a", encoding="utf-8") as f:
            for content in img_list:
                f.write(json.dumps(content, ensure_ascii=False))
                f.write("\n")
        print("保存成功")


    # 4.保存数据
    def save_content_list(self,content_list):
        with open("tieba.txt", "a", encoding="utf-8") as f:
            for content in content_list:
                f.write(json.dumps(content, ensure_ascii=False))
                f.write("\n")
        print("保存成功")


    def run(self): #实现主要逻辑
        next_url = self.start_url
        while next_url is not None:
            #1. start_url
            #2. 发送请求，获取响应
            html_str = self.parse_url(next_url)
            #3. 提取数据
            content_list,next_url = self.get_content_list(html_str)
            #4。保存
            self.save_content_list(content_list)
            #5.获取next_url，循环2-5

if __name__ == '__main__':
    tieba = TiebaSpider("美女")
    tieba.run()
