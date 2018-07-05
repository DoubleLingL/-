#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Author:Huang lingling

'''
方向雷达图
'''
import pandas as pd
from pandas import Series,DataFrame
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from numpy import *
import math
import sys
reload(sys)
sys.setdefaultencoding('utf8')
#plt.rcParams['font.sans-serif'] = ['KaiTi'] #显示中文
#标签
labels=np.array(['East','  EastNor','North','WestNor ','West','WestSou ','South',' EastSou'])
#数据个数
dataLen = 8
#数据

data=np.array([603,7219,308,7052,1008,3392,487,2282])#0925
#data=np.array([1552,8659,640,9572,1184,4182,818,3201])#0919
angles=np.linspace(0,2*np.pi,dataLen,endpoint=False)
data=np.concatenate((data,[data[0]]))
angles=np.concatenate((angles,[angles[0]]))

fig=plt.figure()
print(plt.style.available)
plt.style.use('seaborn-paper')
ax=fig.add_subplot(111,polar=True)
ax.plot(angles,data,'go-',alpha=0.25,linewidth=3)
ax.fill(angles,data,facecolor='y',alpha=0.65)

ax.set_thetagrids(angles * 180/np.pi,labels)
ax.set_title('Direction Radar 20160925',va='bottom')
ax.set_ylim(0,10000)
ax.grid(True)
plt.show()