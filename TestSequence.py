import Motor as motor
import time

def motor2UpDown():
    motor.moveMotor2(True)
    time.sleep(1)
    motor.stopMotor2()
    time.sleep(1)
    motor.moveMotor2(False)
    time.sleep(1)
    motor.stopMotor2()
    time.sleep(1)
    motor.moveMotor2(False)
    time.sleep(1)
    motor.stopMotor2()
    time.sleep(1)
    motor.moveMotor2(True)
    time.sleep(1)
    motor.stopMotor2()
    time.sleep(1)

def motor1Rotate(angle: float, direction: bool):
    rotateTime = 1.5 / 90 * angle
    motor.moveMotor1(direction)
    time.sleep(rotateTime)
    motor.stopMotor1()
    time.sleep(1)

print("Starting sequence!")

motor2UpDown()
motor1Rotate(90, True)
motor2UpDown()
motor1Rotate(45, False)
motor2UpDown()
motor1Rotate(45, False)


motor.exit()