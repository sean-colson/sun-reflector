import math

class SunPosition:
    
    def __init__(self, location, refraction=True):
        self.location = location
        self.refraction = refraction

    def getElevation(when):
        year, month, day, hour, minute, second, timezone = when
        latitude, longitude = self.location
        rad, deg = math.radians, math.degrees
        sin, cos, tan = math.sin, math.cos, math.tan
        asin, atan2 = math.asin, math.atan2
        rlat = rad(latitude)
        rlon = rad(longitude)
        greenwichtime = hour - timezone + minute / 60 + second / 3600
        daynum = (
            367 * year
            - 7 * (year + (month + 9) // 12) // 4
            + 275 * month // 9
            + day
            - 730531.5
            + greenwichtime / 24
        )
        mean_long = daynum * 0.01720279239 + 4.894967873
        mean_anom = daynum * 0.01720197034 + 6.240040768
        eclip_long = (
            mean_long
            + 0.03342305518 * sin(mean_anom)
            + 0.0003490658504 * sin(2 * mean_anom)
        )
        obliquity = 0.4090877234 - 0.000000006981317008 * daynum
        rasc = atan2(cos(obliquity) * sin(eclip_long), cos(eclip_long))
        decl = asin(sin(obliquity) * sin(eclip_long))
        sidereal = 4.894961213 + 6.300388099 * daynum + rlon
        hour_ang = sidereal - rasc
        elevation = asin(sin(decl) * sin(rlat) + cos(decl) * cos(rlat) * cos(hour_ang))
        azimuth = atan2(
            -cos(decl) * cos(rlat) * sin(hour_ang),
            sin(decl) - sin(rlat) * sin(elevation),
        )
        azimuth = into_range(deg(azimuth), 0, 360)
        elevation = into_range(deg(elevation), -180, 180)
        if refraction:
            targ = rad((elevation + (10.3 / (elevation + 5.11))))
            elevation += (1.02 / tan(targ)) / 60
        return (round(azimuth, 2), round(elevation, 2))
    

