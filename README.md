### fpv_rover

## Table of contents
* [Components](#components)

## Components:
* raspberry pi
* L298N
* 3d printed tank with components from https://hackaday.io/project/164896-rc-fpv-tank-rover

## Rover-A files:
* /var/www/html/rover.php - public script
* /var/www/html/rover.py - rover script
* /var/www/html/led.py - night vision led script
* /var/www/html/led_cmd.txt - night vision led key
* /lib/systemd/system/rover_led.service - autorun script

## Server-B files:
* rover.php

```
Due to government blocking of Telegram, I had to add an intermediate server.
```

## Server-C files:
* rover_bot.php - bot script, called from telegram
* relayPhotoViaPut_rover.php - photo script, called from rover
* relayPhoto.php - photo script, called from relayPhotoViaPut_rover.php

## autorun script install procedure:
```
sudo nano /lib/systemd/system/rover_led.service #add text from file
sudo systemctl daemon-reload
sudo systemctl enable rover_led.service
sudo systemctl start  rover_led.service
sudo systemctl status rover_led.service #check
```

## access from web
* Rover-A connected to Wi-fi-router-A
* Wi-fi-router-A connected to internet via USB-modem
* Rover-A automatically connected to Server-B-vpn at system start
* Server-B connected to Wi-fi-router-B with external IP
* Wi-fi-router-B port 80 forwarded to Server-B
* Server-B port 80 forwarded to Rover-A
* Server-C receives commands from Server-Telegram and redirects them to Server-B
* Rover-A sends photo via Server-C to Server-Telegram
