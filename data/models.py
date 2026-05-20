from dataclasses import dataclass

@dataclass
class AGGFrame:
    gx: float
    gy: float
    gz: float


@dataclass
class ACCFrame:
    ax: float
    ay: float
    az: float

@dataclass
class GNSSFrame:
    timestamp: str    # UTC时间 "092208.00"
    lat: float        # 十进制度，北正南负
    lon: float        # 十进制度，东正西负
    fix_quality: int  # 0=无效 1=GPS 2=DGPS
    num_sats: int     # 使用卫星数
    hdop: float       # 水平精度因子
    altitude: float   # 海拔 (m)
