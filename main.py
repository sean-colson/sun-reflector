import time
import machine
from servo import Servo
from sunpos import SunPosition

az_pin = machine.Pin(15)
az_servo = Servo(az_pin)
angle_pin = machine.Pin(16)
angle_servo = Servo(angle_pin)

az_start = 20
az_end = 160
az_sleep = .1
start_angle = 85

location = (-27.2846602, 153.0148983)

def rest_servos():
    az_servo.write_angle(90)
    angle_servo.write_angle(1)
    time.sleep(5)
    
    
sp = SunPosition(location)

rest_servos()

time.localtime()
abc = time.localtime()
abc = abc[:6]
list(abc)

cde = [-8]
abc = list(abc) + list(cde)

when = (abc)
elevation = sp.getElevation(when)
print(elevation)



# while az_start <= az_end:
#     az_servo.write_angle(az_start)
#     if az_start <= 90:
#         angle = int(((az_start / 90) * 5) + start_angle)
#     if az_start > 90:
#         angle = int(((az_start / 90) * 5) - start_angle)
#     print(angle)        
# #     angle_servo.write_angle(angle)
#     time.sleep(az_sleep)
#     az_start += 1
# rest_servos()

