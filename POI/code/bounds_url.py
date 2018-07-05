#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__='huanglingling'

'''功能：
获取bounds列表
获取url列表
以便后续POI爬取
'''
from code import varglobal

def getBorderByGridId(gridid):
    row = int(gridid)//varglobal.COUNTLNG # 返回整数部分　　　行号
    column = int(gridid) - row * varglobal.COUNTLNG     #  列号
    if column == 0:
        column = varglobal.COUNTLNG
        row = row - 1
    lat1 = float('%.8f' % (varglobal.MINLAT + row * varglobal.SIZELAT))
    lat2= float('%.8f' % (varglobal.MINLAT + (row + 1) * varglobal.SIZELAT))
    lng1 = float('%.7f' % (varglobal.MINLNG + (column - 1) * varglobal.SIZELNG))
    lng2 = float('%.7f' % (varglobal.MINLNG + column * varglobal.SIZELNG))
    return lat1, lat2, lng1, lng2

def geturl():
    #l = []
    l_1=[]
    urls=[]
    for i in range(1,varglobal.COUNTCELL+1):
        r = getBorderByGridId(i)
        #newgrid = [i,r[0], r[1], r[2], r[3]]
        newgrid1 = [r[0], r[1], r[2], r[3]]
        l_1.append(newgrid1)
        #l.append(newgrid1)
        print(str(r[0])+','+str(r[2])+','+str(r[1])+','+str(r[3]))
        for i in range(0,varglobal.page_nums):
            page_num=str(i)
            url="http://api.map.baidu.com/place/v2/search?query=中学& bounds="+str(r[0])+','+str(r[2])+','+str(r[1])+','+str(r[3])+"&page_size=20&page_num="+str(page_num)+"&output=json&ak=ZWMBHwbcv14HiW8PMnTqFnVFc8bfGHqx"
            #print('url',url)
            urls.append(url)
    print('urls', urls)
    return urls



if __name__=="__main__":
    geturl()
