#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Huang lingling
#######################
#从文件000000_0.csv,000001_0.csv.....提取每天数据出来

import pandas as pd
import numpy as np
from pandas import read_csv
from datetime import datetime

#load data

dataset=read_csv('/media/hll/amuse/gy/1925/000006_0.csv')
#dataset=read_csv('data0511.csv',header=None)#不把第一行当作属性
print(dataset.head())
#column names
dataset.columns=['uid','starttime','endtime','latitude','longitude','state']
print(dataset.head())
#将数据类型转换为日期类型
dataset['starttime']=pd.to_datetime(dataset['starttime'])
#以starttime为索引
dataset=dataset.set_index('starttime')

#提取2016-09-05的数据
dataset=dataset['2016-09-25']
#print(dataset.head(5))
#将数据写入csv文件
dataset.to_csv('/media/hll/doc/1925/0925/0925_6.csv')
