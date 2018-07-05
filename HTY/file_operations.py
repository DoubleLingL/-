from model import *
import json
import csv
from collections import *

__author__ = 'HuangTaoyu'

def load_poi(line):
	'''
	加载POI数据
	'''
	return [POI(line)]

def load_pts_new(arow):
	'''
	加载所有用户的数据
	'''
	line = [str(arow['age']), arow['end_time'].strftime(DATE_FORMAT), 
			str(arow['latitude']), str(arow['longitude']),
			str(arow['point_type']), arow['start_time'].strftime(DATE_FORMAT), 
			str(arow['trip_purpose']), str(arow['uid']),
			str(arow['ta_id']), str(arow['level'])]
	line = ','.join(line)
	sp = UserLocation(line,delimiter=',')
	if arow['point_type'] == 'stay':
		point_type = PointType.stay
	else:
		point_type = PointType.normal
	sp = RichPoint(sp, arow['end_time'],
			trafficid=arow['ta_id'],
			stationid=arow['level'],
			point_type=point_type, gen_age=True)
	return (sp.loc.uid, sp)
