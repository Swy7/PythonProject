from functools import reduce
from itertools import chain

import pymysql
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import pandas.io.sql as sql

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

#评分top10电影
rating=sql.read_sql_query('select title,rating_num from movie order by rating_num desc limit 10',conn)

plt.figure(figsize=(8,4))
x1=np.arange(len(rating))+1
y1=rating.rating_num
plt.xticks(x1,rating.title,size='small',rotation=90,fontproperties=font,fontsize=14)
plt.grid(True)
plt.xlabel('名称',fontproperties=font,fontsize=14)
plt.ylabel('评分',fontproperties=font,fontsize=14)
plt.title('评分top10电影',fontproperties=font,fontsize=14)
for i in range(len(rating)):
    plt.text(x1[i], y1[i]+0.05,'%s分' % y1[i], ha='center', va= 'bottom',fontproperties=font,fontsize=14)
plt.bar(x1,y1)

#评论top10电影
comment=sql.read_sql_query('select title,rating_num,comment_num from movie order by comment_num desc limit 10',conn)

plt.figure(figsize=(8,4))
x2=np.arange(len(comment))+1
y2=comment.comment_num
plt.xticks(x2,comment.title,size='small',rotation=90,fontproperties=font,fontsize=14)
plt.grid(True)
plt.xlabel('名称',fontproperties=font,fontsize=14)
plt.ylabel('评论数',fontproperties=font,fontsize=14)
plt.title('评论top10电影',fontproperties=font,fontsize=14)
for i in range(len(comment)):
    plt.text(x2[i], y2[i]+0.05,'%s分' % comment.rating_num[i], ha='center', va= 'bottom',fontproperties=font,fontsize=14)
plt.bar(x2,y2)

#导演作品出现次数
dire=sql.read_sql_query('select director,count(*) as num from movie group by director having num >2 order by num desc',conn)

plt.figure(figsize=(8,4))
x3=np.arange(len(dire))+1
y3=dire.num
plt.xticks(x3,dire.director,size='small',rotation=90,fontproperties=font,fontsize=14)
plt.grid(True)
plt.xlabel('导演',fontproperties=font,fontsize=14)
plt.ylabel('次数',fontproperties=font,fontsize=14)
plt.title('导演作品出现次数',fontproperties=font,fontsize=14)
plt.bar(x3,y3)

cursor.close()
conn.close()