#!/usr/bin/env python
"""
v002 update
starting on the project for real 
deleting the other functions and just putting in the the hue things... 

"""
import time
import Adafruit_SSD1306
import RPi.GPIO as GPIO
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import os
import pigpio
import rotary_encoder

def display_time():
    # Collect current time and date
    if(time_format):
        current_time = time.strftime("%I:%M")
    else:
        current_time = time.strftime("%H:%M")
        
    current_date = time.strftime("%m / %d / %Y")

    # Clear image buffer by drawing a black filled box
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    #Get 24 hour time variable 
    H = time.strftime("%H") 
    # Set font type and size
    if H >= 21 or H < 6:
        font = ImageFont.truetype('BMW_outline.otf', 40)
    else:
        font = ImageFont.truetype('BMW_naa.ttf', 40)

    # Position time
    x_pos = (disp.width/2)-(string_width(font,current_time)/2)
    y_pos = 2 + (disp.height-4-8)/2 - (35/2)
        
    # Draw time
    draw.text((x_pos, y_pos), current_time, font=font, fill=255)

    # Set font type and size
    font = ImageFont.truetype('BMW_naa.ttf', 13)
    #font = ImageFont.load_default()

    # Position date
    x_pos = (disp.width/2)-(string_width(font,current_date)/2)
    y_pos = disp.height-10

    # Draw date during daytime hours 
    if H <= 21 and H > 6:
        draw.text((x_pos, y_pos), current_date, font=font, fill=255)   

    # Draw the image buffer
    disp.image(image)
    disp.display()

def display_social():
    # Collect social media subscribers/followers/... by parsing webpages
    #twitter = os.popen("curl https://twitter.com/fiveseven808?lang=en | grep 'data-nav=\"followers\"' | grep -o '[0-9]\+'").read()
    twitter = "0"
    #youtube = os.popen("curl https://www.youtube.com/c/FrederickVandenbosch | grep -o '[0-9|,]\+ subscribers' | grep -o '[0-9|,]\+'").read()
    youtube = "0"
    facebook = "0"
    #instagram = os.popen("curl https://www.instagram.com/f_vdbosch/ | grep -o '\"followed_by\":{\"count\":[0-9]\+}' | grep -o '[0-9]\+'").read()
    instagram = "0"
    googleplus = "0"

    # Put data in lists that can be iterated over
    channels = ["YouTube", "Twitter", "Facebook", "Instagram", "Google+"]
    subscribers = [youtube, twitter, facebook, instagram, googleplus]

    # Clear image buffer by drawing a black filled box
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    # Set font type and size
    font = ImageFont.truetype('BMW_naa.ttf', 11)
    #font = ImageFont.load_default()

    # Iterate over lists
    for i in range(0, 5):
        # Position channel name
        x_pos = 2
        y_pos = 2 + (((disp.height-4)/5)*i)

        # Draw channel name
        draw.text((x_pos, y_pos), channels[i], font=font, fill=255)

        # Position subcribers/followers/...
        x_pos = disp.width - 2 - string_width(font, subscribers[i])
        y_pos = 2 + (((disp.height-4)/5)*i)

        # Draw subcribers/followers/...
        draw.text((x_pos, y_pos), subscribers[i], font=font, fill=255)

    # Draw the image buffer
    disp.image(image)
    disp.display()

def display_network():
	# Collect network information by parsing command line outputs
	ipaddress = os.popen("ifconfig wlan0 | grep 'inet addr' | awk -F: '{print $2}' | awk '{print $1}'").read()
	netmask = os.popen("ifconfig wlan0 | grep 'Mask' | awk -F: '{print $4}'").read()
	gateway = os.popen("route -n | grep '^0.0.0.0' | awk '{print $2}'").read()
	ssid = os.popen("iwconfig wlan0 | grep 'ESSID' | awk '{print $4}' | awk -F\\\" '{print $2}'").read()

	# Clear image buffer by drawing a black filled box
	draw.rectangle((0,0,width,height), outline=0, fill=0)

	# Set font type and size
	font = ImageFont.truetype('BMW_naa.ttf', 16)
	#font = ImageFont.load_default()
        
	# Position SSID
	x_pos = 2
	y_pos = 2

	# Draw SSID
	draw.text((x_pos, y_pos), ssid, font=font, fill=255)
	
	# Set font type and size
	font = ImageFont.truetype('BMW_naa.ttf', 11)
	#font = ImageFont.load_default()

	# Position IP
	y_pos += 12 + 10 
        
	# Draw IP
	draw.text((x_pos, y_pos), "IP: "+ipaddress, font=font, fill=255)

	# Position NM
	y_pos += 10 

	# Draw NM
	draw.text((x_pos, y_pos), "NM: "+netmask, font=font, fill=255)

	# Position GW
	y_pos += 10

	# Draw GW
	draw.text((x_pos, y_pos), "GW: "+gateway, font=font, fill=255)
	
	# Draw the image buffer
	disp.image(image)
	disp.display()
	
