#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Huang lingling

import pandas as pd
from pandas import Series,DataFrame
import matplotlib.pyplot as plt
import matplotlib as mpl
import  matplotlib.dates as mdate
from matplotlib.dates import AutoDateFormatter,DateFormatter
import matplotlib.ticker as mtick
import numpy as np
from numpy import *
path='/media/hll/amuse/gy/predict23142/flow48/flow0511.csv'
#path='/media/hll/amuse/gy/1925grid/23142_0919_25/23142flow1/flow1.csv'
#path='/media/hll/amuse/gy/0511grid/23142_0905_11/23142flow1/0907flow1.csv'
#path='/media/hll/amuse/gy/1218grid/23142_0912_18/23142flow1/flow1.csv'
#path='/media/hll/amuse/gy/1218grid/23142_0912_18/direcflow/direcflow.csv'
#path='/media/hll/amuse/gy/1925grid/23142_0919_25/direcflow/direcflow.csv'
df=pd.read_csv(path)
print(df.head())

df.index=pd.date_range('2016-09-05 00:00:00',freq='0.5H',periods=336)
df.plot(x_compat=True)
#ax.set_major_formatter(mdate.DateFormatter('%H:%M:%S'))
#plt.title('2016/09/12 -2016/09/18 Mon-Sun')
plt.legend(loc='best',ncol=1,bbox_to_anchor=(0.8,0.785))
#plt.legend(loc='best',ncol=2,bbox_to_anchor=(0.7,0.785))
plt.title('2016/09/05-11 ')

plt.show()
#20160907
#seqGridInFlow
#194,199,178,116,127,131,354,1278,1847,2160,2022,1917,1927,1641,1831,1819,1833,2174,1764,1576,1310,1183,930,632
#seqGridOutFlow
#387,242,202,147,145,152,423,1456,2035,2317,2071,1934,1950,1666,1815,1833,1832,2152,1748,1496,1237,1089,807,354
#seqGridFlow
#488,296,240,168,163,170,523,2064,2805,3257,3022,2751,2831,2397,2583,2646,2671,3448,2661,2102,1799,1616,1272,838

#20160910
#seqGridInFlow
#202,269,179,148,126,160,323,1085,1415,1582,1625,1647,1690,1578,1563,1511,1586,1731,1580,1423,1209,1244,1022,652
#seqGridOutFlow
#377,334,211,166,136,176,381,1193,1547,1697,1677,1687,1726,1611,1565,1512,1585,1718,1551,1393,1170,1127,878,364
#seqGridFlow
#485,414,234,190,152,208,457,1731,2080,2273,2188,2339,2463,2179,2113,2044,2140,2371,2197,1966,1690,1707,1423,852





