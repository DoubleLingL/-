from travel_chain_local import *
from file_operations import *
from divide_data import *
from config import *
from get_freq_time import *
from get_res_work_place import *
from model import *
from pyspark.sql.types import IntegerType
from pyspark.sql import functions as sql_func
from pyspark.sql import SparkSession
from pyspark import AccumulatorParam
from pyspark import SparkContext
import datetime as dt
import time
import sys
from collections import *


__author__ = 'HuangTaoyu'


# def main(all_person_div_week_pts):
# 	person_div_week_pts, person_div_stay_pts = all_person_div_week_pts[0], all_person_div_week_pts[1]
# 	spts, spts_index, h_freq, l_time, single_hf, single_lt = get_several_freq_time(person_div_week_pts) # 得到高频长时点
# 	res_work = get_resplace_workplace( person_div_week_pts, spts, 
# 										spts_index, h_freq, l_time,
# 										single_hf, single_lt ) # 得到职住地
# 	get_serveral_days_od( [person_div_week_pts[SAMPLING_INDEX]], spts, spts_index, 
# 							h_freq, l_time, person_div_stay_pts, 
# 							res_work, SHOP_HOS_STAY_TIME.value, 
# 							poi_pts.value, SAMPLING_INDEX) #对抽样日的数据进行OD识别
# 	alist,have_trip = [],False
# 	for sp in person_div_week_pts[SAMPLING_INDEX]:
# 		if sp.point_type.value == 'origin':
# 			have_trip = True
# 		arow = (sp.loc.uid, sp.longitude, sp.latitude, 
# 				sp.start_time, sp.end_time, sp.add_type.value,
# 				sp.point_type.value, sp.trip_purpose.value, 
# 				sp.age, sp.traffic_id, sp.base_station_id)
# 		alist.append(arow)
# 	if 'rwplace' not in res_work and 'resplace' not in res_work and not have_trip:  #过滤没有住也也没有出行的用户
# 		return []
# 	if  len(spts) < 2: #过滤统计天数内没有动过的用户
# 		return []
# 	else:
# 		return alist


def get_stay_dict(alist):
	if alist==[]:
		return False
	global stay_list
	for sp in alist[0][SAMPLING_INDEX]:
		if sp.point_type == PointType.stay:
			t = int((sp.end_time - sp.start_time).seconds/30)
			t = t if t<=239 else 239
			stay_list[t] += 1
	return True


def get_SHOP_HOS_STAY_TIME(alist,person_sum):
	thesum = 0
	for index,item in enumerate(alist):
		thesum += item.value
		if (thesum-person_sum)/person_sum >= RESERVED_TRIP_STRENGTH:
			SHOP_HOS_STAY_TIME = (len(alist)-index-1)*30
			return SHOP_HOS_STAY_TIME



if __name__ == '__main__':
	if(len(sys.argv)!=2):
		exit(0)
	poi_path = sys.argv[1]

	spark = SparkSession.builder.master("yarn") \
		.appName('Tast_df') \
		.enableHiveSupport() \
		.getOrCreate()
	
	# 初始化累加器
	sc = spark.sparkContext
	stay_list = []
	for i in range(240):
		acc = sc.accumulator(0)
		stay_list.append(acc)

	'''
	获取Hive表的DataFrame
	9.12-9.18停留时长15分钟+一次清洗: base.gy_cleaned_week1218_al_15min_mapped_filled
	9.12-9.18停留时长10分钟+一次清洗: base.gy_cleaned_week1218_al_10min_new_mapped_filled
	9.12-9.18停留时长10分钟+二次清洗: base.gy_cleaned_week1218_patternclean_2w_al_mapped_filled
	9.05-9.11停留时长10分钟+二次清洗: base.gy_week0511_preprocessed
	9.19-9.25停留时长10分钟+二次清洗: base.gy_week1925_preprocessed
	李文杰1.9号重洗数据(修正基站点在越南,即速度阈值不生效的问题)9.12--9.18停留时长10分钟+二次清洗: base.gy_week1218_rock_corrected
	李文杰1.10号重洗数据(修正基站点在越南,即速度阈值不生效的问题)9.5--9.11停留时长10分钟+二次清洗: base.gy_week0511_rock_corrected
	李文杰1.10号重洗数据(修正基站点在越南,即速度阈值不生效的问题)9.19--9.25停留时长10分钟+二次清洗:base.gy_week1925_rock_corrected
	'''
	df = spark.table('base.gy_week1218_rock_corrected')

	''' 
	获取
	1抽样日的停留时间分布,填充到累加器
	2按用户按天分割的活动链
	3按用户按天分割的夜间聚合前的原始停留点
	'''
	rdd1 = df.rdd\
			.map(load_pts_new)\
			.groupByKey()\
			.mapValues(lambda pts:sorted(pts, key=lambda x: x.start_time, reverse=False))\
			.values()\
			.map(lambda pts:divideptsbyday_and_addnightime(list(pts)))\
			.filter(get_stay_dict)
	rdd1.cache

	# 获取用户个数
	person_sum = rdd1.count()
	print('person_sum: ',person_sum)	
	
	# 得到阈值--出行最短停留时长,并设其为广播变量
	stay_list.reverse()
	SHOP_HOS_STAY_TIME = sc.broadcast(get_SHOP_HOS_STAY_TIME(stay_list, person_sum))
	print(stay_list)
	summ = 0
	for index,item in enumerate(stay_list):
		summ+=item.value
		print(index,(summ-person_sum)/person_sum)
	print('SHOP_HOS_STAY_TIME: ',SHOP_HOS_STAY_TIME.value)

	# 加载POI到广播变量
	rdd2 = sc.textFile(poi_path)\
			.flatMap(load_poi)\
			.collect()
	poi_pts = sc.broadcast(rdd2)

	# 对抽样日数据进行OD识别
	rdd3 = rdd1.flatMap(lambda alist:creat_travel_chain(alist,SHOP_HOS_STAY_TIME.value,poi_pts.value))\
			.filter(lambda pts: pts != [])
	rdd1.unpersist

	df1 = spark.createDataFrame(rdd3,['uid', 'longitude','latitude',
									'start_time','end_time', 'add_type', 
									'point_type', 'trip_purpose',
									'age', 'ta_id', 'level'])
	df1.write.mode('overwrite').saveAsTable('huangtaoyu_week1218_tuesday_al_10min_2clean_pro_mapped_filled_od_version8')


