#!/usr/bin/env python3
import psutil
import openrazer.client
from time import sleep



devman = openrazer.client.DeviceManager()
devices = devman.devices
print("devices found: " + str(len(devices)))
if len(devices) == 0:
    print("ERROR: No Razer device found!")
    quit()
device = devices[0]



def devsetcolor(device, x, y, color):
    device.fx.advanced.matrix[y, x] = color

def devdraw(device):
    device.fx.advanced.draw()

def devcols(device):
    return device.fx.advanced.cols

def devrows(device):
    return device.fx.advanced.rows

def display_white(device):
    for y in range(devrows(device)):
        for x in range(devcols(device)):
            devsetcolor(device, x, y, [255, 255, 255])

anim_counter = 0
def display_battery(device):
    global anim_counter
    anim_counter += 1
    batterylevel = psutil.sensors_battery().percent

    y = 0
    xborder = int((batterylevel * 15 / 100) + 1)


    if batterylevel > 15:
        for x in range(1, devcols(device)):
            devsetcolor(device, x, y, [10, 255, 10])

        for x in range(xborder, devcols(device)):
            devsetcolor(device, x, y, [255, 10, 10])

    elif batterylevel > 5:
        for x in range(1, devcols(device)):
            devsetcolor(device, x, y, [0, 255, 0])
        if (anim_counter % 6) > 2:
            for x in range(xborder, devcols(device)):
                devsetcolor(device, x, y, [255, 0, 0])

    else:
        for x in range(1, devcols(device)):
            devsetcolor(device, x, y, [0, 255, 0])
        if (anim_counter % 2) > 0:
            for x in range(xborder, devcols(device)):
                devsetcolor(device, x, y, [255, 0, 0])

def display_cpu(device):
    cpulevel = psutil.cpu_percent()

    x = 14
    y = 2

    if cpulevel > 50:
        devsetcolor(device, x, y, [255, 0, 0])
    elif cpulevel > 5:
        green_val = 255 - ((cpulevel - 5 ) * 255 / 45)
        red_val = (cpulevel - 5 ) * 255 / 45
        devsetcolor(device, x, y, [red_val, green_val, 0])
    else:
        devsetcolor(device, x, y, [255, 255, 255])



def mainloop():
    try:
        while 1:
            display_white(device)
            display_battery(device)
            display_cpu(device)
            devdraw(device)
            sleep(0.25)
    except KeyboardInterrupt:
        quit()


mainloop()


for x in range(devcols(device)):
    for y in range(devrows(device)):
        devsetcolor(device, x, y, [255, 0, 0])

devdraw(device)
