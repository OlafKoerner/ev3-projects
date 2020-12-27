#!/usr/bin/env python3

import ev3dev.ev3 as ev3
import operator
from time import sleep

MOT_RUNNING_WAIT_SECS = 0.1
MOT_INERTIA_WAIT_SECS = 1.0
MOT_COL_POS_CORNER  = -315
MOT_COL_POS_EDGE    = -340
MOT_COL_POS_CENTER  = -380

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
    assert motor_c.connected
    if motor_c.connected: motor_c_null_pos = motor_c.position

    # connect color sensor
    sensor_color = ev3.ColorSensor(ev3.INPUT_1)
    assert sensor_color.connected

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

def turn_Y():
    up()
    rot_free(-0.25)

def turn_y():
    up()
    rot_free(0.25)

def turn_T():
    up()
    flip()

def turn_t():
    up()
    flip()
    flip()
    flip()

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

def move_color_sensor_to_pos(pos):
    if RUN_ON_EV3:
        motor_c.run_to_abs_pos(position_sp=motor_c_null_pos + pos, speed_sp=200, stop_action='hold')
        while motor_c.is_running:
            sleep(MOT_RUNNING_WAIT_SECS)
        sleep(MOT_INERTIA_WAIT_SECS)
    return

class RGBColor:
    def __init__(self, r_mean, g_mean, b_mean, r_std, g_std, b_std):
        self.r_mean = r_mean
        self.g_mean = g_mean
        self.b_mean = b_mean
        self.r_std = r_std
        self.g_std = g_std
        self.b_std = b_std
        self.z = 0
        self.col = ''
        return

def read_color():
    #if RUN_ON_EV3:
        rgb_of_color = {}
        rgb_of_color['g'] = RGBColor( 92, 302, 304, 5, 5, 5)
        rgb_of_color['b'] = RGBColor( 45, 183, 239, 5, 5, 5)
        rgb_of_color['w'] = RGBColor(346, 413, 345, 5, 5, 5)
        rgb_of_color['r'] = RGBColor(227, 189, 121, 5, 5, 5)
        rgb_of_color['c'] = RGBColor(256, 333, 398, 5, 5, 5)
        rgb_of_color['y'] = RGBColor(276, 340, 404, 5, 5, 5)
        for col in rgb_of_color:
            rgb_of_color[col].z = (270 - rgb_of_color[col].r_mean) / rgb_of_color[col].r_std + \
                    (340 - rgb_of_color[col].g_mean) / rgb_of_color[col].g_std + \
                    (404 - rgb_of_color[col].b_mean) / rgb_of_color[col].b_std
            rgb_of_color[col].col = col
            '''
            col.z = (sensor_color.red   - col.r) / r_std + \
                    (sensor_color.green - col.g) / g_std + \
                    (sensor_color.blue  - col.b) / b_std
            '''
        result = min(rgb_of_color.values(), key=operator.attrgetter('z')).col
        return result
def main(args):
    #btn = ev3.Button()



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
