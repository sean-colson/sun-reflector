from machine import Pin, Timer
from neopixel import NeoPixel
import time
from math import sqrt
import uasyncio as asyncio

# Colors
RED = (25, 0, 0)
DARK_GREEN = (0, 37, 0)
GREEN = (0, 25, 0)
LIGHT_GREEN = (0, 12, 0)
BLUE = (0, 0, 25)
LIGHT_BLUE = (0, 0, 12)
WHITE = (25, 25, 25)
PURPLE = (25, 0, 25)
AMBER = (25, 19, 0)
CLEAR = (0, 0, 0)

# Intervals
ARROW_FLASH = 1

# Phases
BASE_STATE = "green"
BASE_STATES = {
    "green": "transition",
    "transition": "amber",
    "amber": "red",
    "red": "green"
}
ARROW_STATE = "amber"
ARROW_STATES = {
    "amber": "green",
    "green": "amber"
}
# Configure these values based on your setup
ROWS = 16
COLS = 16
NUM_LEDS = ROWS * COLS # 16x16 matrix = 256 LEDs
CENTER_ROW = (ROWS - 1) / 2
CENTER_COL = (COLS - 1) / 2
RADIUS = 8
PIN = 2  # GPIO pin connected to the NeoPixel data line

# Create a NeoPixel object
np = NeoPixel(Pin(PIN), NUM_LEDS)

def get_index(row, col):
    index = (row * COLS)
    if (row % 2 == 0):
        index += 15 - col
    else:
        index += col;    
#    print(row, col, index)
    return index

# function to display full panel 
def full_robot(RGB):
    data = [(0, 0, 0)] * NUM_LEDS
    for row in range(ROWS):
        for col in range(COLS): 
            distance = sqrt((col - CENTER_COL) ** 2 + (row - CENTER_ROW) ** 2)
            if distance <= RADIUS:
                data[get_index(row, col)] = RGB
    return data

# function to dispay right arrow
def right_arrow(data, arrow_col, RGB):
    for col in range(8, 16):
        data[get_index(6, col)] = CLEAR
    data[get_index(6, arrow_col)] = RGB
    data[get_index(6, arrow_col + 1)] = RGB
    for col in range(8, 16):
        data[get_index(7, col)] = RGB
    for col in range(8, 16):
        data[get_index(8, col)] = RGB       
    for col in range(8, 16):
        data[get_index(9, col)] = CLEAR
    data[get_index(9, arrow_col)] = RGB
    data[get_index(9, arrow_col + 1)] = RGB
    return data
    
def right_arrow_rotate(data, RGB):
    current = 0
    for col in range(8, 16):
        if data[get_index(6, col)] == RGB:
            current = col
    print(current)        
    data[get_index(6, current)] == CLEAR            
    data[get_index(6, current + 1)] == CLEAR
    if (current >= 14):
        current = 8
    else:
        current = current + 2
    print(current);    
    data[get_index(6, current)] == RGB            
    data[get_index(6, current + 1)] == RGB
    return data

# Function to update the panel
def update_panel(data):
    for i in range(NUM_LEDS):
        np[i] = data[i]
    np.write()

def clear_panel():
    data = [CLEAR] * NUM_LEDS  # Initialize all LEDs to black
    update_panel(data)
    return data
    
# 1. Create a list to hold the color data for each LED
# 2. Set the color of some LEDs
# data[0] = (255, 0, 0)  # First LED to red
# data[15] = (0, 255, 0)  # Sixteenth LED to green
# data[255] = (0, 0, 255)  # Last LED to blue

# 3. Update the panel

# robot = full_robot(RED)
# robot = right_arrow(robot, 13, GREEN)
# update_panel(robot)
# for count in range(12):
#     robot = right_arrow_rotate(robot, GREEN)
#     update_panel(robot)
#     time.sleep(1)
# time.sleep(1)
# robot = full_robot(AMBER)
# update_panel(robot)
# time.sleep(1)
# robot = full_robot(GREEN)
# update_panel(robot)
# time.sleep(1)
# input()
# robot = full_robot(CLEAR)
# update_panel(robot)
# time.sleep(1)
# for count in range(20):    
#     robot = right_arrow(robot, 13, LIGHT_GREEN)
#     update_panel(robot)
#     time.sleep(ARROW_FLASH)
#     robot = right_arrow(robot, 13, GREEN)
#     update_panel(robot)
#     time.sleep(ARROW_FLASH)
# robot[get_index(0, 0)] = (255, 255, 255)
# robot[get_index(1, 7)] = (0, 0, 255)
# robot[get_index(2, 8)] = (255, 0, 255)
# update_panel(robot)
# time.sleep(1)
#update_panel(right_arrow(robot, 0, int(255*.10), 0))
#time.sleep(5)
# update_panel(full_robot(0, int(255*.10), 0))
# time.sleep(10)
# update_panel(full_robot(0, 0, 0))

# 4. (Optional) Create animations or patterns
#    - Modify the 'data' list based on your desired pattern.
#    - Call 'update_panel(data)' repeatedly with updated data.
def reset_arrow_state():
    global ARROW_STATE
    print("reset")
    ARROW_STATE = None
    
async def arrow_state_machine(robot):
    global ARROW_STATE
    count = 0
    while ARROW_STATE and count < 10:
       print(f"Arrow state: {ARROW_STATE}")
       count += 1
       if ARROW_STATE == "amber":
           robot = right_arrow(robot, 13, AMBER)
           update_panel(robot)
           await asyncio.sleep(ARROW_FLASH)
       elif ARROW_STATE == "green":
           robot = right_arrow(robot, 13, CLEAR)
           update_panel(robot)
           await asyncio.sleep(ARROW_FLASH)
       ARROW_STATE = ARROW_STATES[ARROW_STATE]
       
async def transition(robot):
    print("transition")
    row = 15
    while row > 0:
        for col in range(COLS):
            index = get_index(row, col)
            if robot[index] == GREEN:
                robot[index] = AMBER
        update_panel(robot);
        await asyncio.sleep(.1)
        row -= 1;
    
async def robot_state_machine():
    global BASE_STATE
    robot = clear_panel();
    while BASE_STATE:
        print(f"Base state: {BASE_STATE}")
        # Perform state-specific actions
        if BASE_STATE == "green":
            print("Green...")
            robot = full_robot(GREEN)
            robot = right_arrow(robot, 13, GREEN)
            update_panel(robot)
            await arrow_state_machine(robot)
        elif BASE_STATE == "transition":
            await transition(robot);
        elif BASE_STATE == "amber":
            robot = full_robot(AMBER)
            update_panel(robot)
            print("Amber...")
            await asyncio.sleep(1)
        elif BASE_STATE == "red":
            robot = full_robot(RED)
            update_panel(robot)
            print("Red...")
            await asyncio.sleep(3)
        # Transition to the next state
        BASE_STATE = BASE_STATES[BASE_STATE]
        
async def main():
   await robot_state_machine()
   
asyncio.run(main())