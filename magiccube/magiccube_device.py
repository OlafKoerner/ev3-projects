#!/usr/bin/env python3

import ev3dev.ev3 as ev3

#  Connect motors on output ports
motor_a = ev3.ServoMotor(ev3.OUTPUT_A)
#assert motor_a.connected

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


def main():
    # 'R' turn right side clockwise
    # 'L' turn left side clockwise
    # 'F' turn front side clockwise
    # 'B' turn back side clockwise
    # 'U' turn up side clockwise
    # 'D' turn down clockwise
    # lower case letter means counter clockwise turn

    command_string = "Uu"

    motor_a.run(position_sp=100)
