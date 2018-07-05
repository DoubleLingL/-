from model import *
from config import *
import copy
import datetime as dt

__author__ = 'HuangTaoyu'


def divideptsbyday_and_addnightime(pts):
	'''
	功能有3
	1. 得到按天分割的统计日的数据
	2. 针对夜晚的点进行聚类
	3. 用周一,二,四,五的停留时间补周三凌晨的停留时间
	parame：
		pts: list，某一用户统计日内的活动链
	return:
		[divided_sp, stay_points]: 
		divided_sp: 2D-list,每一个list中存放用户一天的数据
		stay_points: 2D-list,每一个list中存放用户一天夜间被聚类的原始停留点
	'''
	WEEKDATE1,divided_sp,stay_points,end_times = copy.deepcopy(WEEKDATE),[],[],[]
	WEEKDATE1.extend([WEEKDATE1[-1]+1])
	#WEEKDATE1=[12,13,14,15,16,17,18] 
	date = divide_pts_by_time(pts,WEEKDATE1) # 完成功能1
	if len(date) < len(WEEKDATE1):
		return []
	for i in range(len(WEEKDATE1)-1):
		# 完成功能2
		day_pts,stay_pts,end_time = deal_nigth_data_and_addtime(i,pts[date[WEEKDATE1[i]]:date[WEEKDATE1[i+1]]]) 
		divided_sp.append(day_pts)
		stay_points.append(stay_pts)
		end_times.extend(end_time)


	first_index,add_time = -1,False
	stay_points_sum = 0
	for fir_stay_index,item in enumerate(divided_sp[SAMPLING_INDEX]):
		if item.point_type == PointType.stay:
			if first_index==-1:
				first_index = fir_stay_index
			stay_points_sum += 1

	# 完成功能3
	if stay_points_sum > 0: #过滤掉没有停留点的用户
		if len(divided_sp[SAMPLING_INDEX])>first_index+1:
			end_times = sorted(end_times,key=lambda x:x,reverse=True)
			sp0,sp1 = divided_sp[SAMPLING_INDEX][first_index],divided_sp[SAMPLING_INDEX][first_index+1]
			if sp0.end_time.hour < CLUSTER_NIGHT_PTS_END_TIME and \
				sp1.start_time.hour > CLUSTER_NIGHT_PTS_END_TIME:
				
				for new_time in end_times:
					if (sp1.start_time.hour-new_time.hour)*3600 + \
						(sp1.start_time.minute-new_time.minute)*60 + \
						(sp1.start_time.second-new_time.second) > MIN_TIMEDIFF and \
						(new_time.hour-sp0.end_time.hour)*3600 + \
						(new_time.minute-sp0.end_time.minute)*60 + \
						(new_time.second - sp0.end_time.second) >= 0:
						
						sp0.end_time = sp0.end_time.replace(sp0.end_time.year,
															sp0.end_time.month,
															sp0.end_time.day,
															new_time.hour,
															new_time.minute,
															new_time.second)
						add_time = True
						break
				if not add_time:
					'''sp0.end_time.hour < CLUSTER_NIGHT_PTS_END_TIME and sp1.start_time.hour > CLUSTER_NIGHT_PTS_END_TIME
					保证了减去半小时,时间不会重叠'''
					d = sp1.start_time - dt.timedelta(hours=0.5) 
					sp0.end_time = sp0.end_time.replace(d.year, d.month, d.day, d.hour, d.minute, d.second)
		return [divided_sp,stay_points]
	else:
		return []




