hueBerry: Setup instructions for Developers
=============
### *"Bare-metal" install instructions for dev-kit*

[![hueBerry Mess!](https://github.com/fiveseven808/HueBerry_SmartSwitch/blob/dev/hueBerry%20Photos/B%20reel/IMG_20160812_165047.jpg?raw=true)](https://youtu.be/YTvbsL82ZcM?t=1m3s "hueBerry Mess!")



## Getting Started: Updated 1/29/2017
Getting started with the hueBerry from a bare-metal pi is pretty simple. Here, I will attempt to guide you from start to finish! 

**Requirements:**

  * Raspberry Pi (I used a Zero)
  * Adafruit_SSD1306 library
  * pigpio library
  * SSD1306 compatible display (128x64 resolution)
  * Rotary encoder switch thing 
  * Full BOM located [here](https://docs.google.com/spreadsheets/d/18q5wE9IcbJ1D823ktt4ZN7Fp1JHZutR4hCld2env4vI/edit?usp=sharing)

**Do you meet the dev-kit minimum requirements?** Do you have a display, encoder, pi, and network connection? If so, you may continue! Otherwise, go back and get those components. 
	
**Instructions:**

1. [Install the latest Raspbian distribution](https://www.raspberrypi.org/documentation/installation/installing-images/)
2. Wire up the I2C display and rotary encoder (wiring diagrams coming soon)
3. [Install the Adafruit_SSD1306 library](https://learn.adafruit.com/ssd1306-oled-displays-with-raspberry-pi-and-beaglebone-black/usage)
  1. sudo apt-get update
  2. sudo apt-get install build-essential python-dev python-pip
  3. sudo pip install RPi.GPIO
  4. sudo apt-get install python-imaging python-smbus
  5. sudo apt-get install git
  6. git clone https://github.com/adafruit/Adafruit_Python_SSD1306.git
  7. cd Adafruit_Python_SSD1306
  8. sudo python setup.py install
4. [Install and run pigpiod via "sudo pigpiod"](http://abyz.co.uk/rpi/pigpio/download.html)
```bash
rm master.zip
sudo rm -rf pigpio-master
wget https://github.com/joan2937/pigpio/archive/master.zip
unzip master.zip
cd pigpio-master
make -j4
sudo make install
sudo pigpiod 
```
  * You may want to add this to your startup file (I used /etc/rc.local)

5. Run whatever the latest v00*.py is. Should work.
6. Follow instructions on the screen to pair your hueBerry and bridge
7. ???
8. Profit!!!


		  	 
	
	
**License:** 

[Creative Commons Attribution-NonCommercial 4.0 International ](https://creativecommons.org/licenses/by-nc/4.0/)  
This is an open source beta program supplied with no guarantee.