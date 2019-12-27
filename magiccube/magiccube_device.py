#!/usr/bin/env python3

import ev3dev.ev3 as ev3
from time import sleep

#  Connect motors on output ports
motor_a = ev3.Motor(ev3.OUTPUT_A)
assert motor_a.connected

motor_b = ev3.Motor(ev3.OUTPUT_B)
assert motor_b.connected

btn = ev3.Button()

# Connect color sensors
#cs = ColorSensor()
#assert cs.connected

fNoColor = 0
fBlack = 1
fBlue = 2
fGreen = 3
fYellow = 4
fRed = 5
fWhite = 6
fBrown = 7

print('Robot Starting')
ev3.Sound.speak('Okay folks... Let us solve the cube!').wait()

# We will need to check EV3 buttons state
btn = ev3.Button()

# 'R' turn right side clockwise
# 'L' turn left side clockwise
# 'F' turn front side clockwise
# 'B' turn back side clockwise
# 'U' turn up side clockwise
# 'D' turn down clockwise
# lower case letter means counter clockwise turn

print('Motor start turning...')
motor_a.run_to_rel_pos(position_sp=300, speed_sp=200)
while motor_a.is_running: sleep(0.1)
sleep(1)

motor_a.run_to_rel_pos(position_sp=-30, speed_sp=200)
while motor_a.is_running: sleep(0.1)
sleep(1)

motor_b.run_to_rel_pos(position_sp=120, speed_sp=200)
while motor_b.is_running: sleep(0.1)
sleep(1)

motor_b.run_to_rel_pos(position_sp=-120, speed_sp=150)
while motor_b.is_running: sleep(0.1)
sleep(1)

ev3.Sound.speak('Cube is solved!').wait()
