'''
model:字段顺序与后面50000用户的数据字段相符
'''

import datetime as dt
from geopy.distance import great_circle
from enum import Enum

__author__ = 'JackJay'

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
OUT_DELIMITER = ','


class GeoPoint:
    """
    代表一个地理定位点
    
    包含以下可访问的属性:
    longitude : 经度
    latitude : 纬度
    
    快捷方式(实例p1, p2):
    p1 + p2 : 加法重载, 返回新定位点,经纬度分别为2点经纬度之和
    p1 - p2 : 减法重载, 返回2点间大圆距离，单位米
    p1 += p2 : 自加重载, 相当于 p1 = p1 + p2
    p1 == p2 : 等值判断重载, 经纬度完全相同时才判相等，否则不相等
    str(p1) : 返回二元组形式的字符串
    """
    def __init__(self, longitude=0, latitude=0,copy=False,geop=None):
        if copy:
            self.longitude = geop.longitude
            self.latitude = geop.latitude 
        else:
            self.longitude = longitude
            self.latitude = latitude

    # 计算两个轨迹点的空间距离，单位m，返回正数，使用vincenty公式
    def distance(self, another):
        if not isinstance(another, GeoPoint):
            return TypeError('不支持的类型 %s' % type(another))
        return great_circle((self.latitude, self.longitude), (another.latitude, another.longitude)).m

    # 重载 - 运算符
    __sub__ = distance

    # 位置是否相同
    def __eq__(self, other):
        if isinstance(other, GeoPoint):
            return self.longitude == other.longitude and self.latitude == other.latitude
        return False

    # 重载 + 运算符
    def __add__(self, other):
        if isinstance(other, GeoPoint) or isinstance(other, UserLocation):
            longitude = self.longitude + other.longitude
            latitude = self.latitude + other.latitude
            return GeoPoint(longitude, latitude)
        else:
            raise TypeError('不支持')

    # 重载 += 运算符
    def __iadd__(self, other):
        if isinstance(other, GeoPoint):
            self.longitude += other.longitude
            self.latitude += other.latitude
        else:
            raise TypeError('不支持')

    def __str__(self):
        return '(%s, %s)' % (self.longitude, self.latitude)

    __repr__ = __str__


class UserLocation:
    """
    代表一个用户的一个定位点
    
    包含以下可访问属性:
    uid : 用户id
    longitude : 经度
    latitude : 纬度
    time : 定位时间
    
    快捷方式(实例 loc1, loc2):
    lo1 == loc2 : 等值判断重载， 经纬度完全相同时相等，负责不等
    str(loc) : 返回字段按默认分隔符OUT_DELIMITER分隔的一行字符串
    """
    def __init__(self, data=None, delimiter='\t', delimited=False,copy=False,usrloc=None):
        """
        构造函数，从字符串或按字段顺序排列的list中构造对象
        :param data: 由delimiter分隔的字符串，或者已经分隔的list
        :param delimiter: 字段分隔符
        :param delimited: 是否已经分隔
        """
        if copy:
            self.uid = usrloc.uid
            self.time = usrloc.time
            self.point = GeoPoint(copy=True, geop=usrloc.point)
        else:
            fields = data if delimited else data.split(delimiter)
            self.uid = fields[7]
            self.point = GeoPoint(longitude=float(fields[3]), latitude=float(fields[2]))
            self.time = dt.datetime.strptime(fields[5], DATE_FORMAT)

    def distance(self, another):
        if isinstance(another, UserLocation):
            return self.point.distance(another.point)
        elif isinstance(another, GeoPoint):
            return self.point.distance(another)
        else:
            raise TypeError('不支持的类型 %s' % type(another))

    # 计算两个轨迹点的时间间隔，单位s，返回正数，无所谓谁减谁
    def time_duration(self, another):
        return abs((self.time - another.time).total_seconds())

    # 计算两个轨迹点间的平均速度
    def speed(self, another):
        if isinstance(another, UserLocation):
            distance = self.distance(another.point)
            time = self.time_duration(another)
            return 0 if time == 0 else distance / float(time)
        else:
            raise TypeError('不支持的类型 %s' % type(another))

    # 转换成经纬度对，方便矩阵运算
    def get_pair(self, lng_first=True):
        return [self.point.longitude, self.point.latitude]

    # 用经纬度对值替换对象原有的经纬度
    def set_pair(self, pair, lng_first=True):
        self.point.longitude, self.point.latitude = pair[0], pair[1]

    def __getattr__(self, item):
        if item == 'longitude':
            return self.point.longitude
        elif item == 'latitude':
            return self.point.latitude
        else:
            raise AttributeError('没有此属性')

    # 判断定位点位置是否相同
    def __eq__(self, other):
        return self.point == other.point

    # loc转换为字符串，方便输出，自带换行。
    def __str__(self):
        return OUT_DELIMITER.join([self.uid, str(self.point.longitude), str(self.point.latitude),
                                    dt.datetime.strftime(self.time, DATE_FORMAT)])


