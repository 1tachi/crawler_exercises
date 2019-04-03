import requests
from bs4 import BeautifulSoup
import time
# import sys
# import io
#
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')         #改变标准输出的默认编码


'''
function:爬取生活大爆炸贴吧基本内容
tech: requests 、bs4
python-version: 3.6
os： win10
'''
#url = 'http://tieba.baidu.com/f?kw=%E7%94%9F%E6%B4%BB%E5%A4%A7%E7%88%86%E7%82%B8&ie=utf-8&pn=50'
#url = 'http://tieba.baidu.com/f?kw=%E7%94%9F%E6%B4%BB%E5%A4%A7%E7%88%86%E7%82%B8&ie=utf-8&pn=50'
#url = 'http://tieba.baidu.com/f?kw=%E7%94%9F%E6%B4%BB%E5%A4%A7%E7%88%86%E7%82%B8&ie=utf-8&pn=150'


# 抓取网页的函数
def get_htm(url):
    try:
        r = requests.get(url, timeout=30)
        # 判断请求的页面是否返回正常
        r.raise_for_status()
        # 根据页面编码自动设置相同编码
        # r.encoding = r.apparent_encoding
        r.encoding = 'utf-8'
        #return r.content.decode("utf-8",'ignore')
        return  r.content
    except:
        return "  Error "


# 分析页面内容并爬取
def get_content(url):
    '''
    分析贴吧的文件，整理信息，保存列表在变量中
    :param url:
    :return:
    '''

    # 初始化一个列表来保存所有的帖子
    comments = []
    # 首先，我们把需要爬取信息的网页下载到本地
    html = get_htm(url)

    # 使用Beautifulsoup提取内容
    soup = BeautifulSoup(html, 'lxml')
    # 找到所有具有‘ j_thread_list clearfix’属性的li标签。返回一个列表类型。
    liTags = soup.find_all('li', attrs={'class': 'j_thread_list clearfix'})
    # print(liTags)
    # 通过循环找到每个帖子里的我们需要的信息
    for li in liTags:
        # 初始化一个字典来存储文章信息
        comment = {}
        # 使用一个try:except 防止爬虫找不到信息而停止
        try:
            # 开始筛选信息并保存到字典中
            comment = {}
            comment['title'] = li.find('a', attrs={'class': 'j_th_tit'}).text.strip()
            comment['link'] = "http://tieba.baidu.com/" + li.find('a', attrs={'class': 'j_th_tit'})['href']
            comment['name'] = li.find('span', attrs={'class': 'tb_icon_author'}).text.strip()
            comment['time'] = li.find('span', attrs={'class': 'pull-right is_show_create_time'}).text.strip()
            comment['replyNum'] = li.find('span', attrs={'class': 'threadlist_rep_num center_text'}).text.strip()
            # comment['title'] =
            # comment['title'] =
            comments.append(comment)

        except:
            print('Something Wrong!....')
    return comments


# 保存爬取内容
def Out2File(dict):
    '''
    将爬取到的文件写入到本地, 保存到当前目录的 TTBT.txt文件中
    :param dict:
    :return:
    '''
    with open('TTBT.txt', 'a+') as f:
        for comment in dict:
            f.write('标题：{} \t 链接：{} \t 发帖人：{} \t  发帖时间：{} \t 回复数量：{} \n'.format(comment['title'], comment['link'], comment['name'], comment['time'], comment['replyNum']))
        print('当前页面爬取完成！')


# dict1 = get_content(url)
# Out2File(dict1)

# 主函数
def main(base_url, deep):
    '''
    主函数入口
    :param base_url: http://tieba.baidu.com/f?kw=%E7%94%9F%E6%B4%BB%E5%A4%A7%E7%88%86%E7%82%B8&ie=utf-8
    :param deep: 3
    :return:
    '''
    # 初始化一个列表存取待爬的url
    url_list = []
    # 将所有的要爬取的url 存入列表

    for i in range(0, deep):
        url_list.append(base_url + '&pn=' + str(50 * i))
    print('所有的网页已经下载到本地！ 开始筛选信息。。。。')
    # print(url_list)
    # print(len(url_list))
    # 循环写入所有数据
    for url in url_list:
        content = get_content(url)
        Out2File(content)
    print('所有信息保存完毕！')
    print(content)


base_url = 'http://tieba.baidu.com/f?kw=%E7%94%9F%E6%B4%BB%E5%A4%A7%E7%88%86%E7%82%B8&ie=utf-8'
deep = 3

if __name__ == '__main__':
    main(base_url, deep)
