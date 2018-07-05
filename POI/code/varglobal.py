#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__='huanglingling'

'''功能：
常变量
'''
import math
import csv

# 网格化区域的边界   贵阳市主城区经纬度范围  4836个网格
MAXLAT = 26.724595
MINLAT = 26.369862
MAXLNG = 106.845274
MINLNG = 106.566514

'''
# 网格化区域的边界   贵阳市主城区经纬度范围  前2170个网格
MAXLAT = 26.529066#26.52451784# 26.45173862
MINLAT = 26.369862
MAXLNG = 106.845274#106.8485334
MINLNG = 106.566514
'''
# 网格大小，定为500m*500m，500m表现在经纬度上约等于0.004549
SIZELNG = 0.0045487002#0.004548695934959
SIZELAT = 0.0045487013

page_nums=20
# 网格数量
COUNTLAT = int(math.ceil((MAXLAT-MINLAT)/SIZELAT))
COUNTLNG = int(math.ceil((MAXLNG-MINLNG)/SIZELNG))
COUNTCELL = int(COUNTLAT*COUNTLNG)
print(COUNTLAT)
print(COUNTLNG)
print(COUNTCELL)