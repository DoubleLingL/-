#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Huang lingling
import pandas as pd
from pandas import *
import numpy as np
from numpy import *
import os
import xlrd
import csv
import time
import sys

##########################################
#2016.09.05-09.25
#提取经过网格23142，的用户数据
#### 更快抽取数据版本####
##########################################
#0905...0925数据的路径   排序后
dataPath='/media/hll/amuse/gy/0511grid/0905/0905all_sort.csv'
#经过23142网格的所有用户id的路径   排序后
uidPath='/media/hll/amuse/gy/0511grid/uid0905_11/0905uid_sort.csv'

'''
dataset=pd.read_csv(dataPath)
#dataset=dataset.set_index('uid')

#uidset=pd.read_csv(uidPath)
#uidset.columns=['uid']
print(dataset.head())

uidset=[]
with open(uidPath,'r') as f:
    lines=f.readlines()
    for line in lines:
        linearr=line.strip()
        uidset.append(linearr)
print(uidset[:5])


userdata=dataset[dataset['uid'].isin(uidset)]
print(len(userdata))
print(userdata.head(10))

userdata.to_csv('/media/hll/amuse/gy/0511grid/23142_0905_11/23142_0905.csv',index=False)
'''
#
'''
id_index=0
id_match_index=0

for id_index_value in open(uidPath):
    for id_match_index in open(dataPath):

    id_index+=1
'''

start_time = time.clock()


#0905...0925数据的路径   排序后
id_data_file='/media/hll/amuse/gy/0511grid/0905/0905all_sort.csv'
#经过23142网格的所有用户id的路径   排序后
id_file='/media/hll/amuse/gy/0511grid/uid0905_11/0905uid_sort.csv'

id_total_line=0
with open(id_file) as id_f:
    id_f_reader = csv.reader(id_f)
    for temp in id_f:
        id_total_line+=1
print("id total line num is",id_total_line)

id_data_total_line=0
with open(id_data_file) as id_data_f:
    id_data_f_reader = csv.reader(id_data_f)
    for temp in id_data_f:
        id_data_total_line+=1
print("id data total line num is",id_data_total_line)

match_line_num=0
mismatch_line_num=0
id_index=0
last_match=0
with open(id_file) as id_f:
    id_f_reader = csv.reader(id_f)
    id_data_f = open(id_data_file,"r")
    id_data_f_reader = csv.reader(id_data_f)
    for id_f_row in id_f_reader:
        for id_data_f_row in id_data_f_reader:
            if((id_f_row[0] != id_data_f_row[1]) and (last_match == 1)):
                #row_len=sys.getsizeof(id_data_f_row)
                #print('row_len',row_len)
                #id_data_f.seek(-row_len,1)
                last_match = 0
                break
            if(id_f_row[0] == id_data_f_row[1]):
                #if(id_data_f_reader.line_num < 100000):
                #    print("id is", id_f_row[0], "id data id is", id_data_f_row[1], id_data_f_reader.line_num)
                #print("id is", id_f_row[0], "id data id is", id_data_f_row[1], id_data_f_reader.line_num)
                last_match = 1
                match_line_num += 1
            else:
                last_match = 0
                match_line_num = match_line_num

print("\nthe id match line num is:",match_line_num)
end_time = time.clock()
print("running time is:%s seconds"%(end_time-start_time))
