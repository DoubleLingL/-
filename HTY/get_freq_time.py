from model import *
from config import *
import datetime as dt

__author__ = 'HuangTaoyu'

def get_several_freq_time(divided_sp):
	''' 
	得到spts,spts_index,h_freq,l_time,single_hf,single_lt
	parame：
		divided_sp: 2D-list, 每一个list中存用户一天中的停留点数据
	global variate:
		spts ：list,存放不同位置的GeoPoint
		spts_index : 2D-list,行对应天,列对应spts;spts_index[3][2]=[1,4]:第3+1天中的第1+1和第4+1个点与spts[2]在MIN_RADIUS范围内
		h_freq: list, h_freq[i]:与spts[i]对应, 0 or 1, 0:非多日高频
		l_time: list, l_time[i]:与spts[i]对应, 0 or 1, 0:非多日长时
		single_hf: list, single_hf[i]:与spts[i]对应, int, 统计天数内累计出现的次数
		single_lt: list, single_lt[i]:与spts[i]对应, int, 统计天数内累计停留的时长
	'''
	spts, spts_index, h_freq, l_time, single_hf, single_lt = [], [], [], [], [], []
	'''divided_sp=[[],[],[],[],[],[],[]]
	 'i'对应 下标
	 'staypoints'对应 子list
	'''
	for i,staypoints in enumerate(divided_sp):
		freq,time = get_single_freq_time(staypoints, i, spts, spts_index)
		single_hf.extend([0]*(len(freq)-len(single_hf)))
		single_hf = [single_hf[i]+freq[i] for i in range(len(freq))]
		single_lt.extend([dt.timedelta()]*(len(time)-len(single_lt)))
		single_lt = [single_lt[i]+time[i] for i in range(len(time))]
	h_freq = [i >= SEVERAL_HIGH_FREQ and 1 or 0 for i in single_hf]
	l_time = [i.total_seconds() >= SEVERAL_LONG_TIME and 1 or 0 for i in single_lt]
	return spts, spts_index, h_freq, l_time, single_hf, single_lt


def get_single_freq_time(staypoints,ind,spts,spts_index):
	'''
	update:2017/10/18 计算一日累计频率和累计时长
	parame：
		staypoints: list, 用户一天中的停留点数据
		ind: 此日停留点在多日停留点中的下标
		spts: 参照get_several_freq_time()注释spts
		spts_index: 参照get_several_freq_time()注释spts_index
	variate:
		freq: list,freq[i]与spts[i]对应. freq[i]表示spts[i]在这一天中出现的次数
		time: list,time[i]与spts[i]对应. time[i]表示用户在spts[i]经纬度停留的时长
	return:
		freq,time
	'''
	freq,time = [0]*len(spts) if len(spts)>0 else [],[dt.timedelta()]*len(spts) if len(spts)>0 else []
	spts_index.append([])
	for i in range(len(spts)):
		spts_index[-1].append([])	
	for i,spt in enumerate(staypoints):	
		if spt.point_type != PointType.stay:
			continue	 
		is_in = False
		for ii,a_spts in enumerate(spts):
			if spt.loc.distance(a_spts.loc) < MIN_RADIUS[a_spts.base_station_id]:
				spts_index[ind][ii].append(i)
				freq[ii]+=1
				time[ii]+=spt.end_time-spt.start_time
				is_in = True
				break
		if len(spts)==0 or not is_in:
			spts.append(RichPoint(copy=True,richp=spt))
			spts_index[ind].append([i])
			freq.append(1)
			time.append(spt.end_time-spt.start_time)
	return freq,time