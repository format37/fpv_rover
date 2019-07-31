#python3 move.py 10,10,1000:-10,-10,1000:10,-10,1000
from gpiozero import Motor
import time
import sys
import getopt
import numpy as np
from picamera import PiCamera
import requests

motor_a = Motor(forward=17, backward=27,pwm=True)
motor_b = Motor(forward=22, backward=23,pwm=True)

def move_motors(command,a,b,t):
	
	if command==0:#m
		millis_time=t
		percent_a	= a*(-1)
		percent_b	= b*(-1)
		millis_current=int(round(time.time() * 1000))
		millis_start = millis_current
		while millis_current<millis_start+millis_time:
		
			if (percent_a>0):
				motor_a.forward(speed=abs(percent_a)/100)
			else:
				motor_a.backward(speed=abs(percent_a)/100)
			if (percent_b>0):
				motor_b.forward(speed=abs(percent_b)/100)
			else:
				motor_b.backward(speed=abs(percent_b)/100)			
			time.sleep(1/1000)
		
			millis_current=int(round(time.time() * 1000))
			
		motor_a.stop()
		motor_b.stop()

	if command==1:#p
		filepath='image.jpg'
		camera = PiCamera()
		camera.resolution = (a, b)#1920, 1080
		camera.start_preview()
		time.sleep(t/1000)
		camera.capture(filepath)
		camera.stop_preview()
		print("photo captured. sending..")
		with open(filepath, 'rb') as fh:
			mydata = fh.read()
			#payload = {'username': 'bob', 'email': 'bob@bob.com'}
			response = requests.put('http://scriptlab.net/telegram/bots/fpv_rovet_bot/relayPhotoViaPut_rover.php',data=mydata,headers={'content-type':'text/plain'},params={'file': filepath})

def main(argv):
	
	cmd=argv[0].replace(":", ";")
	cmd=cmd.replace("m", "0")
	cmd=cmd.replace("p", "1")
	cmd=np.matrix(cmd)
	for cmd_str in cmd:
		c	= cmd_str.item(0)
		a	= cmd_str.item(1)
		b	= cmd_str.item(2)
		t	= cmd_str.item(3)
		
		if c=='0' and (abs(a)>100 or abs(b)>100 or t>1000*10 or t<1):#m
			print("unable to accept some of values")
			exit()
		if c=='1' and (abs(a)>1920 or abs(b)>1080 or t>5000 or t<1):#p
			print("unable to accept some of values")
			exit()
				
		move_motors(c,a,b,t)

if __name__ == "__main__":
	main(sys.argv[1:])
	print("ok")