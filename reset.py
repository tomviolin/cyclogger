#!/usr/bin/env python3
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup([33,35,37], GPIO.IN)
GPIO.cleanup([33,35,37]);


