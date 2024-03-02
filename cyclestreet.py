#!/usr/bin/env python3

import subprocess
import json
import pyautogui
import requests

def cyclestreet():
    return requests.get('http://localhost:8000/latest.json').json()

def main():
    # initial read
    lastdata = cyclestreet()
    lastdistance = float(lastdata['distance'])
    # loop forever
    while True:
        data = cyclestreet()
        distance = float(data['distance'])
        if distance - lastdistance > 0.1/10:
            print(f"{distance}-{lastdistance}={distance - lastdistance}")
            print('up!')
            pyautogui.press('up')
            lastdistance = distance
        elif distance - lastdistance < 0:
            # reset the last distance
            lastdistance = distance

if __name__ == '__main__':
    main()
