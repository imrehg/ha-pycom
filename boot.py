import os
import pycom
import machine
from machine import UART
from network import WLAN

uart = UART(0, baudrate=115200)
os.dupterm(uart)

pycom.heartbeat(False)

SSID=''
WIFI_PASSWORD=''

wlan = WLAN(mode=WLAN.STA)
wlan.scan()
wlan.connect(ssid=SSID, auth=(WLAN.WPA2, WIFI_PASSWORD))
while not wlan.isconnected():
     machine.idle()

machine.main('main.py')
