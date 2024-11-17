import RPi.GPIO as GPIO

if GPIO.getmode() != GPIO.BOARD:
    GPIO.setmode(GPIO.BOARD)

speed = 40

class Motor:
    def __init__(self, pwm_pin, dir_pin1, dir_pin2):
        self.pwm_pin = pwm_pin
        self.dir_pin1 = dir_pin1
        self.dir_pin2 = dir_pin2
        GPIO.setup(self.pwm_pin, GPIO.OUT)
        GPIO.setup(self.dir_pin1, GPIO.OUT)
        GPIO.setup(self.dir_pin2, GPIO.OUT)
        self.motor = GPIO.PWM(self.pwm_pin, 1000)

    def move(self, forward: bool):
        GPIO.output(self.dir_pin1, forward)
        GPIO.output(self.dir_pin2, not forward)
        self.motor.ChangeDutyCycle(speed)

    def stop(self):
        GPIO.output(self.dir_pin1, False)
        GPIO.output(self.dir_pin2, False)
        self.motor.ChangeDutyCycle(0)
        
motor_1 = Motor(pwm_pin=11, dir_pin1=13, dir_pin2=15)
motor_2 = Motor(pwm_pin=22, dir_pin1=16, dir_pin2=18)
motor_3 = Motor(pwm_pin=36, dir_pin1=31, dir_pin2=29)

def moveMotor1(forward: bool):
    motor_1.move(forward)

def stopMotor1():
    motor_1.stop()

def moveMotor2(forward: bool):
    motor_2.move(forward)

def stopMotor2():
    motor_2.stop()

def moveMotor3(forward: bool):
    motor_3.move(forward)

def stopMotor3():
    motor_3.stop()
