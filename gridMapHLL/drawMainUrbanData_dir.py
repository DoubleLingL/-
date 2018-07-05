#!usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'huanglingling'
__date__='2018.06.22'
'''提取主城区数据'''
'''update'''
__date__='2018.06.26'
'''循环遍历文件夹下的文件并处理'''

import csv as csv
import numpy as np
import pandas as pd
import math
from pandas import *
from numpy import *
import os

def test(path,filename):
    df=pd.read_csv(path)
    print(df[:5])
    #index 不在主城区的行
    indexs = list(df[df['grid']==0].index)
    #获取不在主城区的用户ID并去重
    df2=df['uid'].loc[indexs].drop_duplicates()
    #获取不在主城区用户的位置（所在行）
    userindexs=df[df['uid'].isin(df2)].index
    print('userdata:',userindexs)
    #删除不在主城区的用户数据
    df3=df.drop(userindexs)
    print(df3.head(10))
    df3.to_csv('/media/hll/amuse/gy/UrbanData1925/0925/'+filename,index=False)
#/media/hll/amuse/gy/MapData/0919/
rootdir = '/media/hll/amuse/gy/MapData/0925/'
list_1 = os.listdir(rootdir) #列出文件夹下所有的目录与文件
print(list_1)
for i in range(0,len(list_1)):
    path = os.path.join(rootdir,list_1[i])
    filename=os.path.basename(path)
    print(path)
    print(filename)
    if os.path.isfile(path):
        test(path,filename)
