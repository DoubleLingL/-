#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Huang lingling

############################
#分时段统计进入量（一个小时）
# 备注： 统计进入量和出去量 有问题，把所有用户当成了一个用户来处理
############################
#修改以上提及的错误
############################
import pandas as pd
from pandas import *
import numpy as np
from numpy import *
from itertools import islice
import os
import xlrd
import csv
import time
import sys

#path='/media/hll/amuse/gy/0511grid/23142_0905_11/23142_0911.csv'
#path='/media/hll/amuse/gy/1218grid/23142_0912_18/23142_0918.csv'
path='/media/hll/amuse/gy/1925grid/23142_0919_25/23142_0925.csv'
datalist=[]
#每个时段的进入量，流出量以及流量
seqGridInFlow=[]
seqGridOutFlow=[]
seqGridFlow=[]
for i in range(0,48):
    seqGridInFlow.append(0)
    seqGridOutFlow.append(0)
    seqGridFlow.append(0)

print(seqGridInFlow)
print(seqGridOutFlow)
print(seqGridFlow)

with open(path,'r') as f:
    lines=f.readlines()
    for line in lines:
        linearr=line.strip().split(',')
        datalist.append(linearr)
print(datalist[:3])
print(datalist[1][0])
print(len(datalist))

#获取轨迹记录时间所处时间段
def get_timeSeq(timestr):
    time1 = time.strptime(timestr, '%Y-%m-%d %H:%M:%S')
    tmHour = time1.tm_hour
    tmMin=time1.tm_min
    tmSec=time1.tm_sec
    if tmMin>30 or tmMin==30 and tmSec>0:
        seq=tmHour*2+1
    else:
        seq=tmHour*2
    return seq

for i in range(1,len(datalist)):
    if datalist[i][1] == datalist[i-1][1]:
        if datalist[i][6]=='23142.0' and datalist[i-1][6]!='23142.0':
            seq=get_timeSeq(datalist[i][0])
            seqGridInFlow[seq]+=1
    if datalist[i][6] == '23142.0':
        seq = get_timeSeq(datalist[i][0])
        seqGridFlow[seq]+=1
for i in range(1,len(datalist)-1):
    if datalist[i][1] == datalist[i+1][1]:
        if datalist[i][6] == '23142.0' and datalist[i+1][6] != '23142.0':
            seq = get_timeSeq(datalist[i][0])
            seqGridOutFlow[seq]+=1
print('seqGridInFlow:',seqGridInFlow)
print('seqGridOutFlow:',seqGridOutFlow)
print('seqGridFlow:',seqGridFlow)
sum=0
for i in range(0,48):
    sum=sum+seqGridFlow[i]
print('sum ',sum)

seqGrid={'seqGridInFlow':seqGridInFlow,'seqGridOutFlow':seqGridOutFlow,'seqGridFlow':seqGridFlow}
seqGridframe=pd.DataFrame(seqGrid,columns=['seqGridInFlow','seqGridOutFlow','seqGridFlow'])
print(seqGridframe.head())
#seqGridframe.to_csv('/media/hll/amuse/gy/0511grid/23142_0905_11/23142flow48/0911flow.csv',index=False)
#seqGridframe.to_csv('/media/hll/amuse/gy/1218grid/23142_0912_18/23142flow48/0918flow.csv',index=False)
seqGridframe.to_csv('/media/hll/amuse/gy/1925grid/23142_0919_25/23142flow48/0925flow.csv',index=False)