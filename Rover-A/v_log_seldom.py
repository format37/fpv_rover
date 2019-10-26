from ina219 import INA219
import time

SHUNT_OHMS = 0.1
ina = INA219(SHUNT_OHMS)
ina.configure()
v_log = open('/var/www/html/v_log_seldom.txt', 'a')
v_log.write(str(time.time())+' '+str(ina.voltage())+'\n')
v_log.close()

time_current=int(float(time.time()))
log_length=60*60*24 # s * min * hours_count
with open('/var/www/html/v_log_seldom.txt') as file:
    new_data=[]
    lines = file.readlines()
    for line in lines:
        val=line.split()
        val_time=time_current-int(float(val[0]))
        if val_time<=log_length:
            new_data.append(' '.join(val))
file.close()
with open('/var/www/html/v_log_seldom.txt','w') as file:
    file.write('\n'.join(new_data)+'\n')
file.close()