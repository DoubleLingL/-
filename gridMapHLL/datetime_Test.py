#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Huang lingling
import time
def trans_format(time_string, from_format, to_format='%Y-%m-%d %H:%M:%S'):
    time_struct = time.strptime(time_string, from_format)
    print(time_struct)
    times = time.strftime(to_format, time_struct)
    return times

#将11 May转为mm-dd形式
#time_string = "11 May"
#times = trans_format(time_string, '%d %b', '%m-%d')

time_string = "2016 09 05 20 23 56"
times = trans_format(time_string, '%Y %m %d %H %M %S')    #由于没有输入年份，所以输出的默认年份是1900
print(times)

