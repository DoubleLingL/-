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


def load_pts_new(arow):
	line = [str(arow['uid']), str(arow['point_type']), 
			str(arow['trip_purpose']),
			(arow['end_time']-arow['start_time']).seconds,arow['age']]
	return (line[0], line)

def statistics(personlist):

	global all_stay,long_stay,\
			chuxing,o_or_d,work,study,shopping,hospital,fun,back,\
			something,backhome

	for line in personlist:
		if line[1]=='stay' or line[1]=='destination' or line[1]=='origin'\
			or line[1]=='o_and_d' or line[1] == 'trip_timediff'\
			or line[1] == 'close_dis' or line[1] == 'short_time_aft':
			all_stay += 1  #原始停留点个数
		if line[3] > 15*60:
			long_stay += 1 #大于工作停留阈值的停留点个数
		if line[1]=='destination' or line[1]=='o_and_d':
			chuxing += 1  #出行次数
		if line[1] == 'origin':
			o_or_d += 1
		if line[2]=='work':
			work += 1
		elif line[2]=='study':
			study += 1
		elif line[2]=='back':
			back += 1
		elif line[2]=='shopping':
			shopping += 1
		elif line[2]=='hospital':
			hospital += 1
		elif line[2]=='restfun':
			fun += 1
		elif line[2]=='something':
			something += 1
	return personlist



if __name__ == '__main__':
	print(time.localtime(time.time()))

	spark = SparkSession.builder.master("yarn") \
		.appName('od_analysis') \
		.enableHiveSupport() \
		.getOrCreate()

	# 初始化累加器
	sc = spark.sparkContext
	all_stay = sc.accumulator(0)  #原始停留点个数
	long_stay = sc.accumulator(0) #停留时长大于上班上学阈值的停留点个数	
	chuxing = sc.accumulator(0) #总出行次数
	o_or_d = sc.accumulator(0) #有出行的用户数
	work = sc.accumulator(0) #工作
	study = sc.accumulator(0) #上学
	shopping = sc.accumulator(0) #购物
	hospital = sc.accumulator(0) #就医
	fun = sc.accumulator(0) #娱乐
	back = sc.accumulator(0) #返程
	something = sc.accumulator(0) #其它

	
	'''
	以下表OD规则均为住地频5时24,POI半径2000,预留人均强度3.1,去除没有停留点的用户、统计天数内都没有移动过的用户、没有住地并且没有出行的用户
	9.12-9.18停留时长10分钟+一次清洗OD表: huangtaoyu_al_10min_1clean_mapped_filled_od_version8
	9.12-9.18停留时长10分钟+二次清洗OD表: huangtaoyu_al_10min_2clean_mapped_filled_od_version8 (抽样日周三)
	9.05-9.11停留时长10分钟+二次清洗OD表: huangtaoyu_week0511_al_10min_2clean_mapped_filled_od_version8 (抽样日周三)
	9.19-9.25停留时长10分钟+二次清洗OD表：huangtaoyu_week1925_al_10min_2clean_mapped_filled_od_version8 (抽样日周二)
	9.12-9.18停留时长10分钟+二次清洗OD表+修正速度阈值: huangtaoyu_week1218_al_10min_2clean_pro_mapped_filled_od_version8 (抽样日周三)
	同上,周二: huangtaoyu_week1218_tuesday_al_10min_2clean_pro_mapped_filled_od_version8
	9.05-9.11停留时长10分钟+二次清洗OD表+修正速度阈值: huangtaoyu_week0511_al_10min_2clean_pro_mapped_filled_od_version8 (抽样日周三)
	9.19-9.25停留时长10分钟+二次清洗OD表+修正速度阈值: huangtaoyu_week1925_al_10min_2clean_pro_mapped_filled_od_version8 (抽样日周四)
	'''
	df = spark.table('huangtaoyu_week1218_tuesday_al_10min_2clean_pro_mapped_filled_od_version8')
	rdd = df.rdd\
		.map(load_pts_new)\
		.groupByKey()\
		.values()
	rdd.cache

	personsum = rdd.count()
	print('personsum: ',personsum)

	rdd1 = rdd.map(statistics).count()
	print('原始停留点个数: ',all_stay)
	print('大于15分钟的停留点个数: ',long_stay)

	print('出行次数: ',chuxing,chuxing.value/personsum)
	print('有出行的用户数: ',o_or_d)
	print('工作+上学: ',(work.value+study.value)/chuxing.value)
	print('上学: ',study.value/chuxing.value)
	print('其它: ',something.value/chuxing.value)
	print('购物: ',shopping.value/chuxing.value)
	print('就医: ',hospital.value/chuxing.value)
	print('娱乐: ',fun.value/chuxing.value)
	print('返程: ',back.value/chuxing.value)
	
	rdd.unpersist