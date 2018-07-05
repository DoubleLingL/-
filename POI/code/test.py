#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__='huanglingling'
'''
功能：POI爬取
统计网格各类POI的数目，方便定义网格所属POI主题
    宿舍、住宅区：住
    公司企业、学校：职
    美食：吃
    购物：购物
    休闲娱乐、景区：娱乐
    政府机构：政府机构
    其他：其他
 '''
import urllib3
import json
import requests
import sys #导入标准库。可能是防止乱码
from code import varglobal
import pandas as pd
import csv
import math
ty=sys.getfilesystemencoding()  #这个可以获取文件系统的编码形式

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

def geturl(keyword):
    #l = []
    l_1=[]
    urls=[]
    for i in range(1,varglobal.COUNTCELL+1):
        r = getBorderByGridId(i)
        newgrid1 = [r[0], r[1], r[2], r[3]]
        l_1.append(newgrid1)
        print(str(r[0])+','+str(r[2])+','+str(r[1])+','+str(r[3]))
        url="http://api.map.baidu.com/place/v2/search?query="+keyword+"& bounds="+str(r[0])+','+str(r[2])+','+str(r[1])+','+str(r[3])+"&page_size=20&output=json&ak=ZWMBHwbcv14HiW8PMnTqFnVFc8bfGHqx"
        urls.append(url)
    print('urls', urls)
    return urls

def getPOI(urls):
    restaurant=[]
    count=0
    for url in urls:
        html = requests.get(url)  # 获取网页信息
        data = html.json()  # 获取网页信息的json格式数据
        #path = '/home/hll/PycharmProjects/POI/data/POIInfo_office.csv'
        path = '/home/hll/PycharmProjects/POI/data/CenterCityPOIInfo.csv'
        with open(path,'a') as f:
            totalPOI= data['total']
            print('totalPOI:', totalPOI)
            #f.write('total' + ':' + str(totalPOI)+'\n')
            restaurant.append(totalPOI)

            for item in data['results']:
                name = item['name']
                lat = item['location']['lat']
                lng = item['location']['lng']
                add = item['address']
                print(name)
                print(lat)
                print(lng)
                print(add)
                info = name + ',' + str(lat) + ',' + str(lng) + '\n'
                f.write(info)
        count=count+totalPOI
    print('count:',count)
    print('restaurant:',restaurant)
    return restaurant

if __name__=="__main__":
    #keywords=['宿舍','公司企业','学校','美食','购物','休闲娱乐','景区','医疗','政府机构','其他']
    keywords = ['购物']
    allinfo=[]
    for keyword in keywords:
        urls=geturl(keyword)
        POIcountList=getPOI(urls)
        allinfo.append(POIcountList)
    print(allinfo)
    info=pd.DataFrame(allinfo)
    info=info.T
    #info.rename(columns={0:keywords[0],1:keywords[1],2:keywords[2],3:keywords[3],4:keywords[4],5:keywords[5],
                    # 6:keywords[6],7:keywords[7],8:keywords[8],9:keywords[9]},inplace=True)
    info.rename(columns={0: keywords[0]},inplace=True)
    #统计网格总POI数
    info['Col_sum'] = info.apply(lambda x: x.sum(), axis=1)
    print(info)
    #info.to_csv('/home/hll/PycharmProjects/POI/data/info1.csv',header=True,encoding='utf_8',index=False)
    df = pd.DataFrame(columns=["Shopping"])
    df['Shopping'] = info['购物']
    '''
    df['DutyPlace'] = info.apply(lambda x: x['公司企业'] + x['学校']+x['政府机构'], axis=1)
    df['Diet'] = info['美食']
    df['Shopping'] = info['购物']
    df['Amuse'] = info.apply(lambda x: x['休闲娱乐'] + x['景区'], axis=1)
    #df['GovernmentAgencies'] = info['政府机构']
    df['Other'] = info['其他']
    '''
    print(df)
    df.to_csv('/home/hll/PycharmProjects/POI/data/statistic3_1.csv',header=True,
                encoding='utf_8',index=False)
    '''1宿舍 2美食 3购物 4公司企业 5学校 6政府机构 7休闲娱乐 8景区 '''