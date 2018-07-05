#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Huang lingling
import pandas as pd
from pandas import *
import numpy as np
from numpy import *
import os

'''
path='/media/hll/amuse/gy/0511grid/0905/0905_6.csv'
df=pd.read_csv(path)
print(df.head())
print(len(df))

df1=df[df.grid==23142]
print(df1.head(15))
print(len(df1))

dropdf=df1.drop_duplicates(subset=['uid'],keep='first')
print(dropdf.head(10))
print(len(dropdf))

uiddf=dropdf.uid
uiddf.to_csv('/media/hll/amuse/gy/0511grid/uid0905/0905uid.csv',index=False)
print(uiddf.head())
print(len(uiddf))
'''
##########################################
#2016.09.05-09.25
#批量统计经过网格23142，每天的用户数量,用户id数据及轨迹条数
##########################################
#读取的文件夹路径

path=r'/media/hll/amuse/gy/0511grid/0905'
#读取文件夹下的文件为列表
filepath=os.listdir(path)
print(filepath)
#计数：总用户数量和总轨迹数量
usercount=0
trjcount=0
for file in filepath:
    domain=os.path.abspath(path)
    file=os.path.join(domain,file)#每个文件完整路径
    filedf=pd.read_csv(file)#读取文件
    #print(filedf.head())
    print(len(filedf))
    df1 = filedf[filedf.grid == 23142]
    #print(df1.head(15))
    print(len(df1))
    trjcount=trjcount+len(df1)
    dropdf = df1.drop_duplicates(subset=['uid'], keep='first')
    #print(dropdf.head(10))

    usercount=usercount+len(dropdf)

    uiddf = dropdf.uid
    uiddf.to_csv('/media/hll/amuse/gy/0511grid/uid0905_11/0905uid.csv', mode='a+',index=False)
    #print(uiddf.head())
    print(len(uiddf))
print(usercount)
print(trjcount)

















