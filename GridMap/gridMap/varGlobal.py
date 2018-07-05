#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'xiaoby'
"""
定义全局变量作为常量使用

"""

import math
'''
# 网格化区域的边界  整个贵阳市经纬度范围  61495个网格
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
'''
# 网格大小，定为1000m*1000m，1000m表现在经纬度上约等于0.0090090090
SIZELNG = 0.0090974004#0.004548695934959
SIZELAT = 0.0090974026
'''
# 网格数量
COUNTLAT = int(math.ceil((MAXLAT-MINLAT)/SIZELAT))#一列251个  62(500)  31(1000)
COUNTLNG = int(math.ceil((MAXLNG-MINLNG)/SIZELNG))#一行245个  78(500)  39(1000)
COUNTCELL = int(COUNTLAT*COUNTLNG)
print(COUNTLAT)
print(COUNTLNG)
print(COUNTCELL)