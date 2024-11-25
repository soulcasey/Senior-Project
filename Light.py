import RPi.GPIO as GPIO
import time
import threading

# Define GPIO pins for the lights
camera_light = 35
warning_light = 37

is_camera_light_on = False
is_warning_light_on = False

# Global variable to store the blinking thread and stop event
blinkThread = None

# Initialize GPIO in BOARD mode
if GPIO.getmode() != GPIO.BOARD:
    GPIO.setmode(GPIO.BOARD)

# Setup GPIO pins as output
GPIO.setup(camera_light, GPIO.OUT)
GPIO.setup(warning_light, GPIO.OUT)

# Control functions for individual lights
def cameraLight(isOn: bool):
    global is_camera_light_on
    is_camera_light_on = isOn

    GPIO.output(camera_light, isOn)

def warningLight(isOn: bool):
    global is_warning_light_on
    is_warning_light_on = isOn

    GPIO.output(warning_light, isOn)

# Blinking function for the warning light
def blink(stop_event: threading.Event):
    while not stop_event.is_set():
        warningLight(True)
        time.sleep(0.5)  
        warningLight(False)
        time.sleep(0.5) 

# Start blinking the warning light
def startBlink():
    global blinkThread
    if isBlinking():
        print("Warning light is already blinking")
        return

    stop_event = threading.Event()
    thread = threading.Thread(target=blink, args=(stop_event,))
    blinkThread = thread
    thread.start()
    print("Warning light blinking started.")

# Stop blinking the warning light
def stopBlink():
    global blinkThread
    if isBlinking() is False:
        print("Warning light is not blinking.")
        return
    
    stop_event = blinkThread._args[0]  # Get the stop_event from the thread
    stop_event.set()  # Signal the thread to stop
    blinkThread.join()  # Wait for the thread to finish
    blinkThread = None  # Reset the thread

    warningLight(False)
    print("Warning light blinking stopped.")

# Stop blinking the warning light
def isBlinking():
    return blinkThread is not None