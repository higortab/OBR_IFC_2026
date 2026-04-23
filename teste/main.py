#!/usr/bin/env pybricks-micropython
from pybricks.ev3devices import ColorSensor, Motor
from pybricks.parameters import Port
from pybricks.tools import wait
from pybricks.robotics import DriveBase
from pybricks.hubs import EV3Brick
from musicas.mario import mario

ev3 = EV3Brick() 

left_motor = Motor(Port.B)
right_motor = Motor(Port.C)

robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=104)

while True:
    robot.straight(100)
    ev3.speaker.beep()

    robot.straight(-100)
    ev3.speaker.beep()
