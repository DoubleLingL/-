#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Huang lingling
############################
############################
#分时段统计23142号网格的出去量（一个小时）
# 出去量往以下八个方向各有多少流量
#北 南 东 西 东北 东南 西南 西北
############################
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
import math
#一列251个
ROW = 245
#一行245个
COLUMN = 251
#网格号
grid=23142
#商
QUE=94
#余数
REM=112

#path='/media/hll/amuse/gy/0511grid/23142_0905_11/23142_0911.csv'
#path='/media/hll/amuse/gy/1218grid/23142_0912_18/23142_0918.csv'
path='/media/hll/amuse/gy/1925grid/23142_0919_25/23142_0919.csv'
datalist=[]
#每个时段的进入量，流出量以及流量
NorthFlow=[]#上  1
SouthFlow=[]#下  2
EastFlow=[]#右   3
WestFlow=[]#左   4
EastNorthFlow=[]#右上   5
EastSouthFlow=[]#右下   6
WestNorthFlow=[]#左上   7
WestSouthFlow=[]#左下   8
for i in range(0,24):
    NorthFlow.append(0)
    SouthFlow.append(0)
    EastFlow.append(0)
    WestFlow.append(0)
    EastNorthFlow.append(0)
    EastSouthFlow.append(0)
    WestNorthFlow.append(0)
    WestSouthFlow.append(0)

with open(path,'r') as f:
    lines=f.readlines()
    for line in lines:
        linearr=line.strip().split(',')
        datalist.append(linearr)

#获取轨迹记录时间所处时间段
def get_timeSeq(timestr):
    time1 = time.strptime(timestr, '%Y-%m-%d %H:%M:%S')
    tmHour = time1.tm_hour
    return tmHour
def getQueRem(grid,Row):
    que=int(grid)/ROW
    rem=int(grid%ROW)
    return que,rem

for i in range(1,len(datalist)-1):
    if datalist[i][1] == datalist[i+1][1]:
        if datalist[i][6] == '23142.0' and datalist[i+1][6] != '23142.0':
            grid=float(datalist[i+1][6])
            print('grid:',grid)
            que,rem=getQueRem(grid,ROW)
            print('que,rem',que,rem)
            tmHour = get_timeSeq(datalist[i][0])
            print('tmHour',tmHour)
            if que == QUE:
                if 0 < rem < REM:
                    print('4')
                    WestFlow[tmHour] += 1
                else:
                    print('3')
                    EastFlow[tmHour] += 1
            elif que == QUE + 1 and rem == 0:
                print('3')
                EastFlow[tmHour] += 1
            if rem == REM:
                if que > QUE:
                    print('1')
                    NorthFlow[tmHour] += 1
                else:
                    print('2')
                    SouthFlow[tmHour] += 1
            if que > QUE:
                if rem > REM or rem == 0:
                    print('5')
                    EastNorthFlow[tmHour] += 1
                elif rem < REM:
                    print('7')
                    WestNorthFlow[tmHour] += 1
            if que < QUE:
                if rem > REM or rem == 0:
                    print('6')
                    EastSouthFlow[tmHour] += 1
                elif rem<REM:
                    print('8')
                    WestSouthFlow[tmHour] += 1
            if que == QUE and rem == 0:
                print('6')
                EastSouthFlow[tmHour] += 1
print('NorthFlow:',NorthFlow)
print('SouthFlow:',SouthFlow)
print('EastFlow:',EastFlow)
print('WestFlow:',WestFlow)
print('EastNorthFlow:',EastNorthFlow)
print('EastSouthFlow:',EastSouthFlow)
print('WestNorthFlow:',WestNorthFlow)
print('WestSouthFlow:',WestSouthFlow)


seqGrid={'NorthFlow':NorthFlow,'SouthFlow':SouthFlow,'EastFlow':EastFlow,
            'WestFlow':WestFlow,'EastNorthFlow':EastNorthFlow,'EastSouthFlow':EastSouthFlow,
            'WestNorthFlow':WestNorthFlow,'WestSouthFlow':WestSouthFlow}

seqGridframe=pd.DataFrame(seqGrid,columns=['NorthFlow','SouthFlow','EastFlow','WestFlow',
                                           'EastNorthFlow','EastSouthFlow','WestNorthFlow','WestSouthFlow'])
#seqGridframe['Col_sum']=seqGridframe.apply(lambda x: x.sum(),axis=1)
seqGridframe.loc['Row_sum']=seqGridframe.apply(lambda x: x.sum())
print(seqGridframe.head(25))

#seqGridframe.to_csv('/media/hll/amuse/gy/0511grid/23142_0905_11/direcflow/0911direcflow.csv',index=False)
#seqGridframe.to_csv('/media/hll/amuse/gy/1218grid/23142_0912_18/direcflow/0918direcflow.csv',index=False)
#seqGridframe.to_csv('/media/hll/amuse/gy/1925grid/23142_0919_25/direcflow/0925direcflow.csv',index=False)
seqGridframe.loc['Row_sum'].to_csv('/media/hll/amuse/gy/1925grid/23142_0919_25/direcflow/0919direcflow_row.csv',index=False)
