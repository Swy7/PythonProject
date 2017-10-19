import threading

import requests
from bs4 import BeautifulSoup
import pymysql

def download(i):
    headers = {'Host':'movie.douban.com',
               'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept - Language': 'zh-CN,zh;q=0.8',
               'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
              }
    url = 'https://movie.douban.com/top250?start={0}'.format(i)
    re = requests.get(url,headers=headers)
    soup = BeautifulSoup(re.text,'html.parser')
    ol = soup.find('ol',class_='grid_view')
    lis = ol.find_all('li')
    for li in lis:
        title = li.find('span',class_='title').string
        content = li.find('p').get_text().split('/')
        director = content[0].split()[1]
        time = int(content[-3].split()[-1])
        place = ','.join(content[-2].split())
        movie_type = ','.join(content[-1].split())
        span = li.find(class_='star').find_all('span')
        rating_num = float(span[1].string)
        comment_num = int(span[3].string.replace('人评价',''))
        data.append([title,director,time,place,movie_type,rating_num,comment_num])

def load_data(data):
    db = pymysql.connect('localhost','dog','123456','dog1',charset="utf8")
    cur = db.cursor()
    try:
        sql = "INSERT INTO movie(title,director,movie_time,place,movie_type,rating_num,comment_num)\
              VALUES (%s,%s,%s,%s,%s,%s,%s)"
        cur.executemany(sql, data)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()


if __name__=='__main__':
    l=[x*25 for x in range(10)]
    data=[]
    threads = []
    for i in l:
        t = threading.Thread(target=download,args=(i,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    load_data(data)


