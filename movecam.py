from gpiozero import AngularServo
from time import sleep

servo = AngularServo(18, min_angle=-90, max_angle=90)

start=90
limit=90

def up():
	for i in range(limit):
		servo.angle = start-i
		sleep(0.01)

def down():
	for i in range(limit):
		servo.angle = start-limit+i
		sleep(0.01)
	
down()
sleep(2)
up()
sleep(2)
#servo.angle=-20
#leep(2)