#!/usr/bin/env python3

import subprocess
import json
import pyautogui
import requests
import os,sys

initial_test = True

def cyclestreet(url='http://localhost:8000/latest.json'):
    return requests.get(url).json()

def main():
    print("**** DRIVE IN STREET VIEW ****")
    print("Please bring up google maps street view.")
    print(" YOUR LINK:  https://www.google.com/maps/@42.9829454,-87.8783842,3a,75y,357.59h,90t/data=!3m7!1e1!3m5!1sCO-WnUxOyWEUjdDyK7WvEA!2e0!6shttps:%2F%2Fstreetviewpixels-pa.googleapis.com%2Fv1%2Fthumbnail%3Fpanoid%3DCO-WnUxOyWEUjdDyK7WvEA%26cb_client%3Dsearch.revgeo_and_fetch.gps%26w%3D96%26h%3D64%26yaw%3D357.59448%26pitch%3D0%26thumbfov%3D100!7i16384!8i8192?entry=ttu")
    print ("Press ENTER when Street View is ready")
    input("Enter when ready -->")
    print("Ok, start cycling!")
    url = None
    if (len(sys.argv) > 1):
        url = sys.argv[1]
    # initial read
    lastdata = cyclestreet(url)
    lastdistance = float(lastdata['distance'])
    # loop forever
    while True:
        data = cyclestreet(url)
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
