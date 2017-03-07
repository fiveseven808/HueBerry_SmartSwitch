#upgrade.py 
import os

#need to remove all hb_api import staements from hueberry
os.popen("rm /home/pi/scripts/smartswitch/hueberry.py")
os.popen("sudo cp /boot/hueBerry/hueberry.py /home/pi/scripts/smartswitch/")
os.popen("sudo cp /boot/hueBerry/hb_hue.py /home/pi/scripts/smartswitch/")
os.popen("sudo mv /boot/hueBerry/upgrade.py /boot/hueBerry/upgrade.py.used")
os.popen("sudo shutdown -r now")
