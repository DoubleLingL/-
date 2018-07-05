#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''使用本机ubantu中配置的python2.7环境'''
__author__ = 'huanglingling'
'''update'''
__date__='2018.06.26'
'''循环遍历文件夹下的文件并处理'''
#用户轨迹点映射到网格
#所有数据映射到主城区的网格，不在主城区的轨迹点网格映射为0
#

import csv as csv
import numpy as np
import pandas as pd
import math
import varGlobal
from pandas import *
from numpy import *
import os

class Record(object):
    def __init__(self, lng,lat):
        #self.lng = lng
        #self.lat = lat
        self.lng = float(lng)
        self.lat = float(lat)

class Grid(object):
    def __init__(self, uid,stime,etime,lat,lng,stated, gid):

        self.uid = uid
        self.stime = stime
        self.etime = etime
        self.lat=lat
        self.lng=lng
        self.stated = stated
        self.gid = gid

def grid2dict(obj):
    return {
        'uid': obj.uid,
        'stime': obj.stime,
        'etime': obj.etime,
        'stated': obj.stated,
        'gid': obj.gid,
    }

#读取文件数据
def readIn(path):
    with open(path,'r') as f:
        l=f.readlines()
        data = list(map(lambda x: Record(*x.strip().split(',')), l))
    return data

def getGIDBylnglat(lng,lat):
    lng = float(lng)
    lat = float(lat)
    if (varGlobal.MINLAT < lat < varGlobal.MAXLAT) and (varGlobal.MINLNG < lng < varGlobal.MAXLNG):
        x = int((lat - varGlobal.MINLAT) / varGlobal.SIZELAT)
        y = int((lng - varGlobal.MINLNG) / varGlobal.SIZELNG)
        return x * varGlobal.COUNTLNG + y + 1
    else:
        return 0

def writetocsv(data):
    points=[(r.lng,r.lat) for r in data]
    grid = [getGIDBylnglat(x[0], x[1]) for x in points]
    print(grid[:5])
    return grid


def test(path,filename):
    dt = pd.read_csv(path)
    print(dt.head())
    dt.columns = ['stime', 'uid','etime','lat','lng','stated']
    print(dt.shape)
    print(dt.head())
    lnglat=dt[['lng','lat']]
    lnglat.to_csv('/media/hll/doc/1218/lnglattestdata.csv',index=False,header=None)
    #/media/hll/doc/0511/0905/lnglattestdata.csv
    data = readIn('/media/hll/doc/1218/lnglattestdata.csv')
    grid=writetocsv(data)
    datagrid = {'grid': grid}
    gridframe = pd.DataFrame(datagrid, columns=['grid'])
    print(gridframe.shape)
    #print(gridframe.head())
    #合并两个dataframe并写入csv
    frames=[dt,gridframe]
    results=pd.concat(frames,axis=1)
    print(results.head())
    #不将索引写入文件中
    results.to_csv('/media/hll/amuse/gy/MapData/0925/'+filename,index=False)

#/media/hll/amuse/gy/
rootdir = '/media/hll/doc/1925/0925'
list_1 = os.listdir(rootdir) #列出文件夹下所有的目录与文件
print(list_1)
for i in range(0,len(list_1)):
    path = os.path.join(rootdir,list_1[i])
    filename=os.path.basename(path)
    print(path)
    print(filename)
    if os.path.isfile(path):
        test(path,filename)


#if __name__=="__main__" : test()

