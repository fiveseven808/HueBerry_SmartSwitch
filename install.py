"""
Python installer for hueberry. Probably not the best thing in the world...
"""
import sys
import os
import shutil
import imp


temp = os.popen("cat /etc/os-release | grep raspbian").read()
print temp
result_array = temp.split('\n')
num_groups = len(result_array) - 1

print num_groups

if(num_groups != 4):
    print("This OS is not Raspbian. It does not meet the directory structure requirements of this installer. Exiting")
    sys.exit()
    
#shutil.copy(pythondaemon.py,/home/pi/pythondaemon.py)

req_modules = ['pigpio','authenticate','Adafruit_SSD1306','RPi','rotary_encoder','wat']

for x in req_modules:
    try:
        #imp.find_module(x)
        #import Adafruit_SSD1306
        new_module = __import__(x)
        found = True
    except ImportError:
        print(str(x) + " module not found. Please install this")
        