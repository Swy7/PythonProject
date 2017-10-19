from functools import reduce
from itertools import chain

import pymysql
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties


conn = pymysql.connect(user='dog',password='123456',database='dog1',charset='utf8')
cursor = conn.cursor()
cursor.execute('SELECT DISTINCT place FROM movie')
a = cursor.fetchall()
b=[]
for i in a:
    b.append(i[0].split(','))
c=list(set(reduce(chain,b)))
d=[]
for x in c:
    cursor.execute("select count(place),round(avg(rating_num),1) from movie where place like '%{0}%'".format(x))
    d.append(cursor.fetchone())
g=np.array(d)
cursor.execute('select movie_time,count(*) from movie group by movie_time')
h=np.array(cursor.fetchall())
cursor.execute('select movie_time,round(avg(rating_num),1) from movie group by movie_time')
r=np.array(cursor.fetchall())

cursor.close()
conn.close()
#添加字体，可以显示中文
font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc")
#top250电影时间-数量分布
plt.figure(figsize=(15, 4))
plt.xticks(np.arange(1930,2020,5))
plt.grid(True)
plt.xlabel('年份',fontproperties=font,fontsize=14)
plt.ylabel('数量',fontproperties=font,fontsize=14)
plt.title('top250电影时间-数量分布',fontproperties=font,fontsize=14)
plt.bar(h[:,0], h[:,1])
#top250电影时间-分数分布
plt.figure(figsize=(15, 4))
plt.xticks(np.arange(1930,2020,5))
plt.grid(True)
plt.xlabel('年份',fontproperties=font,fontsize=14)
plt.ylabel('分数',fontproperties=font,fontsize=14)
plt.title('top250电影时间-分数分布',fontproperties=font,fontsize=14)
plt.bar(r[:,0], r[:,1])
#top250电影地区-数量-均分分布
plt.figure(figsize=(15, 4))
plt.xticks(np.arange(len(g))+1,c,size='small',rotation=90,fontproperties=font,fontsize=14)
plt.grid(True)
plt.xlabel('地区',fontproperties=font,fontsize=14)
plt.ylabel('数量',fontproperties=font,fontsize=14)
plt.title('top250电影地区分布',fontproperties=font,fontsize=14)
x=np.arange(len(g))+1
y=g[:,0]
z=g[:,1]
#给每个柱状图加上<均分>标签
for i in np.arange(len(g)):
    plt.text(x[i], y[i]+0.05,'均分%s' % z[i], ha='center', va= 'bottom',fontproperties=font,fontsize=7)
plt.bar(x,y)




