import math


def leapyear(year):
    if year % 400 == 0:
        return True
    elif year % 100 == 0:
        return False
    elif year % 4 == 0:
        return True
    else:
        return False


def calc_time(year, month, day, hour=12, minute=0):
    # Get day of the year, e.g. Feb 1 = 32, Mar 1 = 61 on leap years
    month_days = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30]
    day = day + sum(month_days[:month])
    leapdays = leapyear(year) and day >= 60 and (
        not (month == 2 and day == 60))
    if leapdays:
        day += 1

    # Get Julian date - 2400000
    hour = hour + minute / 60.0  # hour plus fraction
    delta = year - 1949
    leap = delta // 4  # former leapyears
    jd = 32916.5 + delta * 365 + leap + day + hour / 24.0
    # The input to the Astronomer's almanac is the difference between
    # the Julian date and JD 2451545.0 (noon, 1 January 2000)
    time = jd - 51545
    return time


def meanLongitudeDegrees(time):
    return ((280.460 + 0.9856474 * time) % 360)


def meanAnomalyRadians(time):
    return (math.radians((357.528 + 0.9856003 * time) % 360))


def eclipticLongitudeRadians(mnlong, mnanomaly):
    return (math.radians((mnlong + 1.915 * math.sin(mnanomaly) + 0.020 * math.sin(2 * mnanomaly)) % 360))


def eclipticObliquityRadians(time):
    return (math.radians(23.439 - 0.0000004 * time))


def rightAscensionRadians(oblqec, eclong):
    num = math.cos(oblqec) * math.sin(eclong)
    den = math.cos(eclong)
    ra = math.atan(num / den)
    if den < 0:
        ra += math.pi
    if (den >= 0 and num < 0):
        ra += 2 * math.pi
    return (ra)


def rightDeclinationRadians(oblqec, eclong):
    return (math.asin(math.sin(oblqec) * math.sin(eclong)))


def greenwichMeanSiderealTimeHours(time, hour):
    return ((6.697375 + 0.0657098242 * time + hour) % 24)


def localMeanSiderealTimeRadians(gmst, longitude):
    return (math.radians(15 * ((gmst + longitude / 15.0) % 24)))


def hourAngleRadians(lmst, ra):
    return (((lmst - ra + math.pi) % (2 * math.pi)) - math.pi)


def elevationRadians(lat, dec, ha):
    return (math.asin(math.sin(dec) * math.sin(lat) + math.cos(dec) * math.cos(lat) * math.cos(ha)))


def solarAzimuthRadiansCharlie(lat, dec, ha):
    zenithAngle = math.acos(
        math.sin(lat) * math.sin(dec) + math.cos(lat) * math.cos(dec) * math.cos(ha))
    az = math.acos((math.sin(lat) * math.cos(zenithAngle) -
                    math.sin(dec)) / (math.cos(lat) * math.sin(zenithAngle)))
    if ha > 0:
        az = az + math.pi
    else:
        az = (3 * math.pi - az) % (2 * math.pi)
    return (az)


def sun_position(year, month, day, hour, minute, inputTimeZone=8, lat=30.672, longitude=103.988):
    time = calc_time(year, month, day, hour, minute)
    hour = hour + minute / 60.0 - inputTimeZone
    # Ecliptic coordinates
    mnlong = meanLongitudeDegrees(time)
    mnanom = meanAnomalyRadians(time)
    eclong = eclipticLongitudeRadians(mnlong, mnanom)
    oblqec = eclipticObliquityRadians(time)
    # Celestial coordinates
    ra = rightAscensionRadians(oblqec, eclong)
    dec = rightDeclinationRadians(oblqec, eclong)
    # Local coordinates
    gmst = greenwichMeanSiderealTimeHours(time, hour)
    lmst = localMeanSiderealTimeRadians(gmst, longitude)
    # Hour angle
    ha = hourAngleRadians(lmst, ra)
    # Latitude to radians
    lat = math.radians(lat)
    # Azimuth and elevation
    el = elevationRadians(lat, dec, ha)
    azC = solarAzimuthRadiansCharlie(lat, dec, ha)
    elevation = math.degrees(el)
    azimuth = math.degrees(azC)
    return azimuth, elevation
