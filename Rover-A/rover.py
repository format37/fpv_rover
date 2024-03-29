#python3 move.py 10,10,1000:-10,-10,1000:10,-10,1000
from gpiozero import Motor
from math import pi, atan
import time
import sys
import getopt
import numpy as np
from picamera import PiCamera
import requests
from ina219 import INA219
from ina219 import DeviceRangeError
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline, BSpline

SHUNT_OHMS = 0.1

motor_b = Motor(forward=17, backward=27,pwm=True)
motor_a = Motor(forward=23, backward=22,pwm=True)

def read():
        ina = INA219(SHUNT_OHMS)
        ina.configure()
        return ina.voltage()

def send_file(filepath,g):
        with open(filepath, 'rb') as fh:
                mydata = fh.read()
                mydata  = bytes(str(g)+'#', encoding = 'utf-8')+mydata
                headers_data={"Origin":"http://scriptlab.net","Referer":"http://scriptlab.net/telegram/bots/fpv_rover_bot/",'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
                response = requests.put('http://scriptlab.net/telegram/bots/fpv_rover_bot/relayPhotoViaPut_rover.php',data=mydata,headers=headers_data,params={'file': filepath})

def move_motors(command,a,b,t,g,time_last):
        f_log = open('log.txt', 'a')
        f_log.write(time.strftime("%Y.%m.%d-%H:%M:%S", time.localtime())+' c:'+str(command)+' a:'+str(a)+' b:'+str(b)+' t:'+str(t)+' g:'+str(g)+'\n')
        f_log.close()
        if command==0:#m
                ina = INA219(SHUNT_OHMS)
                ina.configure()
                millis_time=t*1000
                percent_a       = a*(-1)
                percent_b       = b*(-1)
                millis_current=int(round(time.time() * 1000))
                millis_start = millis_current

                voltage_values=[]
                voltage_time=[]

                while millis_current<millis_start+millis_time:
                        dampfer=(atan( (millis_current-millis_start)/60 -3)+1.5)/pi
                        dampfer=1 if dampfer>0.95 else dampfer
                        pa=percent_a*dampfer
                        pb=percent_b*dampfer
                        if (pa>0):
                                motor_a.forward(speed=abs(pa))
                        else:
                                motor_a.backward(speed=abs(pa))
                        if (pb>0):
                                motor_b.forward(speed=abs(pb))
                        else:
                                motor_b.backward(speed=abs(pb))
                        time.sleep(1/1000)

                        millis_current=int(round(time.time() * 1000))

                        voltage_values += [ ina.voltage() ]
                        voltage_time += [ (millis_current-millis_start)/1000 ]

                motor_a.stop()
                motor_b.stop()

                print(str(min(voltage_values))+' - '+str(max(voltage_values)))
                print(str(round(time.time()-time_last,2))+": m,"+str(a)+","+str(b)+","+str(t))

        if command==1 or command==2:
                if command==2:
                        f = open('led_cmd.txt', 'w')
                        f.write('1')
                        f.close()
                filepath='image.jpg'
                camera = PiCamera()
                camera.rotation=180
                camera.resolution = (int(a), int(b))#1920, 1080
                camera.start_preview()
                time.sleep(1)
                camera.capture(filepath)
                camera.stop_preview()
                camera.close()
                if command==2:
                        f = open('led_cmd.txt', 'w')
                        f.write('0')
                        f.close()
                send_file(filepath,g)

                print(str(read())+' v\n'+str(round(time.time()-time_last,2))+": p,"+str(int(a))+","+str(int(b))+","+str(t)+",")
        if command==3:
                with open('v_log_seldom.txt') as file:
                        time_current=int(float(time.time()))
                        log_length=60*60*2 # s * min * hours_count
                        time_line=[]
                        value_line=[]
                        with open('v_log_seldom.txt') as file:
                                lines = file.readlines()
                                time_line=[]
                                value_line=[]
                                for line in lines:
                                        val=line.split()
                                        val_time=time_current-int(float(val[0]))
                                        value_line.append(float(val[1]))
                        time_line=np.arange(0, len(value_line), step=1)
                        fig, ax = plt.subplots( nrows=1, ncols=1 )
                        ax.plot(time_line,value_line, color = 'blue', linestyle = 'solid',label = 'V')
                        fig.savefig('log.png')
                        plt.close(fig)
                        send_file('log.png',g)

def job_lock():
        with open('job.txt','r') as f:
                val=f.read()
                if int(val)==0:
                        f.close()
                        with open('job.txt','w') as f:
                                f.write('1')
                                f.close()
                                return False
                f.close()
                return True

def job_unlock():
        with open('job.txt','w') as f:
                f.write('0')
                f.close()

def main(argv):
        if job_lock():
                print('job locked')
                exit()
        time_start=time.time()
        time_last=time_start
        cmd=argv[0].replace(":", ";")
        cmd=cmd.replace("m", "0")
        cmd=cmd.replace("p", "1")
        cmd=cmd.replace("n", "2")
        cmd=cmd.replace("v", "3")
        cmd=np.matrix(cmd)
        for cmd_str in cmd:
                c       = cmd_str.item(0)       # cmd
                a       = cmd_str.item(1)       # a param
                b       = cmd_str.item(2)       # b param
                t       = cmd_str.item(3)       # time
                g       = cmd_str.item(4)       # group

                if c==0 and (abs(a)>1 or abs(b)>1 or t>10 or t<0.01):#m
                        print("m,"+str(a)+","+str(b)+","+str(t))
                        print("m values should be beetwen m,-1 to 1,-1 to 1,0.01 to 10")
                        exit()
                if c==1 and (abs(a)>2000 or abs(b)>2000):#p
                        print("p,"+str(int(a))+","+str(int(b))+","+str(t))
                        print("p values should be beetwen p,0-1920,0-1080,0")
                        exit()

                move_motors(c,a,b,t,g,time_last)
                time_last=time.time()

        print(str(round(time.time()-time_start,2))+": Complete")
        job_unlock()

if __name__ == "__main__":
        main(sys.argv[1:])