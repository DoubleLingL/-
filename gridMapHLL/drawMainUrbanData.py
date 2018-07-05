#!usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'huanglingling'

'''提取主城区数据'''

import csv as csv
import numpy as np
import pandas as pd
import math
from pandas import *
from numpy import *
import os

#path='/media/hll/doc/0511/0905/0905grid_6.csv'
path='/home/hll/PycharmProjects/gridMapHLL/gridData/gridtestdata2.csv'
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
df3.to_csv('/home/hll/PycharmProjects/gridMapHLL/gridData/gridtestdata2_urban.csv',index=False)