def divide_pts_by_time(pts,WEEKDATE1):
	'''
	按天切割数据,并返回统计日每天的第一个数据在pts中的下标 update:2017/11/15
	update:2017/12/18 : 停留点切割后判断时长是否达到停留点的标准，重新给point_type赋值
	parame：
		pts: list，某一用户统计日内的活动链
		WEEKDATE1：统计日日期+最后一天的后一天  
		WEEKDATE1=[12,13,14,15,16,17,18]
	return:
		date：dict(),统计日每天的第一个数据在pts中的下标
	'''
	n,length,date = 0,len(pts),dict()
	for i in range(length):
		pt = pts[i+n]
		s_day,e_day = pt.start_time.day,pt.end_time.day
		if e_day < WEEKDATE1[0]:
			continue
		if WEEKDATE1[-1] in date.keys():
			break
		s_day in WEEKDATE1 and s_day not in date.keys() and date.setdefault(s_day,i+n)
		if e_day - s_day > 0:
			#跨天
			del(pts[i+n])
			pt1 = RichPoint(copy=True,richp=pt)#RichPoint 在model.py中定义
			pt1.end_time = pt1.end_time.replace(pt1.start_time.year,pt1.start_time.month,pt1.start_time.day,23,59,59)
			pt1.point_type = PointType.stay if (pt1.end_time-pt1.loc.time).seconds > BASIC_STAYTIME else PointType.normal
			pts.insert(i+n,pt1)
			#dt.timedelta ——> datetime.timedelta 加一天
			thedate = pt1.end_time + dt.timedelta(days = 1)
			yea,mon,day = thedate.year,thedate.month,thedate.day
			if e_day - s_day > 1:
				for ii in range(e_day - s_day - 1):
					pt1 = RichPoint(copy=True,richp=pt)
					pt1.loc.time = pt1.loc.time.replace(yea,mon,day,0,0,0)
					pt1.end_time = pt1.end_time.replace(yea,mon,day,23,59,59)
					day in WEEKDATE1 and day not in date.keys() and date.setdefault(day,i+n+1)
					pts.insert(i+n+1,pt1)
					thedate = pt1.end_time + dt.timedelta(days = 1)
					yea,mon,day = thedate.year,thedate.month,thedate.day
					n+=1
			pt1 = RichPoint(copy=True,richp=pt)
			pt1.loc.time = pt1.loc.time.replace(yea,mon,day,0,0,0)
			pt1.point_type = PointType.stay if (pt1.end_time-pt1.loc.time).seconds > BASIC_STAYTIME else PointType.normal
			day in WEEKDATE1 and day not in date.keys() and date.setdefault(day,i+n+1)
			pts.insert(i+n+1,pt1)
			n+=1
	return date




def deal_nigth_data_and_addtime(DAY_IND,pts):
	'''
	creat:2017.12.15
		将开始时间在0--7点前的点聚类，并将聚类后的点代替原有的多个点，聚类半径：config.py:RESPLACE_DISTANCE
		并记录统计日内其它天的第一个停留点的结束时间
	parame：
		DAY_IND：pts在统计日的下标
		pts：抽样日的活动链
	return：
		new_pts:用户一天中的聚类后的停留点
		stay_pts:用户夜晚被聚类的原始停留点
		end_time_list：统计日内其它天的第一个停留点的结束时间
	'''
	new_pts, stay_pts, begin_point, close_point, end_time_list = [],[],None,[],[] #end_time_list:存放周1245聚合点的end_time
	lat, lng = 0, 0
	for ind,pt in enumerate(pts):
		#CLUSTER_NIGHT_PTS_END_TIME=6  0-6点之间的点,即夜间的点进行聚类
		if pt.start_time.hour <= CLUSTER_NIGHT_PTS_END_TIME:
			is_close = True
			if begin_point == None:
				begin_point,lat,lng = pt, pt.loc.point.latitude, pt.loc.point.longitude
				close_point.append(begin_point)
				begin_point.point_type == PointType.stay and stay_pts.append(begin_point) 
				continue
			if pt.loc.distance(begin_point.loc) > RESPLACE_DISTANCE[min(pt.base_station_id,begin_point.base_station_id)]:
				is_close = False
			if is_close:
				close_point.append(pt)
				lat += pt.loc.point.latitude
				lng += pt.loc.point.longitude
				pt.point_type == PointType.stay and stay_pts.append(pt)
			if not is_close:
				append_new_pt(new_pts, close_point, lat, lng)
				begin_point, lat, lng = pt, pt.loc.point.latitude, pt.loc.point.longitude
				close_point = []
				close_point.append(begin_point)
				if begin_point.point_type == PointType.stay:
					stay_pts.append(begin_point)
		else:
			if len(close_point) > 0:
				append_new_pt(new_pts, close_point, lat, lng)
				close_point = []
				if not DAY_IND==SAMPLING_INDEX:
					end_time_list.append(new_pts[-1].end_time.time())
			rest_pts = pts[ind:]
			new_pts.extend(rest_pts)
			break
	if len(close_point) > 0:
		append_new_pt(new_pts, close_point, lat, lng)
	return new_pts,stay_pts,end_time_list


def append_new_pt(new_pts,close_point,lat,lng):
	new_pt = RichPoint(copy=True,richp=close_point[0])
	new_pt.loc.point.latitude = lat/len(close_point)
	new_pt.loc.point.longitude = lng/len(close_point)
	new_pt.loc.time = close_point[0].start_time
	new_pt.end_time = close_point[-1].end_time
	new_pt.point_type = PointType.stay if (new_pt.end_time-new_pt.loc.time).seconds > BASIC_STAYTIME else PointType.normal
	new_pt.base_station_id = close_point[0].base_station_id
	new_pt.traffic_id = close_point[0].traffic_id
	new_pts.append(new_pt)
