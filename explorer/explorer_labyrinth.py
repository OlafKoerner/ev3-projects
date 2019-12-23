#!/usr/bin/env python3

from time import sleep
from random import choice, randint

from ev3dev.auto import *
import ev3dev.ev3 as ev3  # OKO fuer die Sound Funktion

#  Connect two large motors on output ports B and C:
motors = [LargeMotor(address) for address in (OUTPUT_B, OUTPUT_C)]
us_motor = MediumMotor(OUTPUT_A); assert us_motor.connected

# Every device in ev3dev has `connected` property. Use it to check that the
# device has actually been connected.
assert all([m.connected for m in motors]), \
    "Two large motors should be connected to ports B and C"

# Connect infrared and touch sensors.
#ir = InfraredSensor(); assert ir.connected
us = UltrasonicSensor(); assert us.connected
ts = TouchSensor(); assert ts.connected
cs = ColorSensor(); assert cs.connected


fNoColor = 0
fBlack = 1
fBlue = 2
fGreen = 3
fYellow = 4
fRed = 5
fWhite = 6
fBrown = 7
LetzteFarbe = 0
WegMerkenListe = []

print('Robot Starting')
ev3.Sound.speak('Okay folks. Let us go for a ride!').wait()

# We will need to check EV3 buttons state.
btn = Button()


def start():
    """
    Start both motors. `run-direct` command will allow to vary motor
    performance on the fly by adjusting `duty_cycle_sp` attribute.
    """
    for m in motors:
        m.run_direct()


def backup():
    """
    Back away from an obstacle.
    """

    # Sound backup alarm.
    #Sound.tone([(1000, 500, 500)] * 3)

    # Turn backup lights on:
    for light in (Leds.LEFT, Leds.RIGHT):
        Leds.set_color(light, Leds.RED)

    # Stop both motors and reverse for 1.5 seconds.
    # `run-timed` command will return immediately, so we will have to wait
    # until both motors are stopped before continuing.
    for m in motors:
        m.stop(stop_action='brake')
        m.run_timed(speed_sp=-500, time_sp=1500)

    WegMerkenListe.append('backup')
    #ev3.Sound.speak('Geh mir aus dem Weg!').wait()

    # When motor is stopped, its `state` attribute returns empty list.
    # Wait until both motors are stopped:
    while any(m.state for m in motors):
        sleep(0.1)

    # Turn backup lights off:
    for light in (Leds.LEFT, Leds.RIGHT):
        Leds.set_color(light, Leds.GREEN)


def turn():
    """
    Turn the robot in random direction.
    """

    # We want to turn the robot wheels in opposite directions from 1/4 to 3/4
    # of a second. Use `random.choice()` to decide which wheel will turn which
    # way.
    power = choice([(750, -750), (-750, 750)])
    t = randint(250, 750)

    WegMerkenListe.append([power, t]) #OKO: Merke die Zufallszahlen und schreibe an Ende der Liste

    for m, p in zip(motors, power):
        m.run_timed(speed_sp = p, time_sp = t)

    # Wait until both motors are stopped:
    while any(m.state for m in motors):
        sleep(0.1)


def lenkelinks():
    print('turn left')
    power = (-300, 300)
    t = 200

    WegMerkenListe.append([power, t])

    for m, p in zip(motors, power):
        m.stop(stop_action='brake')
        m.run_timed(speed_sp = p, time_sp = t)

    # Wait until both motors are stopped:
    while any(m.state for m in motors):
        sleep(0.1)


def lenkerechts():
    print('turn right')
    power = (300, -300)
    t = 200

    WegMerkenListe.append([power, t])

    for m, p in zip(motors, power):
        m.stop(stop_action='brake')
        m.run_timed(speed_sp = p, time_sp = t)

    # Wait until both motors are stopped:
    while any(m.state for m in motors):
        sleep(0.1)

def start_us_scan():
    global us_motor_zeropos
    us_motor_zeropos = us_motor.position
    global dist_dict
    dist_dict = {0 : us.distance_centimeters}
    global us_motor_degree_max
    us_motor_degree_max = 60
    global us_motor_degree_adder
    us_motor_degree_adder = us_motor_degree_max / 3
    global us_motor_degree
    us_motor_degree = us_motor_degree_adder
    global us_motor_speed
    us_motor_speed = 50
    us_motor.run_to_abs_pos(speed_sp=us_motor_speed, position_sp=us_motor_degree, stop_action='hold')

# Run the robot until a button is pressed.
start()
start_us_scan()
while not btn.any():

    #turn ultra sonic sensor left/right
    if us_motor.position - us_motor_zeropos > us_motor_degree_max :
        us_motor_degree_adder = -us_motor_degree_adder
        us_motor_degree_max = -us_motor_degree_max
    if abs(us_motor.position - us_motor_zeropos - us_motor_degree) < 5 :
        us_motor_degree = us_motor_degree + us_motor_degree_adder
        us_motor.run_to_abs_pos(speed_sp=us_motor_speed, position_sp=us_motor_degree, stop_action='hold')
        #save us distance in dict
        dist_dict[us_motor_degree] = us.distance_centimeters
        for key in dist_dict : sys.stdout.write(str(dist_dict[key]));
        print('')

    if ts.is_pressed:
        # We bumped an obstacle.
        # Back away, turn and go in other direction.
        backup()
        turn()
        start()

    dc = 0

    """
    # Infrared sensor in proximity  mode will measure distance to the closest
    # object in front of it.
    #distance = ir.proximity

    if distance < 60:
        turn()
        start()

    if distance > 75:  # OKO sonst 60
        # Path is clear, run at full speed.
        dc = 30  # OKO sonst 95
    else:
        # Obstacle ahead, slow down.
        dc = 30  # OKO sonst 30

    if cs.color == fRed:
        print('red')
        lenkelinks()
        start()
    elif cs.color == fBlue:
        print('blue')
        lenkerechts()
        start()
    elif LetzteFarbe == fRed:
        lenkelinks()
        LetzteFarbe = fNoColor
        start()
    elif LetzteFarbe == fBlue:
        lenkerechts()
        LetzteFarbe = fNoColor
        start() """
    for m in motors:
        m.duty_cycle_sp = dc

    sleep(0.1)

    WegMerkenListe.append('fahren')

# Stop the motors before exiting.
for m in motors:
    m.stop()

us_motor.stop(stop_action='coast')

"""
ev3.Sound.speak('Now I want back home!').wait()
#print(WegMerkenListe)
# OKO: Finde den Weg zurueck...
for Wert in reversed(WegMerkenListe):
    if Wert == 'fahren':
        for m in motors:
            m.duty_cycle_sp = -dc
            start()
    elif Wert == 'backup':
        for m in motors:
            m.stop(stop_action='brake')
            m.run_timed(speed_sp=500, time_sp=1500)

        while any(m.state for m in motors):
            sleep(0.1)
    else:
        for m, p in zip(motors, Wert[0]):
            m.run_timed(speed_sp=-p, time_sp=Wert[1])
            #print(-p)
            #print(Wert[1])

        # Wait until both motors are stopped:
        while any(m.state for m in motors):
            sleep(0.1)

    sleep(0.1)


# Stop the motors before exiting.
for m in motors:
    m.stop()


ev3.Sound.speak('Fenja is the champion!').wait()
sleep(1)
"""