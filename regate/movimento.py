from pybricks.tools import wait


class Movimento:

    def __init__(self, robot):

        self.robot = robot

    # ------------------------

    def andar_1_celula(self):

        self.robot.reset()

        self.robot.drive(150, 0)

        while self.robot.left_motor.angle() < 360:
            pass

        self.robot.stop()

    # ------------------------

    def virar_90(self, direita=True):

        if direita:
            self.robot.turn(90)
        else:
            self.robot.turn(-90)

        wait(200)