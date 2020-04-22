#!/usr/bin/env python3

import ev3dev.ev3 as ev3
from time import sleep

# connect motors to output ports
motor_a = ev3.Motor(ev3.OUTPUT_A)
# assert motor_a.connected

motor_b = ev3.Motor(ev3.OUTPUT_B)


# assert motor_b.connected

# definition of motor moves
def down():
    print('down')
    print('first position: ', motor_a.position)
    motor_a.run_to_abs_pos(position=motor_a_null_pos+120, speed_sp=200, stop_action='hold')
    while motor_a.is_running:
        print('position: ', motor_a.position, '   position_sp: ', motor_a.position_sp)
        sleep(0.1)
    sleep(1)


def flip():
    print('flip')
    motor_a.run_to_abs_pos(position=motor_a_null_pos+120, speed_sp=200, stop_action='hold')
    while motor_a.is_running: sleep(0.1)
    sleep(1)
    motor_a.run_to_abs_pos(position=motor_a_null_pos-120, speed_sp=200, stop_action='hold')
    while motor_a.is_running: sleep(0.1)
    sleep(5)


def rot(x):
    motor_b.run_to_abs_pos(position=motor_b_null_pos-1120 * x, speed_sp=200, stop_action='hold')
    while motor_b.is_running: sleep(0.1)
    sleep(1)
    motor_b.run_to_abs_pos(position=motor_b_null_pos+30 * x / abs(x), speed_sp=200, stop_action='hold')
    while motor_b.is_running: sleep(0.1)
    sleep(1)


def up():
    print('up')
    print('first position: ', motor_a.position)
    motor_a.run_to_abs_pos(position=motor_a_null_pos-120, speed_sp=200, stop_action='hold')
    while motor_a.is_running:
        print('position: ', motor_a.position, '   position_sp: ', motor_a.position_sp)
        sleep(0.1)
    sleep(5)


# definition of turns
def turn_R():
    rot(0.25)
    down()
    flip()
    rot(0.25)
    flip()
    up()
    rot(0.25)


def turn_r():
    rot(0.25)
    down()
    flip()
    rot(-0.25)
    flip()
    up()
    rot(0.25)


def turn_L():
    rot(-0.25)
    down()
    flip()
    rot(0.25)
    flip()
    up()
    rot(-0.25)


def turn_l():
    rot(-0.25)
    down()
    flip()
    rot(-0.25)
    flip()
    up()
    rot(-0.25)


def turn_F():
    rot(0.5)
    down()
    flip()
    rot(0.25)
    flip()
    up()


def turn_f():
    rot(0.5)
    down()
    flip()
    rot(-0.25)
    flip()
    up()


def turn_B():
    down()
    flip()
    rot(0.25)
    flip()
    up()
    rot(0.5)


def turn_b():
    down()
    flip()
    rot(-0.25)
    flip()
    up()
    rot(0.5)


def turn_U():
    down()
    flip()
    flip()
    rot(0.25)
    flip()
    flip()
    up()


def turn_u():
    down()
    flip()
    flip()
    rot(-0.25)
    flip()
    flip()
    up()


def turn_D():
    down()
    rot(0.25)
    up()


def turn_d():
    down()
    rot(-0.25)
    up()

    # 'R' turn right side clockwise
    # 'L' turn left side clockwise
    # 'F' turn front side clockwise
    # 'B' turn back side clockwise
    # 'U' turn up side clockwise
    # 'D' turn down clockwise
    # lower case letter means counter clockwise turn


"""
switcher = {
    'R': turn_R(),
    'r': turn_r(),
    'L': turn_L(),
    'l': turn_l(),
    'F': turn_F(),
    'f': turn_f(),
    'B': turn_B(),
    'b': turn_b(),
    'U': turn_U(),
    'u': turn_u(),
    'D': turn_D(),
    'd': turn_d()
}
"""


def turn_sides(cmd):
    for chr in cmd:
        func = switcher.get(chr)
        func()


def main(args):
    btn = ev3.Button()

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
    ev3.Sound.speak('Okay folks... Let us solve the cube!').wait()
    print('Motor start turning...')

    motor_a_null_pos = motor_a.position
    motor_b_null_pos = motor_b.position

    # turn_side('DdRrUu')
    # turn_D()
    # turn_d()
    # turn_R()
    # turn_r()
    # turn_U()
    # turn_u()

    down()
    up()
    down()
    flip()
    up()


    # for cmd in args:
    #   turn_side(cmd)

    motor_a.stop(stop_action="coast")
    motor_b.stop(stop_action="coast")

    ev3.Sound.speak('Cube is solved!').wait()