def display_ping():
	# Collect network information by parsing command line outputs
	pingtime = os.popen("ping -c 1 192.168.1.1 | grep time | awk -F=64 '{print $2}'").read()

	# Clear image buffer by drawing a black filled box
	draw.rectangle((0,0,width,height), outline=0, fill=0)

	# Set font type and size
	font = ImageFont.truetype('BMW_naa.ttf', 17)
	#font = ImageFont.load_default()
        
	# Position SSID
	x_pos = 2
	y_pos = 2

	# Draw SSID
	draw.text((x_pos, y_pos), "PingTime: ", font=font, fill=255)
	
	# Set font type and size
	font = ImageFont.truetype('BMW_naa.ttf', 13)
	#font = ImageFont.load_default()

	# Position IP
	y_pos += 12 + 10 
        
	# Draw IP
	draw.text((x_pos, y_pos), pingtime, font=font, fill=255)
	
	# Draw the image buffer
	disp.image(image)
	disp.display()
def display_mika():
	# Clear image buffer by drawing a black filled box
	draw.rectangle((0,0,width,height), outline=0, fill=0)
	# Set font type and size	
	font = ImageFont.truetype('BMW_naa.ttf', 17)
	#font = ImageFont.load_default()
        
	# Position SSID
	x_pos = (disp.width/2)-(string_width(font,"I love you!")/2)
	y_pos = 2 + (disp.height-4-8)/2 - (35/2)

	# Draw SSID
	draw.text((x_pos, y_pos), "I love you!", font=font, fill=255)
	# Position date
	x_pos = (disp.width/2)-(string_width(font,"Mika!")/2)
	y_pos = disp.height-30

	# Draw date
	draw.text((x_pos, y_pos), "Mika!", font=font, fill=255)
	
	# Draw the image buffer
	disp.image(image)
	disp.display()

def display_2lines(line1,line2,size):
	# Clear image buffer by drawing a black filled box
	draw.rectangle((0,0,width,height), outline=0, fill=0)
	# Set font type and size	
	font = ImageFont.truetype('BMW_naa.ttf', size)
	#font = ImageFont.load_default()
        
	# Position SSID
	x_pos = (disp.width/2)-(string_width(font,line1)/2)
	y_pos = 2 + (disp.height-4-8)/2 - (35/2)

	# Draw SSID
	draw.text((x_pos, y_pos), line1, font=font, fill=255)
	# Position date
	x_pos = (disp.width/2)-(string_width(font,line2)/2)
	y_pos = disp.height-30

	# Draw date
	draw.text((x_pos, y_pos), line2, font=font, fill=255)
	
	# Draw the image buffer
	disp.image(image)
	disp.display()
    
def display_light(text):
	# Clear image buffer by drawing a black filled box
	draw.rectangle((0,0,width,height), outline=0, fill=0)

	font = ImageFont.truetype('BMW_naa.ttf', 17)
	x_pos = (disp.width/2)-(string_width(font,text)/2)
	y_pos = 2 + (disp.height-4-8)/2 - (35/2)

	# Draw SSID
	draw.text((x_pos, y_pos), text, font=font, fill=255)
	
	# Draw the image buffer
	disp.image(image)
	disp.display()
def run_lightsoff():
    #send command to OS to turn off all lights
    #plot.savefig('hanning' + str(num) + '.pdf')
    twitter = os.popen("curl -H \"Accept: application/json\" -X PUT --data '{\"on\":true,\"bri\":254,\"sat\":117,\"xy\":[0.4423,0.4059],\"transitiontime\":10}' http://192.168.1.144/api/0DEuqTaGHB5J2V72IzV1K-r3mwpf9ddjDkDDIRdzr/lights/9/state").read()
    
def hue_lights(lnum,lon,lbri,lsat,lx,ly,ltt):
    #send command to OS to turn off all lights
    #plot.savefig('hanning' + str(num) + '.pdf')
    result = os.popen("curl -H \"Accept: application/json\" -X PUT --data '{\"on\":" + str(lon) + ",\"bri\":" + str(lbri) + ",\"sat\":" + str(lsat) + ",\"xy\":[" + str(lx) + "," + str(ly) + "],\"transitiontime\":" + str(ltt) + "}' http://192.168.1.144/api/0DEuqTaGHB5J2V72IzV1K-r3mwpf9ddjDkDDIRdzr/lights/" + str(lnum) + "/state").read()
    

def display_custom(text):
	# Clear image buffer by drawing a black filled box
	draw.rectangle((0,0,width,height), outline=0, fill=0)

	# Set font type and size
	#font = ImageFont.truetype('FreeMono.ttf', 8)
	font = ImageFont.load_default()
        
	# Position SSID
	x_pos = (width/2) - (string_width(font,text)/2)
	y_pos = (height/2) - (8/2)

	# Draw SSID
	draw.text((x_pos, y_pos), text, font=font, fill=255)

	# Draw the image buffer
	disp.image(image)
	disp.display()
	
def string_width(fontType,string):
	string_width = 0

	for i, c in enumerate(string):
		char_width, char_height = draw.textsize(c, font=fontType)
		string_width += char_width

	return string_width

# Set up GPIO with internal pull-up
GPIO.setmode(GPIO.BCM)	
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	
# 128x64 display with hardware I2C
disp = Adafruit_SSD1306.SSD1306_128_64(rst=24)

