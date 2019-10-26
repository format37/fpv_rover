from picamera import PiCamera
import requests
import time

g="-384403215"
camera = PiCamera()
filepath='image.jpg'
camera.rotation=180
camera.resolution = (1280, 1280)
camera.start_preview()
time.sleep(1)
camera.capture(filepath)
camera.stop_preview()
with open(filepath, 'rb') as fh:
        mydata = fh.read()
        mydata  = bytes(str(g)+'#', encoding = 'utf-8')+mydata
        headers_data={"Origin":"http://scriptlab.net","Referer":"http://scriptlab.net/telegram/bots/fpv_rover_bot/",'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
        response = requests.put('http://scriptlab.net/telegram/bots/fpv_rover_bot/relayPhotoViaPut_rover.php',data=mydata,headers=headers_data,params={'file': filepath})