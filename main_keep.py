import machine
import math
import time
from datetime import datetime
import urequests
import network
import json
from servo import Servo

rtc = machine.RTC()
tz = "Australia/Brisbane"
latitude = -27.28445993818303
longitude = 153.01750538234373
timeout = 0

ssid = "Colson Network"
pwd = "434f4c534f4e5f46414d494c59"
wifi = network.WLAN(network.STA_IF)

led = machine.Pin(2, machine.Pin.OUT)
led.value(0)

date = ""

def set_servo_pos(angle):
    pulse_width = int(map(lambda x: x * 1000 + 500, (angle, 180)))
    servo.duty(pulse_width)

def connect_wifi():
    global wifi
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.disconnect()
    wifi.connect(ssid, pwd)
    if not wifi.isconnected():
        print('connecting...')
        timeout = 0
        while (not wifi.isconnected() and timeout < 5):
            print(5 - timeout)
            timeout = timeout + 1
            time.sleep(1) 
    if(wifi.isconnected()):
        print('connected')
    else:
        print('not connected')

def updateRTC(tz):
    print(wifi.isconnected())
    if (wifi.isconnected()):
        url = "http://worldtimeapi.org/api/timezone/Australia/Brisbane"
        response = urequests.get(url)
        print(response.status_code)
        data = json.loads(response.text)
        dt = datetime.fromisoformat(data['datetime'])
        year = dt.year
        month = dt.month
        day = dt.day
        weekday = dt.weekday() + 1
        hour = dt.hour
        minute = dt.minute
        second = dt.second
        microsecond = dt.microsecond
        now = (year, month, day, weekday, hour, minute, second, microsecond)
        global rtc
        rtc.datetime(now)
        global date
        date = now
        print("date set")
        led.value(1)
       
def calculate_julian_date(year, month, day, hour, minute, second):
    if month <= 2:
        year -= 1
        month += 12
    A = math.floor(year / 100)
    B = 2 - A + math.floor(A / 4)
    JD = (math.floor(365.25 * (year + 4716))
          + math.floor(30.6001 * (month + 1))
          + day + B - 1524.5
          + (hour + minute / 60 + second / 3600) / 24)
    return JD

def calculate_solar_position(lat, lon, date_time):
    year, month, day, hour, minute, second = date_time
    JD = calculate_julian_date(year, month, day, hour, minute, second)
    d = JD - 2451545.0
    
    # Mean anomaly, degrees
    M = 357.5291 + 0.98560028 * d
    M = M % 360
    
    # Mean longitude of the sun, degrees
    L = 280.46646 + 0.98564736 * d
    L = L % 360
    
    # Ecliptic longitude, degrees
    ecliptic_lon = L + 1.9148 * math.sin(math.radians(M)) + 0.02 * math.sin(math.radians(2 * M)) + 0.0003 * math.sin(math.radians(3 * M))
    ecliptic_lon = ecliptic_lon % 360
    
    # Obliquity of the ecliptic
    epsilon = 23.439 - 0.00000036 * d
    
    # Right ascension, declination
    RA = math.degrees(math.atan2(math.cos(math.radians(epsilon)) * math.sin(math.radians(ecliptic_lon)), math.cos(math.radians(ecliptic_lon))))
    dec = math.degrees(math.asin(math.sin(math.radians(epsilon)) * math.sin(math.radians(ecliptic_lon))))
    
    # Local sidereal time
    GMST = 18.697374558 + 24.06570982441908 * d
    GMST = GMST % 24
    LST = GMST * 15 + lon
    
    # Hour angle
    HA = LST - RA
    if HA < 0:
        HA += 360
    
    # Convert to altitude and azimuth
    x = math.cos(math.radians(HA)) * math.cos(math.radians(dec))
    y = math.sin(math.radians(HA)) * math.cos(math.radians(dec))
    z = math.sin(math.radians(dec))
    
    x_horiz = x * math.sin(math.radians(lat)) - z * math.cos(math.radians(lat))
    y_horiz = y
    z_horiz = x * math.cos(math.radians(lat)) + z * math.sin(math.radians(lat))
    
    azimuth = math.degrees(math.atan2(y_horiz, x_horiz)) + 180
    elevation = math.degrees(math.asin(z_horiz))
    
    return azimuth, elevation

#connect_wifi()

while True:
#     if (date == ""):
#         updateRTC(tz)
#         
#     if (date != ""):        
#         print(rtc.datetime());    
#         current_time = time.localtime()
#         print(current_time)
#         date_time = (current_time[0], current_time[1], current_time[2], current_time[3], current_time[4], current_time[5])
#         date_time = (2024, 7, 9, 17, 43, 0)
#         azimuth, elevation = calculate_solar_position(latitude, longitude, date_time)
#         print("Azimuth:", azimuth)
#         print("Elevation:", elevation)
#         time.sleep(5)
#     if led.value() == 0:
#         led.value(1)
#         set_servo_pos(0)
#     else:
#         led.value(0)
#         set_servo_pos(180)
#         
#     time.sleep(5)

# motor=Servo(pin=22) # A changer selon la broche utilisée
# motor.move(0) # tourne le servo à 0°
# time.sleep(0.3)
# motor.move(90) # tourne le servo à 90°
# time.sleep(0.3)
# motor.move(180) # tourne le servo à 180°
# time.sleep(0.3)
# motor.move(90) # tourne le servo à 90°
# time.sleep(0.3)
# motor.move(0) # tourne le servo à 0°
# time.sleep(0.3)

set_servo_pos(0)
time.sleep(3)
set_servo_pos(180)
time.sleep(3)
set_servo_pos(90)
time.sleep(3)