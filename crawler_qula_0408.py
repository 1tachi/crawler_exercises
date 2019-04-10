'''
target：爬取www.qula站点下的小说
tech：bs4 + requests
python_v: 3.6
os: win10
'''

import bs4
import requests

url = 'https://www.qu.la/paihangbang/'


# 抓取网页内容
def get_html(url):
    try:
        r = requests.get(url, timeout=20)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except:
        return " Something Wrong! "


# print(get_html(url))
# 获取排行榜小说及其链接
def get_content(url):
    '''
    爬取每一类型小说排行榜
    按顺序写入文件
    文件内容为：小说名字+小说链接
    将内容保存到列表并返回一个装满url链接的列表
    :param url:
    :return:
    '''
    url_list = []
    html = get_html(url)
    soup = bs4.BeautifulSoup(html, 'lxml')

    # 处理各个类型
    category_list = soup.find_all('div', class_='index_toplist mright mbottom')
    # 由于小说排版的原因，历史类和完本类小说不在一个div里,需要特殊处理
    history_finished_list = soup.find_all('div', class_='index_toplist mbottom')
    namelist = []
    # 获取排行榜名字
    for cate in category_list:
        name = cate.find('div', class_='toptab').span.string
        # namelist.append(name)
        # with open('novel_list.csv', 'a+') as f:
        #     f.write("\n小说种类：{} \n".format(name))
        ## 我们直接通过style属性来定位总排行榜
        general_list = cate.find(style='display: block;')
        # 找到全部的小说名字，发现他们全部都包含在li标签之中
        book_list = general_list.find_all('li')
        # title_list = []
        # 循环遍历出每一个小说的的名字，以及链接
        for book in book_list:
            link = 'http://www.qu.la/' + book.a['href']
            title = book.a['title']
            # title_list.append(title)
            # 我们将所有文章的url地址保存在一个列表变量里
            url_list.append(link)
            # 保存到文件
            with open('novel_list.csv', 'a') as f:
                f.write("小说名：{:<} \t 小说地址：{:<} \n".format(title, link))

    for cate in history_finished_list:
        name = cate.find('div', class_='toptab').span.string
        # namelist.append(name)
        with open('novel_list.csv', 'a') as f:
            f.write("\n小说种类：{} \n".format(name))
        general_list = cate.find(style='display: block;')
        book_list = general_list.find_all('li')
        for book in book_list:
            link = 'http://www.qu.la/' + book.a['href']
            title = book.a['title']
            url_list.append(link)
            with open('novel_list.csv', 'a') as f:
                f.write("\n小说名：{:<} \t 小说地址：{:<} \n".format(title, link))

    return url_list


# print(get_content(url))
# 获取单本小说的所有章节链接
def get_txt_url(url):
    '''
    获取该小说每个章节的url地址并创建小说文件
    :param url:
    :return:
    '''
    url_list = []
    html = get_html(url)
    soup = bs4.BeautifulSoup(html, 'lxml')
    lista = soup.find_all('dd')
    txt_name = soup.find('h1').text
    with open('C:/Users/xialong/PycharmProjects/untitled1/novel/{}.txt'.format(txt_name), 'a+') as f:
        f.write('小说标题：{} \n'.format(txt_name))

    for url in lista:
        url_list.append('http://www.qu.la/' + url.a['href'])

    return url_list, txt_name


# print(get_txt_url(url))
# 获取单页文章的内容并保存到本地
def get_one_txt(url, txt_name):
    '''
    获取小说每个章节的文本并写入本地
    :param url:
    :param txt_name:
    :return:
    '''
    html = get_html(url).replace('<br/>', '\n')
    soup = bs4.BeautifulSoup(html, 'lxml')
    try:
        txt = soup.find('div', id='content').text.replace('chaptererror();', '')
        title = soup.find('title').text

        with open('C:/Users/xialong/PycharmProjects/untitled1/novel/{}.txt'.format(txt_name), "a") as f:
            f.write(title + '\n\n')
            f.write(txt)
            print('当前小说：{}  当前章节{} 已经下载完毕'.format(txt_name, title))
    except:
        print("something wrong in get_one_txt()!")


# 获取所有小说内容
def get_all_txt(url_list):
    '''
    下载排行榜所有小说并保存为txt
    :param url_list:
    :return:
    '''
    for url in url_list:
        # 遍历获取当前小说所有章节并生成小说文件头
        page_list, txt_name = get_txt_url(url)
    for page_url in page_list:
        # 遍历每一篇小说并下载到目录
        get_one_txt(page_url, txt_name)
        print('当前进度 {}% '.format(url_list.index(url) / len(url_list) * 100))
    #print(page_list,txt_name)

def main():
    # 排行榜地址
    base_url = 'http://www.qu.la/paihangbang/'
    # 获取排行榜中所有小说的url
    url_list = get_content(base_url)
    # 除去重复小说，增加效率
    url_list = list(set(url_list))
    #print(url_list)
    get_all_txt(url_list)


if __name__ == '__main__':
    main()
