# -*- coding: utf-8 -*-
import re
import requests
import json
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
import tablib
from pyecharts import Bar
from scipy.misc import imread


s=requests.session()
url='https://club.jd.com/comment/productPageComments.action'
#url='https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv1522&p5&page=0&pageSize=10&isShadowSku=0&fold=1'
data={ 'callback':'fetchJSON_comment98vv1522',
       'productId':'7029545',
       'score':0,
       'sortType':5,
       'page':0,
       'pageSize':10,
       'isShadowSku':0,
       'fold':1 }

hotcomments = []

num=0
while(True):
#for i in range(0,10):
    t=s.get(url,params=data).text

    try:
        t=re.search(r'(?<=fetchJSON_comment98vv1522\().*(?=\);)',t).group(0)
    except Exception as e:
        break
    j=json.loads(t)
    #commentSummary=j['comments']
    commentSummary=j['comments']
    flag=0
    for comment in commentSummary:
        flag=1
        num=num+1
        item = {
            'content': comment['content'] ,
            'nickname': comment['nickname'],
            'score': comment['score'],
            'creationTime':comment['creationTime'],
            'productColor':comment['productColor']
        }
        hotcomments.append(item)
    if flag==0:
        break
    data['page']+=1
    i=data['page']


print num
print data['page']

content_list = [content['content'] for content in hotcomments]
score = [content['score'] for content in hotcomments]
creationTime=[]
for content in hotcomments:
    creationTime.append(int(content['creationTime'][8:10]))



nickname = [content['nickname'] for content in hotcomments]
productColor = [content['productColor'] for content in hotcomments]






a= productColor.count(u'碳黑色')
b=productColor.count(u'酒红色')
c=productColor.count(u'浅金色')
d=float(a+b+c)
a=float(a/d)
b=float(b/d)
c=float(c/d)

ds = tablib.Dataset()
ds.headers = ['颜色', '评论数']

ds.append(['碳黑色',a])
ds.append(['酒红色', b])
ds.append(['浅金色', c])

bar = Bar('颜色')
bar.add('评论数量(%)', ds.get_col(0), ds.get_col(1))
bar.render('color_bar.html')

ds2 = tablib.Dataset()
ds2.headers = ['评价时间', '评论数']
f=0.0
for i in range(9,27):
    f=f+creationTime.count(i)

for i in range(9,27):
    ds2.append([str(i), creationTime.count(i)/f])

bar2 = Bar('评价时间（购买时间）')
bar2.add('评论数量(%)', ds2.get_col(0), ds2.get_col(1))
bar2.render('time_bar.html')


ds3 = tablib.Dataset()
ds3.headers = ['评分', '评论数']
e=0.0
for i in range(0,6):
    j=5-i
    e+=score.count(j)


for i in range(0,5):
    j=5-i
    ds3.append([str(j), score.count(j)/e])

bar3 = Bar('评分')
bar3.add('评论数量(%)', ds3.get_col(0), ds3.get_col(1))
bar3.render('score_bar.html')



stopwords=[u'此用户未填写评价内容']
content_text = " ".join(content_list)
bg_pic = imread('../Pic/Luo3.png')
wordcloud = WordCloud(width=1500,height=2000,stopwords=stopwords,mask=bg_pic,font_path='../Font/SourceHanSansSC-Heavy.otf',background_color='white',max_words=200).generate(content_text)
# 从背景图片生成颜色值
image_colors = ImageColorGenerator(bg_pic)
plt.figure()
plt.imshow(wordcloud)
plt.axis('off')
plt.show()
# 保存图片
wordcloud.to_file( "chuizi.png")