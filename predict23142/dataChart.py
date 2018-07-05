#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Huang lingling

from pandas import read_csv
from matplotlib import pyplot

#load dataset
path='/media/hll/amuse/gy/predict23142/flow/flow_1.csv'
#path='/media/hll/amuse/gy/predict23142/flow48/inflow0525.csv'
dataset=read_csv(path,header=0,index_col=0)
print(dataset)
values=dataset.values
#作数据分析，除了风向

groups=[0,1,2,3,4,5,6,7,8,9,10]
i=1
#plot each column
pyplot.figure()
for group in groups:
    pyplot.subplot(len(groups),1,i)
    pyplot.plot(values[:,group])
    pyplot.title(dataset.columns[group],y=0.5,loc='right')
    i+=1
pyplot .show()

