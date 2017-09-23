from datetime import datetime, timedelta

import requests 
from bs4 import BeautifulSoup
import pymysql


class news_spider(object):
    def __init__(self,url,l):
        self .url = url
        self .l = l
    def news(self):
        headers = {'content-type': 'application/json','User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
        r = requests.get(self.url,headers=headers)
        a=r.json()['data']
        
        for x in a:
            b = x['title']
            c = x['display_time']
            d= x['web_url']
            e = [b,c,d]
            self.l.append(e)


#巴萨新闻
def braca():
    fcb = []        
    for i in [1,2]:
        url = "https://www.dongqiudi.com/data/team/archive?team=50001756&page=i"
        braca_news = news_spider(url,fcb)
        braca_news.news()
    return fcb

#西甲新闻 
def li_liga():
    liga = []        
    for i in [1,2]:
        url = "http://www.dongqiudi.com/archives/5?page=i"
        liga_news = news_spider(url,liga)
        liga_news.news()
    return liga

#巴萨比赛数据
def match_data():
    url = 'https://www.dongqiudi.com/team/50001756.html'  
    headers = {'content-type': 'application/json','User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
    r = requests.get(url,headers=headers)
    soup = BeautifulSoup(r.text,'html.parser')
    #赛程抓取
    match_table = soup.find('table',class_='schedule_list')
    match_data=[]
    for match_tr in match_table.find_all('tr'):
        match_td = match_tr.find_all('td')
        #将时间改为本地时间
        time = match_td[0].get_text()
        a = datetime.strptime(time,'%Y-%m-%d %H:%M:%S')
        b = a+timedelta(hours=8)
        match_time = datetime.strftime(b,'%Y-%m-%d %H:%M:%S')
        gameweek = "".join(match_td[2].get_text().split()) 
        home_team = match_td[3].get_text().strip()
        home_img = match_td[3].find('img').get('src')
        # 将还未比赛的比分数改为“无”
        if match_td[4].find(class_='fs_a').get_text():
            home_score = match_td[4].find(class_='fs_a').get_text()
        else:
            home_score = '无'
        if match_td[4].find(class_='fs_b').get_text():
            visiting_score = match_td[4].find(class_='fs_b').get_text()
        else:
            visiting_score = '无'
        visiting_team = match_td[5].get_text().strip()
        visiting_img = match_td[5].find('img').get('src')
        match = [match_time,gameweek,home_team,visiting_team,home_score,visiting_score,home_img,visiting_img]
        match_data.append(match)
    #排名抓取
    ranking_table = soup.find('table',class_='scoreboard_list')
    ranking_data=[]
    for ranking_tr in ranking_table.find_all('tr')[1:]:
        ranking_td = ranking_tr.find_all('td')
        rannking=ranking_td[0].get_text()
        team = ranking_td[1].get_text().strip()
        team_img = ranking_td[1].find('img').get('src') 
        gs_ga_gd = "".join(ranking_td[2].get_text().split())
        points=  ranking_td[3].get_text()
        b=[rannking,team,gs_ga_gd,points,team_img]
        ranking_data.append(b)
    return match_data, ranking_data
     

#存入数据
def load_data(fcb,liga,match_data,ranking_data):
    db = pymysql.connect('localhost','dogger','123456','test',charset="utf8")
    cur = db.cursor()
    #写入赛程
    try:
        cur.execute("TRUNCATE match_data")
        db.commit()
    except Exception as e:
        print(e)  
        db.rollback()   
    try:
        match_sql = "INSERT INTO match_data(match_time,gameweek,home_team,visiting_team,\
        home_score,visiting_score,home_img,visiting_img) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        cur.executemany(match_sql,match_data)
        db.commit()
    except Exception as e:
        print(e)  
        db.rollback()
    #写入联赛rank
    try:
        cur.execute("TRUNCATE ranking_data")
        db.commit()
    except Exception as e:
        print(e)  
        db.rollback() 
    try:
        ranking_sql = "INSERT INTO ranking_data(ranking,team,gs_ga_gd,points,team_img)\
        VALUES (%s,%s,%s,%s,%s)"
        cur.executemany(ranking_sql,ranking_data)
        db.commit()
    except Exception as e:
        print(e)  
        db.rollback()
    #写入巴萨新闻
    try:
        cur.execute("TRUNCATE braca_news")
        db.commit()
    except Exception as e:
        print(e)  
        db.rollback() 
    try:
        braca_sql = "INSERT INTO braca_news(title,display_time,web_url)\
        VALUES (%s,%s,%s)"
        cur.executemany(braca_sql,fcb)
        db.commit()
    except Exception as e:
        print(e)  
        db.rollback()
    #写入西甲新闻
    try:
        cur.execute("TRUNCATE la_liga_news")
        db.commit()
    except Exception as e:
        print(e)  
        db.rollback() 
    try:
        la_liga_sql = "INSERT INTO la_liga_news(title,display_time,web_url)\
        VALUES (%s,%s,%s)"
        cur.executemany(la_liga_sql,liga)
        db.commit()
    except Exception as e:
        print(e)  
        db.rollback()
    cur.close()
    db.close()
         

if __name__=='__main__':        
    fcb = braca()
    liga = li_liga()
    match_data,ranking_data = match_data()
    load_data(fcb, liga, match_data, ranking_data)
  
  
    
    
    
    
         
          
    
   

