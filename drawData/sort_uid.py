#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Huang lingling
import pandas as pd
from pandas import *
import numpy as np
from numpy import *
import os

##########################################
#2016.09.05-09.25共21天数据
#将所有数据根据用户轨迹数据以及
# 经过23142的用户uid数据进行升序排序，
# 方便更快的提取经过23142网格的用户数据
# 2018.04.30
##########################################
#0905...0925数据排序前的路径
Path_1='/media/hll/amuse/gy/1925grid/0925/0925all.csv'
#经过23142网格的所有用户id排序前的的路径
path_2=r'/media/hll/amuse/gy/1925grid/uid0919_25/0925uid.csv'
frame_1=pd.read_csv(Path_1)#读取0905...0925数据排序前的路径文件
frame_2=pd.read_csv(path_2,header=None)#读取经过23142网格的所有用户id排序前文件
frame_2.columns=['uid']
print(frame_1.head())
print(len(frame_1))
print(frame_2.head())
print(len(frame_2))
framesort_1=frame_1.sort_values(axis=0,ascending=True,by=['uid','stime'])
framesort_2=frame_2.sort_values(axis=0,ascending=True,by='uid')

print(framesort_1.head(8))
print(len(framesort_1))
print(framesort_2.head(8))
print(len(framesort_2))
#经过23142网格的所有用户id排序后的的路径
#uidPath='/media/hll/amuse/gy/0511grid/uid0905_11/0905uid_sort.csv'
#dataPath='/media/hll/amuse/gy/0511grid/0905/0905all_sort.csv'
framesort_1.to_csv('/media/hll/amuse/gy/1925grid/0925/0925all_sort.csv',index=False)
framesort_2.to_csv('/media/hll/amuse/gy/1925grid/uid0919_25/0925uid_sort.csv',header=None,index=False)
