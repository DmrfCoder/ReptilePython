# -*-coding:utf-8-*-
import codecs
from collections import Counter
# 读入一个txt文件
import jieba as jieba
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
from scipy.misc import imread

rem = [u'，', u'、', u'。', u'的', u'和', '\u3000', '\n']

comment_text = codecs.open('/home/dmrf/文档/毛概/19大报告.txt', 'r','utf-8').read()
# 结巴分词，生成字符串，如果不通过分词，无法直接生成正确的中文词云

cut_text = " ".join(jieba.cut(comment_text))


bg_pic = imread('../Pic/gongchandang.png')
wordcloud = WordCloud(mask=bg_pic, font_path='../Font/SourceHanSansSC-Heavy.otf', background_color='white',
                      max_words=200, mode='RGBA').generate(cut_text)
d=wordcloud.words_
print(d)
# 从背景图片生成颜色值
image_colors = ImageColorGenerator(bg_pic)
plt.figure()
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
wordcloud.to_file("19da.png")