class PointType(Enum):
    """
    定位点枚举类型
    """
    normal = 'normal'
    stay = 'stay'
    # =================Huangtaoyu==================
    origin = 'origin'
    o_and_d = 'o_and_d'
    destination = 'destination'

    # 以下为了测试停留点被过滤的原因
    close_dis = 'close_dis'
    trip_timediff = 'trip_timediff'
    short_time_bef = 'short_time_bef'
    short_time_aft = 'short_time_aft'
    # =================Huangtaoyu==================

class TripPurpose(Enum):
    """出行目的枚举类型"""
    unknown = 'unknown'
    # =================Huangtaoyu==================
    work = 'work'
    study = 'study'
    hospital = 'hospital'
    shopping = 'shopping'
    restfun = 'restfun'
    back = 'back'
    something = 'something'

    backhome = 'backhome'#==========12.27改，查看其它的组成==========
    nopoi = 'nopoi'#==========12.27改，查看其它的组成==========

    # =================Huangtaoyu==================

# =================Huangtaoyu==================
class AddressType(Enum):

    unknown = 'unknown'
    restplace = 'restplace'
    workplace = 'workplace'
    activityplace = 'activityplace'

# =================Huangtaoyu==================

class RichPoint:
    """
    丰富点类型，包含丰富的额外信息
    
    包含以下可访问属性:
    uid : 用户id
    longitude : 经度
    latitude : 纬度
    start_time : 停留起始时间
    end_time : 停留结束时间
    point_type : 点类型
    trip_purpose : 出行目的
    age : 用户年龄
    address_type : 地理属性   #=================Huangtaoyu==================
    
    快捷方式(实例p):
    str(p) : 返回一行字段按OUT_DELIMITER分隔的字符串
    """

    #================= Huangtaoyu ==================
    def __init__(self, loc=None, end_time=None, trafficid=0, stationid=0, point_type=PointType.normal, addtype = AddressType.unknown, purpose=TripPurpose.unknown, gen_age=False , copy=False, richp=None ):
        if copy:
            self.loc = UserLocation(copy = True,usrloc = richp.loc)
            self.end_time = richp.end_time
            self.trip_purpose = richp.trip_purpose
            self.point_type = richp.point_type
            self.add_type = richp.add_type
            self.age = richp.age
            self.traffic_id = richp.traffic_id
            self.base_station_id = richp.base_station_id
        else:
            self.loc = loc
            self.end_time = end_time
            self.point_type = point_type
            self.trip_purpose = purpose
            self.add_type = addtype
            self.traffic_id = trafficid
            self.base_station_id = stationid
    #================= Huangtaoyu ==================
        if gen_age:
            # 根据uid生成年龄，uid相同则age一定相同，但uid不同也有可能age相同
            # 1 <= num <= 60
            num = hash(self.loc.uid) % 60 + 1

            # 17 <= age <= 60
            self.age = num if num >= 17 else num + 17

    # def __getattr__(self, item):
    #     if item == 'start_time':
    #         return self.loc.time
    #     else:
    #         return self.loc.__getattr__(item)

    def __getattr__(self, item):
        if item == 'start_time':
            return self.loc.time
        elif item in ['uid', 'longitude', 'latitude']:
            return self.loc.__getattr__(item)
        else:
            raise AttributeError('No such Attribute!')

    #================================Huangtaoyu================================

    # def __str__(self):
    #     return OUT_DELIMITER.join([str(self.loc), self.end_time.strftime(DATE_FORMAT),
    #                                self.point_type.value, self.trip_purpose.value, str(self.age)])

    def __str__(self):
        return OUT_DELIMITER.join([self.loc.uid, str(self.loc.point.longitude), str(self.loc.point.latitude), 
                                    self.start_time.strftime(DATE_FORMAT), self.end_time.strftime(DATE_FORMAT),
                                   self.add_type.value, self.point_type.value, self.trip_purpose.value, 
                                   str(self.age), str(self.traffic_id), str(self.base_station_id)])

    #================================Huangtaoyu================================

    __repr__ = __str__


