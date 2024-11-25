import Motor as motor
import time

motor.moveMotor1(True)
time.sleep(1.5)
motor.moveMotor1(False)
time.sleep(1.5)
motor.moveMotor1(False)
time.sleep(1.5)
motor.moveMotor1(True)
time.sleep(3)
motor.moveMotor1(False)
time.sleep(1.5)