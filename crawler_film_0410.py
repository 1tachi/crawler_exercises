'''
爬取http://dianying.2345.com/top/ 电影
tech: requests --- bs4
python_v: 3.6
os: win10
'''

import  requests
import bs4

def get_hmtl(url):
    try:
        r = requests.get(url,timout=30)
        r.raise_for_status()
        r.encoding = 'gbk'
        return r.text
    except:
        return "somting wrong with get_html!"

#获取网站内容
def get_content(url):
    html = get_hmtl(url)
    soup = bs4.BeautifulSoup(html, 'lxml')
    print(html)
    # 找到电影排行榜的ul列表
    movies_list = soup.find('ul', class_='picList clearfix')
    print(movies_list)
    movies = movies_list.find_all('li')


    for top in movies:
        # 找到图片链接
        img_url = top.find('img')['src']

        name = top.find('span', class_='sTit').a.text
        # 这里做一个异常捕获，防止没有上映时间的出现
        try:
            time = top.find('span', class_='sIntro').text
        except:
            time = "暂无上映时间"

        # 这里用bs4库迭代找出“pACtor”的所有子孙节点，即每一位演员解决了名字分割的问题
        actors = top.find('p', class_='pActor')
        actor = ''
        for act in actors.contents:
            actor = actor + act.string + ' '
        # 找到影片简介
        intro = top.find('p', class_='pTxt pIntroShow').text
        print("片名：{}\t{}\n{}\n{} \n \n".format(name, time, actor, intro))

        # 下载图片
        with open('./img/' + name + '.png', 'wb+') as f:
            f.write(requests.get(img_url).content)

def main():
    url = 'http://dianying.2345.com/top/'
    get_content(url)

if __name__ == '__main__':
    main()