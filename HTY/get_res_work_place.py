from config import *
from model import *

__author__ = 'HuangTaoyu'

def get_resplace_workplace(divided_sp, spts, spts_index, h_freq, l_time, single_hf, single_lt):
	'''
	对高频\长时地进行职住地判断
	param:
		divided_sp: 某用户统计日内的活动链
		spts, spts_index, h_freq, l_time, single_hf, single_lt: 参见get_freq_time.py
	variate:
		type_list:'00:actvplace,10:resplace,01:workplace,11:rwplace'
	'''

	hf_or_lt,res_work,type_list = list(map(lambda x,y:x+y,l_time,h_freq)),[0]*len(spts),['00']*len(spts) 
	for i,item in enumerate(hf_or_lt):
		if item > 0:
			#indexs:2D,行对应天数,每个list为当天在spts[i]范围内的点的下标
			indexs = [len(ind)>i and ind[i] or [] for ind in spts_index]
			sampling_time = dt.timedelta()
			for ii,item1 in enumerate(indexs):
				for aind in item1:
					st = divided_sp[ii][aind].start_time
					et = divided_sp[ii][aind].end_time
					if (et-st).total_seconds() < MIN_STAYTIME:
						continue
					if (st.hour >= REST_TIME[0] and et.hour <= REST_TIME[2]) \
						or (st.hour >= REST_TIME[3] and et.hour <= REST_TIME[4]) \
						or (st.hour <= REST_TIME[1] and et.hour > REST_TIME[2]):
						type_list[i] = '10' if (type_list[i] == '00' or type_list[i] == '10') else '11'
						if ii == SAMPLING_INDEX:
							sampling_time += (et-st)
					elif st.hour > WORK_TIME[0] \
						and et.hour < WORK_TIME[4] \
						and not(st.hour >= WORK_TIME[1] and et.hour <= WORK_TIME[2]) \
						and not (st.hour >= WORK_TIME[3] and et.hour < WORK_TIME[4]):
						type_list[i] = '01' if (type_list[i] == '00' or type_list[i] == '01') else '11'
			if sampling_time.total_seconds() < TOTAL_WORK_TIME and type_list[i]=='10':
				type_list[i] = '00'
	res_work = [hf_or_lt[i]==0 and 'actvplace' 
				or type_list[i] =='00' and 'actvplace' 
				or type_list[i] =='10' and single_lt[i].total_seconds() >= REST_SEVERAL_LONG_TIME and single_hf[i] >= REST_SEVERAL_HIGH_FREQ and 'resplace'
				or type_list[i] =='10' and (single_lt[i].total_seconds() < REST_SEVERAL_LONG_TIME or single_hf[i] < REST_SEVERAL_HIGH_FREQ) and 'actvplace'
				or type_list[i]=='11' and 'rwplace' 
				or type_list[i]=='01' and 'workplace' 
				for i in range(len(spts))]
	return res_work