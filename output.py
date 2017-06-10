class html_output(object):
    def __init__(self):
        self.html_dates=[]
    def collect_data(self,data):
        if data is None:
            return
        self.html_dates.append(data)
    def Html_output(self):
    #   将电视剧按评分排序，加入序号，分为sort_dates1，sort_dates2，在html页面输入两列
        sort_dates=sorted(self.html_dates,key=lambda x:x['rating_num'],reverse=True)
        
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
        
  
        
       

   
       
    
    