# Initialize library
disp.begin()

# Get display width and height
width = disp.width
height = disp.height

# Clear display
disp.clear()
disp.display()

# Create image buffer with mode '1' for 1-bit color
image = Image.new('1', (width, height))

# Load default font
font = ImageFont.load_default()

# Create drawing object
draw = ImageDraw.Draw(image)

prev_millis = 0
prev_social = 0
display = 0
time_format = True

draw.rectangle((0,0,width,height), outline=0, fill=0)

# Set font type and size
font = ImageFont.truetype('BMW_naa.ttf', 50)
#font = ImageFont.load_default()
# Set and Position splash
splash = "hue"
x_pos = (disp.width/2)-(string_width(font,splash)/2)
y_pos = 2 + (disp.height-4-8)/2 - (35/2)
    
# Draw time
draw.text((x_pos, y_pos), splash, font=font, fill=255)
#disp.dim(True)
#disp.set_contrast(0)
disp.image(image)
disp.display()
time.sleep(1)

#----------------- set variables---------------
global pos  
pos = 0

def callback(way):
        global pos
        pos += way
        #print("pos={}".format(pos))
        
pi = pigpio.pi()
decoder = rotary_encoder.decoder(pi, 21, 20, callback)
    
while True:
    millis = int(round(time.time() * 1000))      
    
    # Software debouncing
    if((millis - prev_millis) > 250):
        # Cycle through different displays
        #if(not GPIO.input(20)):
        if(pos > 4):
            pos = 4
        elif(pos < 0):
            pos = 0
        display = pos
        prev_millis = int(round(time.time() * 1000))

		# Trigger action based on current display
        if(not GPIO.input(16)):
            if(display == 0):
                # Toggle between 12/24h format
                time_format =  not time_format
                time.sleep(0.01)
            elif(display == 1):
                # Turn off all lights 
                display_2lines("Turning all","lights OFF slowly",12)
                #run_lightsoff("reconnecting wifi ...")
                #os.popen("sudo ifdown wlan0; sleep 5; sudo ifup --force wlan0")
                debug = os.popen("curl -H \"Accept: application/json\" -X PUT --data '{\"on\":false,\"transitiontime\":100}' http://192.168.1.144/api/0DEuqTaGHB5J2V72IzV1K-r3mwpf9ddjDkDDIRdzr/groups/0/action").read()
                print(debug)
                time.sleep(10)
                time.sleep(0.01)
            elif(display == 2):
                # Turn on NIGHT lights dim (groups 1,2,3)
                display_2lines("Turning specific","lights on DIM",12)
                debug = os.popen("curl -H \"Accept: application/json\" -X PUT --data '{\"on\":true,\"bri\":1,\"transitiontime\":100}' http://192.168.1.144/api/0DEuqTaGHB5J2V72IzV1K-r3mwpf9ddjDkDDIRdzr/groups/1/action").read()
                debug = os.popen("curl -H \"Accept: application/json\" -X PUT --data '{\"on\":true,\"bri\":1,\"transitiontime\":100}' http://192.168.1.144/api/0DEuqTaGHB5J2V72IzV1K-r3mwpf9ddjDkDDIRdzr/groups/2/action").read()
                debug = os.popen("curl -H \"Accept: application/json\" -X PUT --data '{\"on\":true,\"bri\":1,\"transitiontime\":100}' http://192.168.1.144/api/0DEuqTaGHB5J2V72IzV1K-r3mwpf9ddjDkDDIRdzr/groups/3/action").read()
                # Turn off front door light 
                print(debug)
                time.sleep(1)
                time.sleep(0.01)
            elif(display == 3):
                display_2lines("Turning all","lights on FULL",12)
                debug = os.popen("curl -H \"Accept: application/json\" -X PUT --data '{\"on\":true,\"bri\":254,\"transitiontime\":4}' http://192.168.1.144/api/0DEuqTaGHB5J2V72IzV1K-r3mwpf9ddjDkDDIRdzr/groups/0/action").read()
                print(debug)
                time.sleep(1)
                time.sleep(0.01)
            elif(display == 4):
                display_2lines("Turning all","lights OFF quickly",12)
                debug = os.popen("curl -H \"Accept: application/json\" -X PUT --data '{\"on\":false,\"transitiontime\":4}' http://192.168.1.144/api/0DEuqTaGHB5J2V72IzV1K-r3mwpf9ddjDkDDIRdzr/groups/0/action").read()
                print(debug)
                time.sleep(1)
                time.sleep(0.01)
            prev_millis = int(round(time.time() * 1000))
        

    if(display == 0):
        display_time()
        prev_social = 0
    elif(display == 1):
        display_2lines("1. Turn OFF","all lights slowly",17)
        prev_social = 0
    elif(display == 2):
        display_2lines("2. DIM ON","Night lights",17)
        prev_social = 0
    elif(display == 3):
        display_2lines("3. FULL ON","all lights",17)
        prev_social = 0
    elif(display == 4):
        display_2lines("4. Turn OFF","all lights quickly",17)
        prev_social = 0

    time.sleep(0.1)
