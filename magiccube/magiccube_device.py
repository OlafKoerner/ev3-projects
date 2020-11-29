#!/usr/bin/env python3

import ev3dev.ev3 as ev3
from time import sleep

# connect motors to output ports
motor_a = ev3.Motor(ev3.OUTPUT_A)
#assert motor_a.connected
if motor_a.connected: motor_a_null_pos = motor_a.position

motor_b = ev3.Motor(ev3.OUTPUT_B)
#assert motor_b.connected
if motor_b.connected: motor_b_null_pos = motor_b.position

# definition of motor moves
def down():
    if motor_a.connected:
        motor_a.run_to_abs_pos(position_sp=motor_a_null_pos, speed_sp=200, stop_action='hold')
        while motor_a.is_running:
            sleep(0.1)

def flip():
    if motor_a.connected:
        motor_a.run_to_abs_pos(position_sp=motor_a_null_pos+100, speed_sp=200, stop_action='hold')
        while motor_a.is_running:
            sleep(0.1)
        motor_a.run_to_abs_pos(position_sp=motor_a_null_pos, speed_sp=200, stop_action='hold')
        while motor_a.is_running:
            sleep(0.1)

def rot(x):
    if motor_b.connected:
        motor_b.run_to_rel_pos(position_sp=-1082 * x, speed_sp=200, stop_action='hold')
        while motor_b.is_running: sleep(0.1)
        motor_b.run_to_rel_pos(position_sp=-65 * x / abs(x), speed_sp=200, stop_action='hold')
        while motor_b.is_running: sleep(0.1)
        motor_b.run_to_rel_pos(position_sp=+65 * x / abs(x), speed_sp=200, stop_action='hold')
        while motor_b.is_running: sleep(0.1)

def up():
    if motor_a.connected:
        motor_a.run_to_abs_pos(position_sp=motor_a_null_pos-100, speed_sp=200, stop_action='hold')
        while motor_a.is_running:
            sleep(0.1)

# definition of turns
# 'R' turn right side clockwise
# 'L' turn left side clockwise
# 'F' turn front side clockwise
# 'B' turn back side clockwise
# 'U' turn up side clockwise
# 'D' turn down clockwise
# lower case letter means counter clockwise turn
def turn_R():
    up()
    rot(-0.25)
    down()
    flip()
    rot(0.25)
    flip()
    up()
    rot(-0.25)
    flip()
    flip()

def turn_r():
    up()
    rot(-0.25)
    down()
    flip()
    rot(-0.25)
    flip()
    up()
    rot(-0.25)
    flip()
    flip()

def turn_L():
    up()
    rot(0.25)
    down()
    flip()
    rot(0.25)
    flip()
    flip()
    flip()
    up()
    rot(-0.25)


def turn_l():
    up()
    rot(0.25)
    down()
    flip()
    rot(-0.25)
    flip()
    flip()
    flip()
    up()
    rot(-0.25)


def turn_F():
    down()
    flip()
    rot(0.25)
    flip()
    flip()
    flip()


def turn_f():
    down()
    flip()
    rot(-0.25)
    flip()
    flip()
    flip()


def turn_B():
    down()
    flip()
    flip()
    flip()
    rot(0.25)
    flip()


def turn_b():
    down()
    flip()
    flip()
    flip()
    rot(-0.25)
    flip()


def turn_U():
    down()
    flip()
    flip()
    rot(0.25)
    flip()
    flip()


def turn_u():
    down()
    flip()
    flip()
    rot(-0.25)
    flip()
    flip()

def turn_D():
    down()
    rot(0.25)

def turn_d():
    down()
    rot(-0.25)

def turn_C():
    up()
    rot(0.25)

def turn_c():
    up()
    rot(-0.25)


def main(args):
    #btn = ev3.Button()

    # Connect color sensors
    # cs = ColorSensor()
    # assert cs.connected
    
   
    fNoColor = 0
    fBlack = 1
    fBlue = 2
    fGreen = 3
    fYellow = 4
    fRed = 5
    fWhite = 6
    fBrown = 7

    print('Robot Starting')
    #ev3.Sound.speak('Okay folks... Let us solve the cube!').wait()
    ev3.Sound.speak('Okay cube!').wait()
    print('Motor start turning...')


    rot(0.25)


    motor_a.stop(stop_action="coast")
    motor_b.stop(stop_action="coast")

   # ev3.Sound.speak('Cube is solved!').wait()
