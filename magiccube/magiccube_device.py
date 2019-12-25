#!/usr/bin/env python3

from time import sleep
from random import choice, randint

from ev3dev.auto import *
import ev3dev.ev3 as ev3  # OKO fuer die Sound Funktion

#  Connect two large motors on output ports B and C:
motors = [LargeMotor(address) for address in (OUTPUT_B, OUTPUT_C)]

# Every device in ev3dev has `connected` property. Use it to check that the
# device has actually been connected.
assert all([m.connected for m in motors]), \
    "Two large motors should be connected to ports B and C"

# Connect infrared and touch sensors.
#ir = InfraredSensor();  assert ir.connected
#us = UltrasonicSensor(); assert us.connected
#ts = TouchSensor(); assert ts.connected
cs = ColorSensor(); assert cs.connected


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
btn = Button()


def start():
