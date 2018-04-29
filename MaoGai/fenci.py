# -*- coding: utf-8 -*-
import jieba
import codecs
from scipy.misc import imread
import os
from os import path
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
from wordcloud import WordCloud, ImageColorGenerator
from pyecharts import Bar
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import drawBar


def readDocument():
    '''
    获取文档对象
    '''
    comment_text = codecs.open('/home/dmrf/文档/毛概/19大报告.txt', 'r', 'utf-8').read()
    # 结巴分词，生成字符串，如果不通过分词，无法直接生成正确的中文词云

    cut_text = " ".join(jieba.cut(comment_text))
    return cut_text

def segment(doc):
    '''
    用jieba分词对输入文档进行分词，并保存至本地（根据情况可跳过）
    '''
    seg_list = " ".join(jieba.cut(doc, cut_all=False)) #seg_list为str类型

    document_after_segment = open('/home/dmrf/文档/毛概/分词结果.txt', 'w+')
    document_after_segment.write(seg_list)
    document_after_segment.close()

    return seg_list


def wordCount(segment_list):
    '''
        该函数实现词频的统计，并将统计结果存储至本地。
        在制作词云的过程中用不到，主要是在画词频统计图时用到。
    '''
    word_lst = []
    word_dict = {}
    with open('/home/dmrf/文档/毛概/词频统计(去停用词).txt','w') as wf2:
        word_lst.append(segment_list.split(' '))
        for item in word_lst:
            for item2 in item:
                if item2 not in word_dict:
                    word_dict[item2] = 1
                else:
                    word_dict[item2] += 1

        word_dict_sorted = dict(sorted(word_dict.items(),
        key = lambda item:item[1], reverse=True))#按照词频从大到小排序
        for key in word_dict_sorted:
            wf2.write(key+' '+str(word_dict_sorted[key])+'\n')
    wf2.close()

def drawWordCloud(seg_list):
    '''
        制作词云
        设置词云参数
    '''
    color_mask = imread("../Pic/map.png") # 读取背景图片,注意路径
    wc = WordCloud(
        #设置字体，不指定就会出现乱码，注意字体路径
        font_path="../Font/SourceHanSansSC-Heavy.otf",
        #font_path=path.join(d,'simsun.ttc'),
        #设置背景色
        background_color='white',
        #词云形状
        mask=color_mask,
        #允许最大词汇
        max_words=2000,
        #最大号字体
        max_font_size=60
    )
    wc.generate(seg_list) # 产生词云
    image_colors = ImageColorGenerator(color_mask)
    wc.to_file("ciyun2.jpg") #保存图片
    #  显示词云图片
    plt.imshow(wc, interpolation="bilinear")
    plt.axis('off')

    #这里主要为了实现词云图片按照图片颜色取色
    plt.figure()
    plt.imshow(wc.recolor(color_func=image_colors), interpolation="bilinear")
    plt.axis("off")

    plt.show()

def removeStopWords(seg_list):
    '''
    自行下载stopwords1893.txt停用词表，该函数实现去停用词
    '''
    wordlist_stopwords_removed = []

    stop_words = open('/home/dmrf/文档/python/1893停用词表.txt')
    stop_words_text = stop_words.read()

    stop_words.close()

    stop_words_text_list = stop_words_text.split('\n')
    after_seg_text_list = seg_list.split(' ')

    for word in after_seg_text_list:
        if word not in stop_words_text_list:
            wordlist_stopwords_removed.append(word)

    without_stopwords = open('/home/dmrf/文档/毛概/分词结果(去停用词).txt', 'w')
    without_stopwords.write(' '.join(wordlist_stopwords_removed))
    return ' '.join(wordlist_stopwords_removed)


if __name__ == "__main__":
    doc = readDocument()
    segment_list = segment(doc)
    segment_list_remove_stopwords = removeStopWords(segment_list)
    drawWordCloud(segment_list_remove_stopwords)
    wordCount(segment_list_remove_stopwords)
    drawBar.drawStatBarh()