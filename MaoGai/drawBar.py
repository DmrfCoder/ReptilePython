# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from matplotlib.font_manager import *
import numpy as np
import codecs
import tablib
import sys
reload(sys)
from pyecharts import Bar

sys.setdefaultencoding('utf-8')

def drawStatBarh():
    '''
    画出词频统计条形图，用渐变颜色显示，选取前N个词频
    '''
    fig, ax = plt.subplots()
    myfont = FontProperties(fname='../Font/SourceHanSansSC-Heavy.otf')
    N = 20


    data=[]
    for line in codecs.open('/home/dmrf/文档/毛概/词频统计(去停用词).txt', "r"):
        line.strip('\n')
        c=line.split(' ')
        e=c[0]
        try:
            f=int(c[1])
        except IndexError:
            continue
        item={
            'words':e,
            'count':f
        }
        data.append(item)


    data.sort(reverse=True)
    words= [d['words'] for d in data]
    counts= [w['count'] for w in data]

    ds = tablib.Dataset()
    ds.headers = ['关键词', '出现次数']

    for i in range(1,N):
        ds.append([words[i], counts[i]])
    bar = Bar('词频分析')
    bar.add('出现次数', ds.get_col(0), ds.get_col(1))
    bar.render('19.html')

    y_pos = np.arange(N)

    colors = ['#FA8072'] #这里是为了实现条状的渐变效果，以该色号为基本色实现渐变效果
    for i in range(len(words[:N]) - 1):
        colors.append('#FA' + str(int(colors[-1][3:]) - 1))

    rects = ax.barh(y_pos, counts[:N], align='center', color=colors)

    ax.set_yticks(np.arange(N))
    ax.set_yticklabels(words[:N],fontproperties=myfont)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_title('十九大报告中的高频词汇',fontproperties=myfont, fontsize=17)
    ax.set_xlabel(u"出现次数",fontproperties=myfont)

    autolabel(rects, ax)
    plt.savefig('plt.png')
    plt.show()


def autolabel(rects, ax):
    """
    给条形图加上文字标签
    """
    #fig, ax = plt.subplots()
    for rect in rects:
        width = rect.get_width()
        ax.text(1.03 * width, rect.get_y() + rect.get_height()/2.,
            '%d' % int(width),ha='center', va='center')

drawStatBarh()