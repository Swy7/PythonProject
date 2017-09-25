from datetime import datetime, timedelta

import requests 
from bs4 import BeautifulSoup
import pymysql


class news_spider(object):
    def __init__(self,url,l):
        self .url = url
        self .l = l
    def news(self):
        headers = {'Host':"www.dongqiudi.com",
                   "Accept": "*/*",
                   "Accept-Encoding": "gzip, deflate",
                   "Accept-Language": "zh-CN,zh;q=0.8",
                   "Connection": "keep-alive",
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
                   }      
        r = requests.get(self.url,headers=headers,timeout=10)
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
        url = "https://www.dongqiudi.com/data/team/archive?team=50001756&page={0}".format(i)
        braca_news = news_spider(url,fcb)
        braca_news.news()
    return fcb


#西甲新闻 
def li_liga():
    liga = []        
    for i in [1,2]:
        url = "http://www.dongqiudi.com/archives/5?page={0}".format(i)
        liga_news = news_spider(url,liga)
        liga_news.news()
    return liga


#昨，近，明所有重要赛事，赛况
def rencent_match():
    now = datetime.now().strftime('%Y-%m-%d')
    url = "http://www.dongqiudi.com/match/fetch_new?tab=null&date={0}&scroll_times=0&tz=-8".format(now)    
    headers = {'Host':"www.dongqiudi.com",
               "Accept": "*/*",
               "Accept-Encoding": "gzip, deflate",
               "Accept-Language": "zh-CN,zh;q=0.8",
               "Connection": "keep-alive",
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
               }
    r = requests.get(url,headers=headers,timeout=10)
    a = r.json()['html']
    soup = BeautifulSoup(a,'html.parser')
    match_table = soup.find('table',class_='list')
    match_data = []
    match_tr = match_table.find_all('tr')
    #找出表示时间的‘tr’的下标
    a=[]
    for tr in match_tr:
        if tr.find('th'):
            b = match_tr.index(tr)
            a.append(b)
        else:
            pass
    #昨天所有重要赛事       
    for y_tr in match_tr[a[0]+1:a[1]]:
        y_td = y_tr.find_all('td')
        y_time = "".join(y_td[0].get_text().split())
        y_round = "".join(y_td[1].get_text().split())
        y_home_team = "".join(y_td[2].get_text().split())
        if y_td[3].get_text() == 'VS':
            y_score = '无'
        else:
            y_score = y_td[3].get_text()
        y_visiting_team = "".join(y_td[4].get_text().split())
        y_date = 'yesterday'
        match_data.append([y_time,y_round,y_home_team,y_visiting_team,y_score,y_date])
    #今天所有重要赛事       
    for t_tr in match_tr[a[1]+1:a[2]]:
        t_td = t_tr.find_all('td')
        t_time = "".join(t_td[0].get_text().split())
        t_round = "".join(t_td[1].get_text().split())
        t_home_team = "".join(t_td[2].get_text().split())
        if t_td[3].get_text() == 'VS':
            t_score = '无'
        else:
            t_score = t_td[3].get_text()
        t_visiting_team = "".join(t_td[4].get_text().split())
        t_date = 'today'
        match_data.append([t_time,t_round,t_home_team,t_visiting_team,t_score,t_date])
    #明天所有重要赛事       
    for tom_tr in match_tr[a[2]+1:a[3]]:
        tom_td = tom_tr.find_all('td')
        tom_time = "".join(tom_td[0].get_text().split())
        tom_round = "".join(tom_td[1].get_text().split())
        tom_home_team = "".join(tom_td[2].get_text().split())
        if tom_td[3].get_text() == 'VS':
            tom_score = '无'
        else:
            tom_score = tom_td[3].get_text()
        tom_visiting_team = "".join(tom_td[4].get_text().split())
        tom_date = 'tomorrow'
        match_data.append([tom_time,tom_round,tom_home_team,tom_visiting_team,tom_score,tom_date])
    return match_data
    

#巴萨比赛数据
def braca_match():
    url = 'https://www.dongqiudi.com/team/50001756.html'  
    headers = {'Host':"www.dongqiudi.com",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
               "Accept-Encoding": "gzip, deflate",
               "Accept-Language": "zh-CN,zh;q=0.8",
               "Connection": "keep-alive",
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
               }
    r = requests.get(url,headers=headers)
    soup = BeautifulSoup(r.text,'html.parser')
    #巴萨赛程，赛况抓取
    braca_table = soup.find('table',class_='schedule_list')
    braca_data=[]
    for braca_tr in braca_table.find_all('tr'):
        braca_td = braca_tr.find_all('td')
        #将时间改为本地时间
        time = braca_td[0].get_text()
        a = datetime.strptime(time,'%Y-%m-%d %H:%M:%S')
        b = a+timedelta(hours=8)
        match_time = datetime.strftime(b,'%Y-%m-%d %H:%M:%S')
        gameweek = "".join(braca_td[2].get_text().split()) 
        home_team = braca_td[3].get_text().strip()
        home_img = braca_td[3].find('img').get('src')
        # 将还未比赛的比分数改为“无”
        if braca_td[4].find(class_='fs_a').get_text():
            home_score = braca_td[4].find(class_='fs_a').get_text()
        else:
            home_score = '无'
        if braca_td[4].find(class_='fs_b').get_text():
            visiting_score = braca_td[4].find(class_='fs_b').get_text()
        else:
            visiting_score = '无'
        visiting_team = braca_td[5].get_text().strip()
        visiting_img = braca_td[5].find('img').get('src')
        match = [match_time,gameweek,home_team,visiting_team,home_score,visiting_score,home_img,visiting_img]
        braca_data.append(match)
    #西甲rank抓取
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
    return braca_data, ranking_data
     

#存入数据
def load_data(fcb,liga,match_data,braca_data,ranking_data):
    db = pymysql.connect('localhost','dogger','123456','test',charset="utf8")
    cur = db.cursor()
    #写入巴萨新闻
    try:
        cur.execute("TRUNCATE braca_news")
        db.commit()
    except Exception as e:
        print(e)  
        db.rollback() 
    try:
        bracanews_sql = "INSERT INTO braca_news(title,display_time,web_url)\
        VALUES (%s,%s,%s)"
        cur.executemany(bracanews_sql,fcb)
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
    #写入近期比赛
    try:
        cur.execute("TRUNCATE recent_match")
        db.commit()
    except Exception as e:
        print(e)  
        db.rollback() 
    try:
        match_sql = "INSERT INTO recent_match(match_time,round,home_team,visiting_team,score,\
        data)VALUES (%s,%s,%s,%s,%s,%s)"
        
        cur.executemany(match_sql,match_data)
        db.commit()
    except Exception as e:
        print(e)  
        db.rollback()   
    #写入巴萨赛程，赛况
    try:
        cur.execute("TRUNCATE braca_data")
        db.commit()
    except Exception as e:
        print(e)  
        db.rollback()   
    try:
        bracamatch_sql = "INSERT INTO braca_data(match_time,gameweek,home_team,visiting_team,\
        home_score,visiting_score,home_img,visiting_img) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        cur.executemany(bracamatch_sql,braca_data)
        db.commit()
    except Exception as e:
        print(e)  
        db.rollback()
    #写入西甲联赛rank
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
    cur.close()
    db.close()

         
if __name__=='__main__':        
    fcb = braca()
    liga = li_liga()
    match_data = rencent_match()
    braca_data,ranking_data = braca_match()
    load_data(fcb, liga, match_data, braca_data, ranking_data)


               
               


               

