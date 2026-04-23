#!/usr/bin/env pybricks-micropython
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port, Color
from pybricks.robotics import DriveBase
from pybricks.tools import wait

left_motor = Motor(Port.B)
right_motor = Motor(Port.C)
sensor = ColorSensor(Port.S1)

robot = DriveBase(left_motor, right_motor, 55.5, 104)

lado = 1

while True:
    if sensor.color() != Color.BLACK:
        robot.drive(50, 20 * lado)
    else:
        robot.drive(100, 0)
        lado *= -1

    wait(10)