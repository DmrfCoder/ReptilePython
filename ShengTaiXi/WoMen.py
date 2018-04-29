#-*-coding:utf-8-*-

import requests
import json
from pyecharts import Bar
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
from scipy.misc import imread



url = 'https://music.163.com/weapi/v1/resource/comments/R_SO_4_554931466?csrf_token='

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36',
    'Referer': 'https://music.163.com/#/song?id=554931466',
    'Origin': 'http://music.163.com',
    'Host': 'music.163.com'
}
# 加密数据，直接拿过来用
user_data = {
    'params': 'LRNiczTozzAnMy3D1xvDbgLmg9FVCIEHJ7zYZFUTa+pvU8O5waHO/hQ8of2TtOL0y41C43VGDrc5FyO8ujqv5Em9JeZ75xqcQYVtv7KTR5LWvqQL/vt1C6FhOk0kJL/Q/l8H8aywEfqUP/UMYlQjIzX8JWGYzqkASRaEA4ELMRkZOkUPFD8bky4bsTarwibb',
    'encSecKey': '8d3d117a2b3c66aa72756e74af3a27e2528395881d4d90c45a05df8ab6f7c2381d0d254c931097a0f0b29036632b6137a71ebac39ad4e91668f9d6a05442b6dc001ab57c6b880fd6e3222b6880d49ac03b8944c5130a51740c27dec4fb9e9ad33741a21dacb145818a97d6e4f0491a276bb2eea684b1b29e757eee3237bf04f8'
}

response = requests.post(url, headers=headers, data=user_data)

data = json.loads(response.text)
hotcomments = []
for hotcommment in data['hotComments']:
    item = {
        'nickname': hotcommment['user']['nickname'],
        'content': hotcommment['content'],
        'likedCount': hotcommment['likedCount']
    }
    hotcomments.append(item)

# 获取评论用户名，内容，以及对应的获赞数   
content_list = [content['content'] for content in hotcomments]
nickname = [content['nickname'] for content in hotcomments]
liked_count = [content['likedCount'] for content in hotcomments]

bar = Bar("热评中点赞数示例图")
bar.add( "点赞数",nickname, liked_count, is_stack=True,mark_line=["min", "max"],mark_point=["average"])
bar.render('shengtaixi.html')


#bg_pic = imread('../Pic/Chen1.png')
content_text = " ".join(content_list)
wordcloud = WordCloud(font_path='../Font/SourceHanSansSC-Heavy.otf',background_color='white',max_words=200,mode='RGBA').generate(content_text)

plt.figure()
plt.imshow(wordcloud,interpolation='bilinear')
plt.axis('off')
plt.show()
wordcloud.to_file( "shengtai.png")
