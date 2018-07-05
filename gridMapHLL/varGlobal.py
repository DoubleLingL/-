#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'HUANGLINGLING'
"""
定义全局变量作为常量使用
2018.6.20
主城区 网格映射
"""

import math
'''
# 网格化区域的边界
MAXLAT = 27.336802899269
MINLAT = 26.19699124
MAXLNG = 107.25959083043
MINLNG = 106.14803355374
'''
# 网格化区域的边界   贵阳市主城区经纬度范围  4836个网格
MAXLAT = 26.724595
MINLAT = 26.369862
MAXLNG = 106.845274
MINLNG = 106.566514
# 网格大小，定为500m*500m，500m表现在经纬度上约等于0.004549
SIZELNG = 0.0045487002#0.004548695934959
SIZELAT = 0.0045487013
# 网格数量
COUNTLAT = math.ceil((MAXLAT-MINLAT)/SIZELAT)#一列251个
COUNTLNG = math.ceil((MAXLNG-MINLNG)/SIZELNG)#一行245个
COUNTCELL = COUNTLAT*COUNTLNG
#print(COUNTLAT)
#print(COUNTLNG)
#print(COUNTCELL)

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
CLUSTERTIME = 6
CLUSTERDISTANCE = 2000
STAYTIME=600 # (10*60)s