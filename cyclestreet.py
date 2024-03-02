#!/usr/bin/env python3

import subprocess
import json
import pyautogui

def cyclestreet():
    # capture the output of the command
    output = subprocess.check_output(['ssh', 'cycler', 'cat', '/home/tomh/gpio/latest.json'])
    # decode the output to a string
    output = output.decode('utf-8')
    # print the output
    #print(output)
    return json.loads(output)

def main():
    # initial read
    lastdata = cyclestreet()
    lastdistance = float(lastdata['distance'])
    # loop forever
    while True:
        data = cyclestreet()
        distance = float(data['distance'])
        print(f"{distance}-{lastdistance}={distance - lastdistance}")
        if distance - lastdistance > 0.1/8:
            print('up!')
            pyautogui.press('up')
            lastdistance = distance
        elif distance - lastdistance < 0:
            # reset the last distance
            lastdistance = distance



if __name__ == '__main__':
    main()
