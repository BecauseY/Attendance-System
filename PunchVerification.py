from math import radians, cos, sin, asin, sqrt
def WhereAreYou(CurLongitude,CurLatitude,LocationLongitude,LocationLatitude,LocationRadius):
    """
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees)
    """
    # Calculate the great circle distance between two points
    # on the earth (specified in decimal degrees)
    # 将十进制度数转化为弧度
    CurLongitude,CurLatitude,LocationLongitude,LocationLatitude = map(radians, [float(CurLongitude),float(CurLatitude),float(LocationLongitude),float(LocationLatitude)])

    # haversine公式
    dlon = LocationLongitude - CurLongitude
    dlat = LocationLatitude - CurLatitude
    a = sin(dlat / 2) ** 2 + cos(CurLatitude) * cos(LocationLatitude) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # 地球平均半径，单位为公里
    distance = c * r * 1000
    if(distance < float(LocationRadius)):
        return True
    else:
        return False