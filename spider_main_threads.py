from urllib import request
from bs4 import BeautifulSoup
import random
import time
import json
import threading

import queue






    

     


def fst_page_urls(url):
    
    req = request.Request(url)
    hds=['User-Agent,Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',\
        'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11',\
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)',\
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36']
    hd=hds[random.randint(0,3)]
    req.add_header('User-Agent',hd)
    content = request.urlopen(req).read()
    content1 = content.decode()
    content2 = json.loads(content1)
    L = content2['subjects']
    for l in L:
        q.put(l['url'])
    


def spider():
    
    url=q.get()
    req = request.Request(url)
    hds=['User-Agent,Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',\
        'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11',\
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)',\
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36']
    hd=hds[random.randint(0,3)]
    req.add_header('User-Agent',hd)
    cont = request.urlopen(req).read()
    
    
    soup = BeautifulSoup(cont,'html.parser',from_encoding='utf-8')
    page_date = {}
    page_date['pic'] = soup.find('div',id="mainpic",class_="").find('img')['src']
    page_date['title'] = soup.find('span',property="v:itemreviewed").string
    page_date['rating_num'] = soup.find('strong',class_="ll rating_num",property="v:average").string
    page_date['type'] = soup.find('span', property="v:genre").string
    page_date['url'] = url
    director_node = soup.find('span', class_="pl", text='导演')
    try:
        director = director_node.find_all_next(text=True, limit=7)
        page_date['director'] = " ".join(director)
    except:
        page_date['director']='暂无'
    
    actor_node = soup.find('span', class_="pl", text='主演')
    try:
        actor = actor_node.find_all_next(text=True, limit=7)
        page_date['actor'] = " ".join(actor)
    except:
        page_date['actor']='暂无'
    
    summary_node = soup.find('span', property="v:summary")
    try:
        page_date['summary'] = summary_node.get_text()
    except:
        page_date['summary']='暂无'
   
    lock = threading.Lock()
    lock.acquire()
    try:        
        cont_dates.append(page_date)
    finally:
            
        lock.release()
    
    q.task_done() 


def Html_output():
#   将电视剧按评分排序，加入序号，分为sort_dates1，sort_dates2，在html页面输入两列
    html_dates=cont_dates
    sort_dates=sorted(html_dates,key=lambda x:x['rating_num'],reverse=True)
    
    for i in range(len(sort_dates)):
        sort_dates[i]['order']=i+1
    
    sort_dates1=sort_dates[::2]
    
    sort_dates2=sort_dates[1::2]
    
    with open('tv.html','w') as f:
        htmlhead="""
        <!DOCTYPE html>
        <html>
        <head>
        <title>最近剧集排名</title>
        <base target="_blank"/>
        <style type="text/css">
        p {font-size:20px;}
        .outset {border-bottom-style:outset}
        header {
                background-color:black;
                color:white;
                text-align:center;
                padding:5px;
        }
        
        
         .main-left{
            width:50%;
            float:left;
        }
        
         .main-right{
            width:50%;
            float:right;
        }        
        
        footer {
                background-color:black;
                color:white;
                clear:both;
                text-align:center;
                padding:5px;
        }
        
        </style>
        </head>
         <body>
        <header>
        <h1>近期美剧排名</h1>
        </header>
        
        """
        f.write(htmlhead)
    
    f=open('tv.html','a+')
    f.writelines('<div class="main-left">')
    for date1 in sort_dates1:
        f.writelines('<img src= %s  width="230" height="300">' % date1['pic'])
        f.writelines('<a href=%s >点击此处查看电影详情</a>' % date1['url'])
        f.writelines('<p class="outset">排名：%s<br />剧名： %s<br />评分：%s<br />%s<br />%s<br />类型： %s<br />简介：%s</p>'\
         % (date1['order'],date1['title'],date1['rating_num'],date1['director'],date1['actor']\
        ,date1['type'],date1['summary']))
    f.writelines('</div>')
    f.writelines('<div class="main-right">')
    for date2 in sort_dates2:
        f.writelines('<img src= %s width="230" height="300">' % date2['pic'])
        f.writelines('<a href= %s>点击此处查看电影详情</a>' % date2['url'])
        f.writelines('<p class="outset">排名：%s<br />剧名： %s<br />评分：%s<br />%s<br />%s<br />类型： %s<br />简介：%s</p>'\
        % (date2['order'],date2['title'],date2['rating_num'],date2['director'],date2['actor']\
        ,date2['type'],date2['summary']))
    f.writelines('</div>')     
    f.writelines('<footer>不要问页面为何这么难看</footer>')
    f.writelines('</body>')
    f.writelines('</html>')
    f.close
    

    
   


   


#     
# 
# def craw(fst_url):
#    
#     time_start=time.time()
#    
#     fst_page_urls(fst_url)
#     
#     threads_num = 3
#     for i in range(threads_num):  
#         t = threading.Thread(target=spider)
#         t.start()
#        
#     share_q.join()  
#     Html_output()
#     time_end=time.time() 
#     print(time_end-time_start)
#     
class MyThread(threading.Thread) :

    def __init__(self, func) :
        threading.Thread.__init__(self)   #调用父类的构造函数
        self.func = func  #传入线程函数逻辑

    def run(self) :
        while not q.empty():
            self.func()
        return    
       
            
            

             
        
    
if __name__=='__main__': 
    fst_url='https://movie.douban.com/j/search_subjects?type=tv&tag=%E7%BE%8E%E5%89%A7&sort=time&page_limit=20&page_start=0'
       
   
    q=queue.Queue()
    cont_dates=[]
    time_start=time.time()
   
    fst_page_urls(fst_url)
    
        
    for i in range(6):  
        t = MyThread(spider)
        
        t.start()
    q.join()  
      
     
    Html_output()
    time_end=time.time() 
    print(time_end-time_start)
    
     
     


    



    

   
   
     
           
        
        
        
        
    
    