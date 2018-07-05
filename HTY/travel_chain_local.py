from config import *
from model import *
import file_operations as fo
import divide_data as div
import get_freq_time as ft
import get_res_work_place as rwp
from numpy import *
from collections import *
import random
import datetime as dt
import os
import gc
import time
from pandas import *
import math
import json

__author__ = 'HuangTaoyu'


def creat_travel_chain(pts_list,SHOP_HOS_STAY_TIME,poi_pts):
	div_week_pts, orig_stay_pts = pts_list[0], pts_list[1]
	global trip_minstay_time, POI, spts, spts_index, h_freq, l_time, res_work
	trip_minstay_time, POI = SHOP_HOS_STAY_TIME, poi_pts
	spts, spts_index, h_freq, l_time, single_hf, single_lt = ft.get_several_freq_time(div_week_pts)
	res_work = rwp.get_resplace_workplace(div_week_pts, spts, spts_index, 
										h_freq, l_time, single_hf, single_lt) # 得到职住地
	judge_od_points(div_week_pts[SAMPLING_INDEX], orig_stay_pts[SAMPLING_INDEX])

	alist,have_trip = [],False
	for sp in div_week_pts[SAMPLING_INDEX]:
		if sp.point_type.value == 'origin':
			have_trip = True
		arow = (sp.loc.uid, sp.longitude, sp.latitude, 
				sp.start_time, sp.end_time, sp.add_type.value,
				sp.point_type.value, sp.trip_purpose.value, 
				sp.age, sp.traffic_id, sp.base_station_id)
		alist.append(arow)
	if 'rwplace' not in res_work and 'resplace' not in res_work and not have_trip:  #过滤没有住也也没有出行的用户
		return []
	if  len(spts) < 2: #过滤统计天数内没有动过的用户
		return []
	else:
		return alist


def judge_od_points(pts, orig_stay_pts):
	'''
	得到一天的出行链 update:2017/11/16
	parame：
		pts: 某用户某一天的活动链
	'''
	
	fst_ind,purp_dic = 0,{'company':TripPurpose.work,
						'school':TripPurpose.study,
						'shopstore':TripPurpose.shopping,
						'hospital':TripPurpose.hospital,
						'restfun':TripPurpose.restfun,
						'other':TripPurpose.something,
						None:TripPurpose.unknown}
	for i in range(len(pts)):
		if pts[i].point_type == PointType.stay:
			fst_ind = i
			break
	if pts[fst_ind].point_type == PointType.normal:
		return
	O_points, origin_point = [],pts[fst_ind]
	origin_point.point_type = PointType.origin
	O_points.append(origin_point)
	
	for sp_ind,sp in enumerate(pts[fst_ind+1:]):
		if sp.point_type == PointType.normal:
			continue
		stay_seconds = (sp.end_time-sp.start_time).seconds  #停留时长
		time_diff = abs((sp.start_time-origin_point.end_time).total_seconds())  #出行时长
		dis = sp.loc.distance(origin_point.loc)  #出行距离
		if stay_seconds > MIN_STAYTIME and time_diff > MIN_TIMEDIFF and dis > \
			max(MIN_DISTANCE,MIN_RADIUS[origin_point.base_station_id]):
			if go_back(origin_point, sp, O_points, orig_stay_pts):   #判断返程
				sp.trip_purpose = TripPurpose.back
			else:
				purpose = get_point_type(origin_point, sp, sp_ind+fst_ind+1)
				sp.trip_purpose = purp_dic[purpose]
		if not sp.trip_purpose == TripPurpose.unknown:
			sp.point_type = PointType.o_and_d
			origin_point = sp
			add_different_opoint(sp,O_points)
	if len(O_points) == 1:
		origin_point.point_type = PointType.stay
	else:
		origin_point.point_type = PointType.destination



def add_different_opoint(sp,O_points):
	'''
	create:2017/10/9
	加入与已有O点距离大于MIN_RADIUS的O点
	'''
	is_close = False
	for o_p in O_points:
		if o_p.loc.distance(sp.loc) < MIN_RADIUS[o_p.base_station_id]:
			is_close = True
			break
	if not is_close:
		O_points.append(sp)



def go_back(origin_point, sp, O_points, orig_stay_pts):
	'''
	update:2017/10/6 判断回程,即sp是否与之前的O点在距离MIN_RADIUS内
	parame：
		sp: 停留点
		O_points: list,存放O点
	return:
		True or False
	'''
	O_pts = O_points
	if len(O_points)>1:
		O_pts.extend(orig_stay_pts)
	orig_time,sp_time = 0,0
	for O_point in O_pts:
		if sp.loc.distance(O_point.loc)< MIN_RADIUS[O_point.base_station_id]:
			sp_time = O_point.start_time
		if origin_point.loc.distance(O_point.loc) < MIN_RADIUS[O_point.base_station_id]:
			orig_time = O_point.start_time
		if orig_time != 0 and sp_time != 0:
			break
	if sp_time == 0:  #目的点是新点
		return False
	elif sp_time > orig_time:  #目的点出现的时间比O点晚
		return False
	else:
		return True


def get_point_type(origin_point, sp, sp_ind):
	'''
	update:2017/10/5
	update:2017/10/6  更改逻辑
	update:2017/12/15 更改,前一点的end_time小于6点时,上学改为工作
	poi属性结合高频长时，得到出行目的(上班、上学、购物、就医、其它；返程参见go_back函数)
	'''
	global spts_index, res_work, trip_minstay_time
	poi,poi_lists = match_poi(sp)
	p_type = None
	state = res_work[get_pointindex(sp,sp_ind)]
	if state == 'workplace'\
				 or (state == 'rwplace' and sp.start_time.hour >= WORK_TIME[0] and sp.end_time.hour < WORK_TIME[4]):
		p_type = list(set(poi_lists).intersection(set(SCHOOL))) != [] and sp.age < SCHOOL_AGE \
					and origin_point.end_time.hour >= CLUSTER_NIGHT_PTS_END_TIME and 'school' or 'company'
	elif state == 'actvplace':
		stay_seconds = (sp.end_time-sp.start_time).seconds
		if stay_seconds > trip_minstay_time:
			p_type = poi in HOSPITAL and 'hospital' \
				or poi in FUN and 'restfun' \
				or poi in SHOP and 'shopstore' \
				or 'other'
	else:
		p_type = 'other'
	
	return p_type
			


def get_pointindex(sp,sp_ind):
	"""
	update:2017/10/5
	得到sp在spts, spts_index[any], h_freq, l_time, single_hf, single_lt, res_work的对应下标
	"""
	global spts_index
	for i,indexs in enumerate(spts_index[SAMPLING_INDEX]):
		if sp_ind in indexs:
			return i


def match_poi(sp):
	'''
	update:2017/10/6  返回可能的poi
	对sp进行POI属性匹配
	return:随机选择到的类型、匹配到的所有类型loc_type
	'''
	global POI
	loc_type,MIN_LAT,MAX_LAT = [],sp.latitude-LAT_DIFF,sp.latitude+LAT_DIFF
	for poi in POI:
		if poi.latitude <= MAX_LAT and poi.latitude >= MIN_LAT:
			dist = poi.distance(sp)
			if dist <= POI_DISTANCE:
				if poi.loc_type in HOSPITAL:
					for i in range(HOSPITAL_WEIGHTS):
						loc_type.append(poi.loc_type)
				else:
					loc_type.append(poi.loc_type)
	if len(loc_type)==0:
		return 0,loc_type
	else:
		return random.choice(loc_type),loc_type