import Motor as motor
import time

try:
    motor.moveMotor1(True)
    time.sleep(2)
    motor.stopMotor1()
    time.sleep(2)
    motor.moveMotor1(False)
    time.sleep(2)
    motor.stopMotor1()
    time.sleep(2)

    motor.moveMotor2(True)
    time.sleep(2)
    motor.stopMotor2()
    time.sleep(2)
    motor.moveMotor2(False)
    time.sleep(2)
    motor.stopMotor2()
    time.sleep(2)

    motor.moveMotor3(True)
    time.sleep(2)
    motor.stopMotor3()
    time.sleep(2)
    motor.moveMotor3(False)
    time.sleep(2)
    motor.stopMotor3()
    time.sleep(2)
except Exception as e:
    motor.stopAllMotors()
finally:
    motor.exit()
