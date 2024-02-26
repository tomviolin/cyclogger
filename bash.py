import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(16,GPIO.OUT)

#pw = GPIO.PWM(16,1)
#pw.start(1)


while True:
    input()
    for i in range(3):
        GPIO.output(16,1)
        GPIO.output(16,0)
        GPIO.output(16,1)
        GPIO.output(16,0)

