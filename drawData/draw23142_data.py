#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Huang lingling
import pandas as pd
from pandas import *
import numpy as np
from numpy import *
import os
import time
##########################################
#2016.09.05-09.25
#提取经过网格23142，的用户数据
##########################################
#0905...0925数据的路径   排序后
dataPath='/media/hll/amuse/gy/1925grid/0925/0925all_sort.csv'
#经过23142网格的所有用户id的路径   排序后
uidPath='/media/hll/amuse/gy/1925grid/uid0919_25/0925uid_sort.csv'

start_time = time.clock()

dataset=pd.read_csv(dataPath)
print(dataset.head())

uidset=[]
with open(uidPath,'r') as f:
    lines=f.readlines()
    for line in lines:
        linearr=line.strip()
        uidset.append(linearr)
print(uidset[:5])
#userdata为dataset中uid的行索引
userdata=dataset[dataset['uid'].isin(uidset)]
print(len(userdata))
print(userdata.head(10))

userdata.to_csv('/media/hll/amuse/gy/1925grid/23142_0919_25/23142_0925.csv',index=False)
end_time = time.clock()
print("running time is:%s seconds"%(end_time-start_time))