from urllib import request
from bs4 import BeautifulSoup
import random
# import time
import json
from douban_spider_ver1 import output




    
def downloader(url):
    if url is None:
        return None
    req = request.Request(url)
    hds=['User-Agent,Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',\
        'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11',\
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)',\
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36']
    hd=hds[random.randint(0,3)]
    req.add_header('User-Agent',hd)
    page_content = request.urlopen(req).read()
    return page_content
     
     


def fst_page_urls(url):
    urls = []
    content1 = downloader(url).decode()
    content2 = json.loads(content1)
    L = content2['subjects']
    for l in L:
        urls.append(l['url'])
    return urls


def html_parser(cont,url): 
    
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
    
    return page_date
    
class spider_main(object): 
    def __init__(self):
        self.outputer=output.html_output()  
    def craw(self,fst_url):
        page_urls = fst_page_urls(fst_url)
        for get_url in page_urls:
            content = downloader(get_url)
#             time.sleep(random.uniform(1,2))
            tv_date = html_parser(content,get_url)
            self.outputer.collect_data(tv_date)
        self.outputer.Html_output()
        
    
if __name__=='__main__': 
    fst_url='https://movie.douban.com/j/search_subjects?type=tv&tag=%E7%BE%8E%E5%89%A7&sort=time&page_limit=20&page_start=0'
    obj_spider=spider_main()
    obj_spider.craw(fst_url)
    
     
     


    



    

   
   
     
           
        
        
        
        
    
    