class UserTrajectory:
    """
    用户轨迹类，包含以下可访问属性
    sorted_locations : 按时间先后顺序排列的UserLocation对象list
    time_durations : sorted_locations中每2个定位点间的时间间隔list
    distances : sorted_locations中每2个定位点间的**大圆**距离
    speed_list : sorted_locations中每2个定位点间**平均**速度
    
    快捷方式(比如实例名为traj)：
    len(traj) : 返回该轨迹中的定位点个数, 等同于len(traj.sorted_locations)
    str(traj) : 返回固定格式字符串
    traj[i] : 像访问list一样使用下标访问sorted_locations，等同于traj.sorted_locations[i]
    """
    def __init__(self, locations, need_sorted=True):
        self.uid = locations[0].uid
        if need_sorted:
            locations = sorted(locations, key=lambda x: x.time)
        self.sorted_locations = locations
        self._time_durations = None
        self._distances = None
        self._speed_list = None

    # 延时计算时间间隔、距离、速度
    def __getattr__(self, item):
        if item == 'time_durations':
            if self._time_durations is None:
                self._time_durations = \
                    [self.sorted_locations[i].time_duration(self.sorted_locations[i + 1])
                     for i, l in enumerate(self.sorted_locations) if i <= len(self.sorted_locations) - 2]
            return self._time_durations
        elif item == 'distances':
            if self._distances is None:
                self._distances = [self.sorted_locations[i].distance(self.sorted_locations[i + 1])
                                   for i, l in enumerate(self.sorted_locations) if i <= len(self.sorted_locations) - 2]
            return self._distances
        elif item == 'speed_list':
            if self._speed_list is None:
                self._speed_list = list(map(lambda s, t: s / float(t) if t != 0 else 0,
                                            self.distances, self.time_durations))
            return self._speed_list
        else:
            raise AttributeError('没有这个属性')

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.sorted_locations[item]
        else:
            raise TypeError('不支持非int访问')

    def __str__(self):
        '\n'.join(list(map(str, self.sorted_locations)))

    def __len__(self):
        return len(self.sorted_locations)


#======================Huangtaoyu=========================

# class POI(GeoPoint):
#     """
#     POI数据类,继承GeoPoint
    
#     包含以下可访问属性:

#     longitude : 经度
#     latitude : 纬度
#     loc_type: 建筑属性编号
#     """
#     def __init__(self, data):
#         fields = data.split(OUT_DELIMITER)
#         super(POI, self).__init__(float(fields[1]), float(fields[2]))
#         self.latitude = float(fields[2])


class POI():
    """
    POI数据类
    
    包含以下可访问属性:

    longitude : 经度
    latitude : 纬度
    loc_type: 建筑属性编号
    """
    def __init__(self, data):
        fields = data.split(OUT_DELIMITER)
        self.loc_type = int(fields[0])
        # print(type(fields[1]),type(fields[1]))
        self.longitude = float(fields[1])
        self.latitude = float(fields[2])


    def distance(self, another):
        return great_circle((self.latitude, self.longitude), (another.latitude, another.longitude)).m

        


        