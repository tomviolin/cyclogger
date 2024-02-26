import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setup(35, GPIO.IN)

lasttime = 0

def flinfo(pin):
    global lasttime
    thistime = time.time()
    if lasttime != 0:
        dt = thistime - lasttime
        print(f"time={thistime} dt={dt}")
    lasttime = thistime

GPIO.add_event_detect(35, GPIO.RISING, flinfo)

input()
