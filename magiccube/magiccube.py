#!/usr/bin/env python3

from time import sleep
from random import choice, randint

from ev3dev.auto import *
import ev3dev.ev3 as ev3  # OKO fuer die Sound Funktion

#  Connect two large motors on output ports A and B:
motors = [LargeMotor(address) for address in (OUTPUT_A, OUTPUT_B)]

assert all([m.connected for m in motors]), "Connect large motors to ports A and B."

#  Connect medium motor on output ports C:
us_motor = MediumMotor(OUTPUT_C)

assert us_motor.connected, "Connect medium motor to port C."

# Connect infrared and touch sensors.
cs = ColorSensor(); assert cs.connected

# We will need to check EV3 buttons state.
btn = Button()


def start():
    """
    Start both motors. `run-direct` command will allow to vary motor
    performance on the fly by adjusting `duty_cycle_sp` attribute.
    """
    for m in motors:
        m.run_direct()




start()

while not btn.any():




    for m in motors:
        m.duty_cycle_sp = dc

    sleep(0.1)

    WegMerkenListe.append('fahren')

# Stop the motors before exiting.
for m in motors:
    m.stop()

us_motor.stop(stop_action='coast')
