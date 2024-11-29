import platform
import time
import threading

# Define GPIO pins for the lights
camera_light = 35
warning_light = 37

is_camera_light_on = False
is_warning_light_on = False

# Global variable to store the blinking thread and stop event
blinkThread = None

# Check if the code is running on a Raspberry Pi or Windows
is_raspberry_pi = platform.system() == "Linux" and "raspberrypi" in platform.node().lower()

if is_raspberry_pi:
    import RPi.GPIO as GPIO # type: ignore

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

    if is_raspberry_pi:
        GPIO.output(camera_light, isOn)

def warningLight(isOn: bool):
    global is_warning_light_on
    is_warning_light_on = isOn

    if is_raspberry_pi:
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
        return

    stop_event = threading.Event()
    thread = threading.Thread(target=blink, args=(stop_event,))
    blinkThread = thread
    thread.start()

# Stop blinking the warning light
def stopBlink():
    global blinkThread
    if isBlinking() is False:
        return
    
    stop_event = blinkThread._args[0]  # Get the stop_event from the thread
    stop_event.set()  # Signal the thread to stop
    blinkThread.join()  # Wait for the thread to finish
    blinkThread = None  # Reset the thread

    warningLight(False)
    
# Stop blinking the warning light
def isBlinking():
    return blinkThread is not None

def exit():
    stopBlink()
    cameraLight(False)
    warningLight(False)