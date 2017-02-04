"""
Python installer for hueberry. Probably not the best thing in the world...
"""
import sys
import os
import shutil
#import imp
import subprocess

temp = os.popen("cat /etc/os-release | grep raspbian").read()
#print temp
result_array = temp.split('\n')
num_groups = len(result_array) - 1

#print num_groups

if(num_groups != 4):
    print("This OS is not Raspbian. It does not meet the directory structure requirements of this installer. Exiting")
    sys.exit()
else:
    print("Looks like you're running Rasbian! Good start!")   
#shutil.copy(pythondaemon.py,/home/pi/pythondaemon.py)

print("Checking required modules. Please wait...")
req_modules = ['pigpio','authenticate','Adafruit_SSD1306','RPi','rotary_encoder','wat']
n2install = []
for x in req_modules:
    try:
        #imp.find_module(x)
        #import Adafruit_SSD1306
        new_module = __import__(x)
        found = True
    except ImportError:
        print("    "+str(x) + " module not found. Please install this before continuing!")
        n2install.append(x)
print("\r")
#p = subprocess.Popen('htop')
#p.wait()
        
if len(n2install) > 0:
    #something wrong with this function... can't initiate apt-get update for some reason
    print("Looks like we have some requirements! Updating system repo!")
    #p = subprocess.Popen("sudo apt-get update")
    #p.wait()
    #os.popen("apt-get update")
    print("finished")
    
baremetal = 0
for x in n2install:
    if x == 'pigpio':
        print("Installing " +str(x))
	#os.popen("cd ~ ")
        os.open("rm master.zip && sudo rm -rf pigpio-master && wget https://github.com/joan2937/pigpio/archive/master.zip && unzip master.zip &&  pigpio-master/make -j4 && sudo pigpio-master/make install && sudo pigpiod ")
        print("Done installing " +str(x))
    if x == 'authenticate':
        print("wtf, the " +str(x)+" module should be in the same directory. update re-clone the repo or somethihng")
        baremetal = 1
    if x == 'Adafruit_SSD1306':
        print("Installing " +str(x))
	#os.popen("cd ~ ")
        os.popen("sudo apt-get install build-essential python-dev python-pip && sudo pip install RPi.GPIO && sudo apt-get install python-imaging python-smbus && sudo apt-get install git && git clone https://github.com/adafruit/Adafruit_Python_SSD1306.git && sudo Adafruit_Python_SSD1306/python setup.py install")
        print("Done installing " +str(x))
    if x =='RPi':
        print("wtf, the " +str(x)+" module should be part of the most recent Raspberry Pi distribution.\nAre you even running this on a Pi?")
        print("installing anyway. lel")
        os.popen("sudo pip install RPi.GPIO")
    if x == 'rotary_encoder':
        print("wtf, the " +str(x)+" module should be in the same directory. update re-clone the repo or somethihng")
        baremetal = 1

#print baremetal    
if baremetal > 0:
    #something wrong with this function... can't initiate apt-get update for some reason
    print("Wanna start from scratch?")
    os.popen("git clone -b dev https://github.com/fiveseven808/HueBerry_SmartSwitch.git")
    print("Cloned Repo lol")
    

finalreadme = """ 
How to run:
    cd HueBerry_SmartSwitch
    sudo pigpiod (if not PiGPIOd is not running already)
    sudo python hueberry.py [&]

&           Sets the program to run in the background 
            (You can see more debug messages if you omit this)
            
Enjoy! 
"""
print(finalreadme)
