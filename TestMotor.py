import Motor as motor
import time

try:
    motor.moveMotor2(True)
    time.sleep(6.6)
    motor.stopMotor2()
    time.sleep(2)
    motor.moveMotor2(False)
    time.sleep(6.6)
    motor.stopMotor2()
    time.sleep(2)

except Exception as e:
    motor.stopAllMotors()
finally:
    motor.exit()
