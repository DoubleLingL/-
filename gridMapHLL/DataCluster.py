#!urs/bin/env python3
#-*- coding:utf-8 -*-
__author__='huanglingling'
'''update'''
__date__='2018.06.22'
'''
对每个用户的夜间数据进行聚类，即0-6点间的数据进行聚类
'''
import numpy as np
import  pandas as pd
from pandas import *
from numpy import *
import varGlobal
import time
from datetime import datetime
from geopy.distance import great_circle
from geopy.distance import vincenty
from DataSplit import *
from myMap import getGIDBylnglat

def get_timehour(timestr):
    '''获取日期中的时 2016-09-05 17:12:20 ---> 17 具体查看time属性'''
    time1 = time.strptime(timestr, varGlobal.DATE_FORMAT)
    tmHour=time1.tm_hour
    print(tmHour)
    return tmHour
def distance(point1,point2):
    return vincenty(point1,point2).m

def gettimedetalInS(etime,stime):
    etimedt = datetime.datetime.strptime(etime,'%Y-%m-%d %H:%M:%S')
    stimedt = datetime.datetime.strptime(stime, '%Y-%m-%d %H:%M:%S')
    return (etimedt-stimedt).seconds

def newpointdata(indexpoint,end_point,lat,lng):
    newpoint=[]
    print('length_endpoint-->',len(end_point))
    newpointuid=indexpoint.uid
    newpoint.append(newpointuid)
    newpointstime = end_point[0].stime
    newpoint.append(newpointstime)
    newpointetime = end_point[-1].etime
    newpoint.append(newpointetime)
    newpointlat=lat/(len(end_point))
    newpoint.append(newpointlat)
    newpointlng = lng / len(end_point)
    newpoint.append(newpointlng)
    newpointstated= 1 if gettimedetalInS(indexpoint.etime,indexpoint.stime)>varGlobal.STAYTIME else 0
    newpoint.append(newpointstated)
    newpointgrid= getGIDBylnglat(newpointlng,newpointlat)
    newpoint.append(newpointgrid)
    print('newpoint-->:',newpoint)
    return newpoint

def getL(recordindex):
    L=len(recordIndex)
    return L

path='/home/hll/PycharmProjects/gridMapHLL/gridData/mainUbanData_split_1_2.csv'
df=pd.read_csv(path)
begin_point,end_point,recordIndex=[],[],[]
lat,lng=0,0
for index in df.index:
    print('index-->',index)
    print('len_end_point:', len(end_point))
    nowtimeHour=get_timehour(df.loc[index,'stime'])
    if nowtimeHour <= varGlobal.CLUSTERTIME:
        is_close=True
        if begin_point==[]:
            begin_point,lat,lng=df.loc[index],df.loc[index,'lat'],df.loc[index,'lng']
            print('begin_point:', begin_point)
            end_point.append(begin_point)
            print('end_point:',end_point)
            #continue
        print('begin_point:', begin_point)
        point2 = (df.loc[index, 'lat'], df.loc[index, 'lng'])
        print('point2:', point2)
        point1=(begin_point.lat,begin_point.lng)
        print('point1:', point1)
            #print('distance(point1,point2)-->',distance(point1,point2))
        if distance(point1,point2) > varGlobal.CLUSTERDISTANCE:
            is_close=False
        if is_close:
            print('processing')
            end_point.append(df.loc[index])
            lat += df.loc[index,'lat']
            lng += df.loc[index,'lng']
            recordIndex.append(index)
            print('end_point:', end_point)
            print('recordIndex:', recordIndex)
        if not is_close:
            p=newpointdata(df.loc[index-1],end_point,lat,lng)
            newpoint=pd.DataFrame([[p[0],p[1],p[2],p[3],p[4],p[5],p[6]]],
                                  columns=['uid','stime','etime','lat','lng','stated','grid'])
            df.drop(recordIndex,inplace=True)
            L=len(recordIndex)
            print('L-->',L)
            above=df.loc[:(index-L-1)]
            below=df.loc[index-1:]
            df=above.append(newpoint,ignore_index=True).append(below,ignore_index=True)
            begin_point, lat, lng = df.loc[index], df.loc[index, 'lat'], df.loc[index, 'lng']
            end_point=[]
            end_point.append(begin_point)
    elif len(end_point)>0 :
        #if len(end_point)>0:
        print('end_point-->',end_point)
        print('lat-->', lat)
        print('lng-->', lng)
        p = newpointdata(df.loc[index], end_point, lat, lng)
        newpoint = pd.DataFrame([[p[0],p[1],p[2],p[3],p[4],p[5],p[6]]],
                                 columns=['uid', 'stime', 'etime', 'lat', 'lng', 'stated', 'grid'])
        df.drop(recordIndex, inplace=True)
        L = len(recordIndex)
        above = df.loc[:(index - L - 1)]
        below = df.loc[index - 1:]
        df = above.append(newpoint, ignore_index=True).append(below, ignore_index=True)
        #index = index - L + 1
        end_point=[]
    #begin_point, lat, lng = df.loc[index], df.loc[index, 'lat'], df.loc[index, 'lng']
        #end_point = []
        #recordIndex = []
        #index = index - L + 1
    #begin_point, end_point, recordIndex = None, [], []
    #lat, lng = 0, 0

df.to_csv('/home/hll/PycharmProjects/gridMapHLL/gridData/mainUbanData_split_1_2_cluster.csv',index=False)

# index=index-L+1
# begin_point, lat, lng = df.loc[index], df.loc[index, 'lat'], df.loc[index, 'lng']
# end_point=[]
# recordIndex=[]
# end_point.append(begin_point)
# index = index - L + 1
# begin_point, end_point, recordIndex = None, [], []
# lat, lng = 0, 0
