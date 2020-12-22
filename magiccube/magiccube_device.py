#!/usr/bin/env python3

import ev3dev.ev3 as ev3
from time import sleep

MOT_RUNNING_WAIT_SECS = 0.1
MOT_INERTIA_WAIT_SECS = 1.0

# connect motors to output ports
from magiccube_main import RUN_ON_EV3

if RUN_ON_EV3:
    motor_a = ev3.Motor(ev3.OUTPUT_A)
    assert motor_a.connected
    if motor_a.connected: motor_a_null_pos = motor_a.position

    motor_b = ev3.Motor(ev3.OUTPUT_B)
    assert motor_b.connected
    if motor_b.connected: motor_b_null_pos = motor_b.position

    motor_c = ev3.Motor(ev3.OUTPUT_C)
    #assert motor_c.connected
    if motor_c.connected: motor_c_null_pos = motor_c.position

# definition of motor moves
def rot(x):
    if RUN_ON_EV3:
        if motor_b.connected:
            motor_b.run_to_rel_pos(position_sp= -360 * 3 * x - 60.5 * x / abs(x), speed_sp=200, stop_action='hold')
            while motor_b.is_running: sleep(MOT_RUNNING_WAIT_SECS)
            sleep(MOT_INERTIA_WAIT_SECS)
            motor_b.run_to_rel_pos(position_sp= +60.5 * x / abs(x), speed_sp=200, stop_action='hold')
            while motor_b.is_running: sleep(MOT_RUNNING_WAIT_SECS)
            sleep(MOT_INERTIA_WAIT_SECS)

def rot_free(x):
    if RUN_ON_EV3:
        if motor_b.connected:
            motor_b.run_to_rel_pos(position_sp=-360 * 3 * x, speed_sp=200, stop_action='hold')
            while motor_b.is_running: sleep(MOT_RUNNING_WAIT_SECS)
            sleep(MOT_INERTIA_WAIT_SECS)
def down():
    if RUN_ON_EV3:
        if motor_a.connected:
            motor_a.run_to_abs_pos(position_sp=motor_a_null_pos, speed_sp=200, stop_action='hold')
            while motor_a.is_running:
                sleep(MOT_RUNNING_WAIT_SECS)

def flip():
    if RUN_ON_EV3:
        if motor_a.connected:
            motor_a.run_to_abs_pos(position_sp=motor_a_null_pos+120, speed_sp=200, stop_action='hold')
            while motor_a.is_running:
                sleep(MOT_RUNNING_WAIT_SECS)
            sleep(MOT_INERTIA_WAIT_SECS)
            motor_a.run_to_abs_pos(position_sp=motor_a_null_pos, speed_sp=200, stop_action='hold')
            while motor_a.is_running:
                sleep(MOT_RUNNING_WAIT_SECS)
            sleep(MOT_INERTIA_WAIT_SECS)

def up():
    if RUN_ON_EV3:
        if motor_a.connected:
            motor_a.run_to_abs_pos(position_sp=motor_a_null_pos-100, speed_sp=200, stop_action='hold')
            while motor_a.is_running:
                sleep(MOT_RUNNING_WAIT_SECS)

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
    rot_free(-0.25)
    down()
    flip()
    rot(0.25)
    flip()
    up()
    rot_free(-0.25)
    flip()
    flip()

def turn_r():
    up()
    rot_free(-0.25)
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
    rot_free(0.25)
    down()
    flip()
    rot(0.25)
    flip()
    flip()
    flip()
    up()
    rot_free(-0.25)

def turn_l():
    up()
    rot_free(0.25)
    down()
    flip()
    rot(-0.25)
    flip()
    flip()
    flip()
    up()
    rot_free(-0.25)

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
    rot_free(-0.25)

def turn_c():
    up()
    rot_free(0.25)


def turn_test():
    num_loop = 20

    for i in range(num_loop):
        turn_D()
        flip()

    for i in range(num_loop):
        flip()
        flip()
        flip()
        turn_d()

def read_stone_colors():
    stone_colors_of_side = {}
    stone_colors_of_side['y'] = ['y', 'y', 'y', 'y', 'y', 'y', 'y', 'y']
    stone_colors_of_side['g'] = ['g', 'g', 'g', 'g', 'g', 'g', 'g', 'g']
    stone_colors_of_side['r'] = ['r', 'r', 'r', 'r', 'r', 'r', 'r', 'r']
    stone_colors_of_side['b'] = ['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b']
    stone_colors_of_side['c'] = ['c', 'c', 'c', 'c', 'c', 'c', 'c', 'c']
    stone_colors_of_side['w'] = ['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w']
    return stone_colors_of_side

def main(args):
    #btn = ev3.Button()

    # Connect color sensors
    #cs = ev3.ColorSensor(ev3.INPUT_1)
#    assert cs.connected

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
    if RUN_ON_EV3:
        ev3.Sound.speak('Okay cube!').wait()
        print('Motor start turning...')


    #rot(0.25)
    #up()

    if RUN_ON_EV3:
        motor_a.stop(stop_action="coast")
        motor_b.stop(stop_action="coast")
        motor_c.stop(stop_action="coast")

        while 1:
            print('postion motor c: ', motor_c.position - motor_c_null_pos)
            print('color: ', cs.red, ' ', cs.green, ' ', cs.blue)


        motor_a.stop(stop_action="coast")
        motor_b.stop(stop_action="coast")
        motor_c.stop(stop_action="coast")

   # ev3.Sound.speak('Cube is solved!').wait()
