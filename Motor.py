import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

speed = 40

# Horizontal Motor
GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
hMotor = GPIO.PWM(11, 1000)

# Vertical Motor
GPIO.setup(16, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
vMotor = GPIO.PWM(22, 1000)

def moveHMotor(forward: bool):
    GPIO.output(13, forward)
    GPIO.output(15, forward == False)
    hMotor.ChangeDutyCycle(speed)

def moveVMotor(forward: bool):
    GPIO.output(16, forward)
    GPIO.output(18, forward == False)
    vMotor.ChangeDutyCycle(speed)

def stopMotor():
    GPIO.output(13, False)
    GPIO.output(15, False)
    GPIO.output(16, False)
    GPIO.output(18, False)
    hMotor.ChangeDutyCycle(0)
    vMotor.ChangeDutyCycle(0)