#!/usr/bin/env python3
# -*- coding: utf-8 -*-


'''
产生全部的网格
从左下开始
'''

from gridMap import varGlobal
import json


from gridMap import gridmap
import csv



# 纬度从上到下变小，经度从左往右变大
# 1存的是小值，2存的是大值
def generateGrid():
    l = []
    for i in range(1,varGlobal.COUNTCELL+1):
        r = gridmap.getBorderByGridId(i)
        newgrid = gridmap.Grid(i, r[0], r[1], r[2], r[3])
        l.append(gridmap.grid2dict(newgrid))
    #with open('app/static/GuiYangGrid.js', 'w') as f:
    with open('app/static/GuiYangGrid4836.js', 'w') as f:
        f.write('var GuiYangGrid = ')
        json.dump(l, f)#把Python object写入到.js文件
        f.write(';')

def generateGridTxt():
    l = []
    for i in range(1,varGlobal.COUNTCELL+1):
        r = gridmap.getBorderByGridId(i)
        newgrid = [i,r[0], r[1], r[2], r[3]]
        l.append(newgrid)
    #with open('data/grid4836.csv', 'w', newline='') as f:   #python3
    with open('data/grid4836.csv', 'w') as f:
        write = csv.writer(f)
        write.writerow(['id','lat_down', 'lat_up', 'lng_left', 'lng_right'])
        write.writerows(l)

if __name__=="__main__" :
    generateGrid()
    generateGridTxt()

