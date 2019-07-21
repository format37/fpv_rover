#python3 move.py 10,10,1000:-10,-10,1000:10,-10,1000

from gpiozero import Motor
import time
import sys
import getopt
import numpy as np

motor_a = Motor(forward=17, backward=27,pwm=True)
motor_b = Motor(forward=22, backward=23,pwm=True)

def move_motors(percent_a,percent_b,millis_time):
			
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

def main(argv):
	
	cmd=argv[0].replace(":", ";")
	cmd=np.matrix(cmd)
	for cmd_str in cmd:
		a	= cmd_str.item(0)
		b	= cmd_str.item(1)
		t	= cmd_str.item(2)
		
		if abs(a)>100 or abs(b)>100 or t>1000*10 or t<1:
			print("unable to accept some of values")
			exit()
				
		move_motors(a,b,t)

if __name__ == "__main__":
	main(sys.argv[1:])
	print("ok")