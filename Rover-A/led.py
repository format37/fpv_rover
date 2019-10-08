from gpiozero import LED
from time import sleep
import requests

led = LED(24)
last_cmd=0

while True:
        f = open('/var/www/html/led_cmd.txt', 'r')
        led_cmd=int(f.read())
        if (int(led_cmd)==1 and last_cmd!=1):
                led.on()
                last_cmd=1
        elif (int(led_cmd)==0 and last_cmd!=0):
                led.off()
                last_cmd=0
        sleep(1)