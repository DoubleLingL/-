#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__='Huanglingling'
'''update'''
__date__='2018.06.21'
import pandas as pd
from pandas import *
import numpy as np
from numpy import *
from itertools import islice
import varGlobal
import os
import xlrd
import csv
import time
import sys
import datetime
'''
数据日期分割
exp:
uid,2016-09-05 17:12:20,2016-09-06 12:27:57,lat,lng,stated,grid
--->
uid,2016-09-05 17:12:20,2016-09-05 23:59:59,lat,lng,stated,grid
uid,2016-09-06 00:00:00,2016-09-06 12:27:57,lat,lng,stated,grid
'''
def get_timeday(timestr):
    '''获取日期中的天 2016-09-05 17:12:20 ---> 5 具体查看time属性'''
    time1 = time.strptime(timestr, varGlobal.DATE_FORMAT)
    tmDay=time1.tm_mday
    print(tmDay)
    return tmDay

def gettimedetal(stime,etime):
    '''获取天差值，以便判断是否跨天'''
    detal=get_timeday(etime)-get_timeday(stime)
    return detal

def trans_format(time_string, from_format, to_format=varGlobal.DATE_FORMAT):
    time_struct = time.strptime(time_string, from_format)
    print(time_struct)
    times = time.strftime(to_format, time_struct)
    return times

def gettime(xtime,x):
    xtime = time.strptime(xtime, varGlobal.DATE_FORMAT)
    if x==1:
        time_string= str(xtime.tm_year) + ' ' + str(xtime.tm_mon) + ' ' + \
                     str(xtime.tm_mday) + ' ' + '23' + ' ' + '59' + ' ' + '59'
    else:
        time_string = str(xtime.tm_year) + ' ' + str(xtime.tm_mon) + ' ' + \
                     str(xtime.tm_mday) + ' ' + '00' + ' ' + '00' + ' ' + '00'
    times = trans_format(time_string, '%Y %m %d %H %M %S')
    return times

def test():
    path='/home/hll/PycharmProjects/gridMapHLL/gridData/gridtestdata_1_2.csv'
    #path='/home/hll/PycharmProjects/gridMapHLL/gridData/mainUbanData.csv'
    df=pd.read_csv(path)
    for indexs in df.index:
        print(indexs)
        data=df.loc[indexs]
        etime = df.loc[indexs,'etime']
        stime = df.loc[indexs, 'stime']
        print(etime,stime)
        detal = gettimedetal(stime,etime)
        print('detal:',detal)
        if detal==1:#暂时不考虑跨越一天以上的数据
            times1 = gettime(stime,1)
            times2 = gettime(etime,2)
            print(times1)
            print(times2)
            df.loc[indexs, 'etime'] = times1
            '''注意 双方括号 [[]]'''
            insertRow = pd.DataFrame([[data.uid,times2,etime,data.lat,data.lng,data.stated,data.grid]],
                                 columns=['uid','stime','etime','lat','lng','stated','grid'])
            above=df.loc[:indexs]
            below=df.loc[(indexs+1):]
            df=above.append(insertRow,ignore_index=True).append(below,ignore_index=True)
            print(df.loc[indexs])
            print(df.loc[indexs+1])
    df.to_csv('/home/hll/PycharmProjects/gridMapHLL/gridData/mainUbanData_split_1_2.csv',index=False)


if __name__=='__main__':
    test()