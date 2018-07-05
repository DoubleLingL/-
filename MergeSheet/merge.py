#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#################
#使用python2.7环境
#################
#合并多个csv文件
#################
__author__ = 'huanglingling'

import pandas as pd
from pandas import *
import os

'''
Folder_path='/home/hll/123'
SaveFileName=r'all.csv'
df1=pd.read_csv('/home/hll/123/1.csv')
print(df1.head())
df2=pd.read_csv('/home/hll/123/2.csv')
print(df2.head())
df3=pd.read_csv('/home/hll/123/3.csv')
print(df3.head())
frames=[df1,df2,df3]
result=pd.concat(frames)
result.to_csv('/home/hll/123/all.csv',index=False)
'''
#path='/media/hll/amuse/gy/1925grid/23142_0919_25/direcflow'
#path='/media/hll/amuse/gy/1218grid/23142_0912_18/direcflow'
#path='/media/hll/amuse/gy/0511grid/23142_0905_11/direcflow'
#path='/media/hll/amuse/gy/predict23142/direcflow'
path='/media/hll/amuse/gy/predict23142/flow48'
filepath=os.listdir(path)
print(filepath)
frames=[]
for file in filepath:
    domain=os.path.abspath(path)
    file=os.path.join(domain,file)
    filedf=pd.read_csv(file)
    frames.append(filedf)
result=pd.concat(frames)
#result.to_csv('/media/hll/amuse/gy/1925grid/23142_0919_25/direcflow/direcflow.csv',index=False)
#result.to_csv('/media/hll/amuse/gy/1218grid/23142_0912_18/direcflow/direcflow.csv',index=False)
#result.to_csv('/media/hll/amuse/gy/0511grid/23142_0905_11/direcflow/direcflow.csv',index=False)
result.to_csv('/media/hll/amuse/gy/predict23142/flow48/flow0525.csv',index=False)