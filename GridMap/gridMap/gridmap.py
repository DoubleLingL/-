#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'xiaoby'


'''generate the grid id according to the input latitude and longitude
   getGridIdByLatLng()：根据给定的经纬度获得网格编号，网格编号从左下角一维编号，编号从1开始
   getBorderByGridId(): 根据ID返回网格边界，返回的是lat_down, lat_up, lng_left, lng_right
'''


from gridMap import varGlobal
import json
from geojson import LineString, Feature
import  geojson


class Grid(object):
    def __init__(self, gridid, lat1, lat2, lng1, lng2):
        self.gridid = gridid
        self.lat1 = lat1
        self.lat2 = lat2
        self.lng1 = lng1
        self.lng2 = lng2

class Record(object):
    def __init__(self, imsi, lng, lat, utime1):
        self.imsi = imsi
        self.lng = float(lng)
        self.lat = float(lat)
        self.utime = utime1

def grid2dict(obj):
    return{
        'gridId': obj.gridid,
        'lat1': obj.lat1,
        'lat2': obj.lat2,
        'lng1': obj.lng1,
        'lng2': obj.lng2
    }

def getGridIdByLatLng(lngin, latin):
    lng = float(lngin)
    lat = float(latin)
    if lat > varGlobal.MAXLAT:
        x = varGlobal.COUNTLAT - 1
    elif lat < varGlobal.MINLAT:
        x = 0
    else:
        x = int((lat - varGlobal.MINLAT ) / varGlobal.SIZELAT)
    if lng > varGlobal.MAXLNG:
        y = varGlobal.COUNTLNG - 1
    elif lng < varGlobal.MINLNG:
        y = 0
    else:
        y = int((lng - varGlobal.MINLNG) / varGlobal.SIZELNG)
    return x * varGlobal.COUNTLNG + y + 1


def getBorderByGridId(gridid):
    row = int(gridid)//varGlobal.COUNTLNG # 返回整数部分　　　行号
    column = int(gridid) - row * varGlobal.COUNTLNG     #  列号
    if column == 0:
        column = varGlobal.COUNTLNG
        row = row - 1

    lat1 = float('%.8f' % (varGlobal.MINLAT + row * varGlobal.SIZELAT))
    lat2= float('%.8f' % (varGlobal.MINLAT + (row + 1) * varGlobal.SIZELAT))
    lng1 = float('%.7f' % (varGlobal.MINLNG + (column - 1) * varGlobal.SIZELNG))
    lng2 = float('%.7f' % (varGlobal.MINLNG + column * varGlobal.SIZELNG))
    return lat1, lat2, lng1, lng2



def readIn():
    #with open('data/f504c3463b1d05cbb33b219ba9555a39.csv', 'r') as f:
    with open('data/cc8.csv', 'r') as f:
        l = f.readlines()
    data = list(map(lambda x: Record(*x.strip().split(',')), l))
    print(l)
    return data


def writeJs(data):
    points = [(r.lng, r.lat) for r in data]
    ids = [getGridIdByLatLng(float(x[0]), float(x[1])) for x in  points]
    print(ids)
    borders = [getBorderByGridId(x) for x in  ids]
    print(borders)
    grid_border = [grid2dict(Grid(r[0],r[1][0],r[1][1],r[1][2],r[1][3])) for r in zip(ids, borders)]
    line = LineString(tuple(points))
    feature_linestring = Feature(
        geometry= line,
        properties={"popupContent": str(data[0].imsi)}
    )
    markers = [{'lng': r.lng, 'lat': r.lat, 'time': r.utime, 'imsi': r.imsi} for r in data]

    #with open('app/static/borders.js', 'w') as f:
    with open('app/static/borders_cc8.js', 'w') as f:
        f.write('var userlocation=[')
        f.write('\n')
        geojson.dump(feature_linestring, f)
        f.write('];')
        f.write('\n')
        f.write('var gridBorder = ')
        json.dump(grid_border, f)
        f.write(';')
        f.write('\n')
        f.write('var stayPoints=')
        f.write('\n')
        json.dump(markers, f)
        f.write(';')


def test():
    a = readIn()
    writeJs(a)

if __name__=="__main__" : test()

