import platform

# Check if the code is running on a Raspberry Pi or Windows
is_raspberry_pi = platform.system() == "Linux" and "raspberrypi" in platform.node().lower()

if is_raspberry_pi:
    import RPi.GPIO as GPIO

    if GPIO.getmode() != GPIO.BOARD:
        GPIO.setmode(GPIO.BOARD)

    motorCount = 0

    class Motor:
        def __init__(self, pwm_pin, dir_pin1, dir_pin2, speed):
            self.pwm_pin = pwm_pin
            self.dir_pin1 = dir_pin1
            self.dir_pin2 = dir_pin2
            self.speed = speed
            GPIO.setup(self.pwm_pin, GPIO.OUT)
            GPIO.setup(self.dir_pin1, GPIO.OUT)
            GPIO.setup(self.dir_pin2, GPIO.OUT)
            self.motor = GPIO.PWM(self.pwm_pin, 1000)
            self.motor.start(0)

            global motorCount
            motorCount += 1
            print("Motor " + str(motorCount) + " setup complete")

        def move(self, forward: bool):
            GPIO.output(self.dir_pin1, forward)
            GPIO.output(self.dir_pin2, not forward)
            self.motor.ChangeDutyCycle(self.speed)

        def stop(self):
            GPIO.output(self.dir_pin1, False)
            GPIO.output(self.dir_pin2, False)
            self.motor.ChangeDutyCycle(0)

    motor_1 = Motor(11, 13, 15, 50)
    motor_2 = Motor(22, 16, 18, 100)

    def moveMotor1(forward: bool):
        print("Motor 1 Forward") if forward else print("Motor 1 Backward")
        motor_1.move(forward)

    def stopMotor1():
        print("Motor 1 Stop")
        motor_1.stop()

    def moveMotor2(forward: bool):
        print("Motor 2 Forward") if forward else print("Motor 2 Backward")
        motor_2.move(forward)

    def stopMotor2():
        print("Motor 2 Stop")
        motor_2.stop()

else:
    # For Windows, simulate the motor behavior (no GPIO interaction)
    def moveMotor1(forward: bool):
        print("Motor 1 Forward") if forward else print("Motor 1 Backward")

    def stopMotor1():
        print("Motor 1 Stop")

    def moveMotor2(forward: bool):
        print("Motor 2 Forward") if forward else print("Motor 2 Backward")

    def stopMotor2():
        print("Motor 2 Stop")

def stopAllMotors():
    stopMotor1()
    stopMotor2()

def exit():
    GPIO.cleanup()