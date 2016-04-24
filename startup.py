#!/usr/bin/python

from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
from subprocess import *
from time import sleep


def run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output

def shutdown():
    run_cmd("shutdown -h now")

def display(lcd, message, backlight):
    lcd.clear()
    lcd.message(message)
    lcd.backlight(backlight)

def getNextPage(lcd, onUp, onDown, onLeft, onRight, onSelect):
    while True:
        if lcd.buttonPressed(lcd.UP):
            while lcd.buttonPressed(lcd.UP):
                sleep(0.1)
            return onUp
        if lcd.buttonPressed(lcd.DOWN):
            while lcd.buttonPressed(lcd.DOWN):
                sleep(0.1)
            return onDown
        if lcd.buttonPressed(lcd.LEFT):
            while lcd.buttonPressed(lcd.LEFT):
                sleep(0.1)
            return onLeft
        if lcd.buttonPressed(lcd.RIGHT):
            while lcd.buttonPressed(lcd.RIGHT):
                sleep(0.1)
            return onRight
        if lcd.buttonPressed(lcd.SELECT):
            while lcd.buttonPressed(lcd.SELECT):
                sleep(0.1)
            return onSelect

# LCD Ansteuerung erstellen
# lcd.RED , lcd.YELLOW, lcd.GREEN, lcd.TEAL, lcd.BLUE, lcd.VIOLET, lcd.ON, lcd.OFF
lcd = Adafruit_CharLCDPlate(1)
lcd.clear()

# Feld mit der aktuellen Seite
currentPage = 53

while True:
    if currentPage == 1:
        lanIp = run_cmd("ip addr show eth0 | grep inet | awk '{print $2}' | cut -d/ -f1")
        msg = "Ethernet\n" + lanIp
        display(lcd, msg, lcd.TEAL)
        currentPage = getNextPage(lcd, 4, 2, 1, 1, 1)

    if currentPage == 2:
        wlanIp = run_cmd("ip addr show wlan0 | grep inet | awk '{print $2}' | cut -d/ -f1")
        msg = "WLAN\n" + wlanIp
        display(lcd, msg, lcd.TEAL)
        currentPage = getNextPage(lcd, 1, 3, 2, 2, 2)

    if currentPage == 3:
        temp = run_cmd("/opt/vc/bin/vcgencmd measure_temp | cut -b 6-")
        msg = "Temp Rasp\n" + temp
        display(lcd, msg, lcd.TEAL)
        currentPage = getNextPage(lcd, 2, 4, 3, 3, 3)

    if currentPage == 4:
        temp_raw = run_cmd("cat /sys/bus/w1/devices/28-000007b38daf/w1_slave")
	temp_raw = temp_raw.split('\n')[1][29:32]
        temp = "{}.{} C".format(temp_raw[:2], temp_raw[-1])
        msg = "Temp\n" + temp
        display(lcd, msg, lcd.TEAL)
        currentPage = getNextPage(lcd, 3, 5, 4, 4, 4)

    if currentPage == 5:
        msg = "Shutdown?"
        display(lcd, msg, lcd.RED)
        currentPage = getNextPage(lcd, 4, 1, 52, 52, 51)

    if currentPage == 51:
        shutdown()
        msg = "Shutting\ndown..."
        display(lcd, msg, lcd.RED)
        sleep(1)
        break

    if currentPage == 52:
        msg = "Shutdown LCD?"
        display(lcd, msg, lcd.RED)
        currentPage = getNextPage(lcd, 4, 1, 5, 5, 53)

    if currentPage == 53:
        msg = ""
        display(lcd, msg, lcd.OFF)
        currentPage = getNextPage(lcd, 1, 1, 1, 1, 1)
