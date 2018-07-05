MIN_DISTANCE = 400 #最短出行距离
MIN_TIMEDIFF = 300 #最短出行时长
BASIC_STAYTIME = 10*60 #停留时长>?分钟即为停留点
MIN_STAYTIME = 15*60 #出行目的最短停留时长
MIN_RADIUS = {-1:600,1:600,2:400,3:250}
LAT_DIFF = 0.018 #经度相同时，纬度0.0018=距离200米,纬度0.004=距离450米,纬度0.0054=距离600米,纬度0.015=距离1500米,纬度0.018=距离2000米
SEVERAL_LONG_TIME = 5*3600 #统计天数内累计停留时长大于?小时为多日长时
REST_SEVERAL_LONG_TIME = 24*3600 #住地需满足的多日长时
SEVERAL_HIGH_FREQ = 5 #统计天数内累计出现次数大于?次为多日高频
REST_SEVERAL_HIGH_FREQ = 5 #住地需满足的多日高频
TOTAL_WORK_TIME = 3*3600 #抽样日当天,在职地的累计停留时长需大于TOTAL_WORK_TIME

SCHOOL_AGE = 23 #小于23岁考虑是否为上学
SCHOOL = [4] #POI数据中学校的编号
SHOP = [1] #POI数据中购物场所的编号
HOSPITAL = [3] #POI数据中医院的编号
FUN = [2] #POI数据中休闲娱乐场所的编号
WEEKDATE = [12,13,14,15,16] #统计日内周一到周五的日期
# WEEKDATE = [5,6,7,8,9] #统计日内周一到周五的日期
# WEEKDATE = [19,20,21,22,23] #统计日内周一到周五的日期
SAMPLING_INDEX = 1 #采样日在统计日中的下标
RESPLACE_DISTANCE = {-1:8000,1:3000,2:2000,3:2000} #0--6点的住地聚类范围

REST_TIME = {0:0,1:5,2:7,3:21,4:23} #与住地有关的时间阈值,具体用法见get_res_work_place.py
WORK_TIME = {0:7,1:11,2:14,3:17,4:21} #与职地有关的时间阈值,具体用法见get_res_work_place.py

CLUSTER_NIGHT_PTS_END_TIME = 6 #大于此时间的点不再进行夜间聚类
EXTEND_END_TIME = 0.5 #若夜间停留点替换结束时间失败,则将此点结束时间设为下一点的开始时间-0.5小时
POI_DISTANCE = 2000 #POI匹配半径,单位米
HOSPITAL_WEIGHTS = 20 #医院的权重

RESERVED_TRIP_STRENGTH = 3.1 #预留出行强度
