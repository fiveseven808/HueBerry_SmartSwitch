#!/usr/bin/env python
"""
v006 update
nothing yet... 

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
        current_time = time.strftime("%-I:%M")
    else:
        current_time = time.strftime("%-H:%M")
        
    current_date = time.strftime("%m / %d / %Y")

    # Clear image buffer by drawing a black filled box
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    #Get 24 hour time variable 
    H = int(time.strftime("%H"))
    # Set font type and size
    #H = 9
    if H >= 21 or H < 6:
        font = ImageFont.truetype('BMW_outline.otf', 40)
        #print("outline")
    else:
        font = ImageFont.truetype('BMW_naa.ttf', 45)
        #print("regular")
    #print H
    #time.sleep(100)

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

def display_2lines(line1,line2,size):
    # Clear image buffer by drawing a black filled box
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    if(time_format):
        current_time = time.strftime("%-I:%M")
    else:
        current_time = time.strftime("%-H:%M")   
    current_date = time.strftime("%m / %d / %Y")
    font = ImageFont.truetype('BMW_naa.ttf', 11)
    #font = ImageFont.load_default()
    #draw a clock
    # Position time
    x_pos = (disp.width/2)-(string_width(font,current_time)/2)
    y_pos = 0
    # Draw time
    draw.text((x_pos, y_pos), current_time, font=font, fill=255)
    #draw a menu line
    timeheight = 10
    draw.line((0, timeheight, disp.width, timeheight), fill=255)
    
    # Set font type and size	
    font = ImageFont.truetype('BMW_naa.ttf', size)
    x_pos = (disp.width/2)-(string_width(font,line1)/2)
    y_pos = 8 + (disp.height-4-8)/2 - (35/2)
    draw.text((x_pos, y_pos), line1, font=font, fill=255)

    x_pos = (disp.width/2)-(string_width(font,line2)/2)
    y_pos = disp.height-26
    draw.text((x_pos, y_pos), line2, font=font, fill=255)


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
  
def hue_lights(lnum,lon,lbri,lsat,lx,ly,lct,ltt):
    #send command to OS to turn off all lights
    #plot.savefig('hanning' + str(num) + '.pdf')
    result = os.popen("curl --silent -H \"Accept: application/json\" -X PUT --data '{\"on\":" + str(lon) + ",\"bri\":" + str(lbri) + ",\"sat\":" + str(lsat) + ",\"xy\":[" + str(lx) + "," + str(ly) + "],\"transitiontime\":" + str(ltt) + ",\"ct\":" + str(lct) + "}' http://192.168.1.144/api/0DEuqTaGHB5J2V72IzV1K-r3mwpf9ddjDkDDIRdzr/lights/" + str(lnum) + "/state").read()
    print(result)
    return result

def hue_groups(lnum,lon,lbri,lsat,lx,ly,lct,ltt):
    #send command to OS to turn off all lights
    #plot.savefig('hanning' + str(num) + '.pdf')
    result = os.popen("curl -s -m 1 -H \"Accept: application/json\" -X PUT --data '{\"on\":" + str(lon) + ",\"bri\":" + str(lbri) + ",\"sat\":" + str(lsat) + ",\"xy\":[" + str(lx) + "," + str(ly) + "],\"transitiontime\":" + str(ltt) + ",\"ct\":" + str(lct) + "}' http://192.168.1.144/api/0DEuqTaGHB5J2V72IzV1K-r3mwpf9ddjDkDDIRdzr/groups/" + str(lnum) + "/action").read()
    print(result)
    return result
    

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
    
def g_light_control():
    time.sleep(0.25)
    global pos
    exitvar = False 
    menudepth = 6
    while exitvar == False: 
        if(pos > menudepth):
            pos = menudepth
        elif(pos < 1):
            pos = 1
        display = pos

        #Display Selected Menu
        if(display <= 5):
            display_2lines(str(display) + ". Group " + str(display),"Control",17)
        else:
            display_2lines("Back","One Level",17)
            
        # Poll button press and trigger action based on current display
        if(not GPIO.input(16)):
            if(display <= 5):
                g_control(display)
                time.sleep(0.01)
            elif(display == 6):
                time.sleep(0.25)
                pos = 8
                exitvar = True
            time.sleep(0.01)
            #prev_millis = int(round(time.time() * 1000))
    return
    
def l_light_control():
    time.sleep(0.25)
    global pos
    exitvar = False 
    menudepth = 13
    while exitvar == False: 
        if(pos > menudepth):
            pos = menudepth
        elif(pos < 1):
            pos = 1
        display = pos

        #Display Selected Menu
        if(display <= 12):
            display_2lines(str(display) + ". Light " + str(display),"Control",17)
        else:
            display_2lines("Back","One Level",17)
            
        # Poll button press and trigger action based on current display
        if(not GPIO.input(16)):
            if(display <= 12):
                l_control(display)
                time.sleep(0.01)
            elif(display == 13):
                time.sleep(0.25)
                pos = 9
                exitvar = True
            time.sleep(0.01)
            #prev_millis = int(round(time.time() * 1000))
    return

def g_control(group):  
    time.sleep(0.25)
    global pos
    pos = 1
    exitvar = False 
    max_rot_val = 25
    bri_pre = pos * 10 
    while exitvar == False: 
        if(pos > max_rot_val):
            pos = max_rot_val
        elif(pos < 0):
            pos = 0

        rot_bri = pos * 10 
        display_2lines("Group " + str(group),"Bri: " + str(rot_bri),17)
        if rot_bri == 0 and rot_bri != bri_pre:
            hue_groups(lnum = group,lon = "false",lbri = rot_bri,lsat = "-1",lx = "-1",ly = "-1",ltt = "4", lct = "-1")
            bri_pre = rot_bri
            time.sleep(.25)
        elif rot_bri != bri_pre:
            hue_groups(lnum = group,lon = "true",lbri = rot_bri,lsat = "-1",lx = "-1",ly = "-1",ltt = "4", lct = "-1")
            bri_pre = rot_bri
            time.sleep(.25)
            
        if(not GPIO.input(16)):
            time.sleep(0.25)
            exitvar = True
            time.sleep(0.01)
            pos = group

def l_control(light):  
    time.sleep(0.25)
    global pos
    pos = 1
    exitvar = False 
    max_rot_val = 25
    bri_pre = pos * 10 
    while exitvar == False: 
        if(pos > max_rot_val):
            pos = max_rot_val
        elif(pos < 0):
            pos = 0

        rot_bri = pos * 10 
        display_2lines("Light " + str(light),"Bri: " + str(rot_bri),17)
        if rot_bri == 0 and rot_bri != bri_pre:
            hue_lights(lnum = light,lon = "false",lbri = rot_bri,lsat = "-1",lx = "-1",ly = "-1",ltt = "4", lct = "-1")
            bri_pre = rot_bri
            time.sleep(.25)
        elif rot_bri != bri_pre:
            hue_lights(lnum = light,lon = "true",lbri = rot_bri,lsat = "-1",lx = "-1",ly = "-1",ltt = "4", lct = "-1")
            bri_pre = rot_bri
            time.sleep(.25)
            
        if(not GPIO.input(16)):
            time.sleep(0.25)
            exitvar = True
            time.sleep(0.01)
            pos = light
    
	
def string_width(fontType,string):
	string_width = 0

	for i, c in enumerate(string):
		char_width, char_height = draw.textsize(c, font=fontType)
		string_width += char_width

	return string_width
#--------------------------------------------------
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
#--------------------------------------------------
prev_millis = 0
display = 0
time_format = True

#Clear Draw buffer
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Set font type and size
font = ImageFont.truetype('BMW_naa.ttf', 50)
#font = ImageFont.load_default()
# Set and Position splash
splash = "hue"
x_pos = (disp.width/2)-(string_width(font,splash)/2)
y_pos = 2 + (disp.height-4-8)/2 - (35/2)
    
# Draw splash
draw.text((x_pos, y_pos), splash, font=font, fill=255)
#disp.dim(True)
#disp.set_contrast(0)
disp.image(image)
disp.display()
#time.sleep(.5)

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

    # Cycle through different displays
    if(pos > 9):
        pos = 9
    elif(pos < 0):
        pos = 0
    display = pos

    #Display Selected Menu
    if(display == 0):
        display_time()
        #Sleep to conserve CPU Cycles
        #time.sleep(0.5)
    elif(display == 1):
        display_2lines("1. Turn OFF","all lights slowly",17)
    elif(display == 2):
        display_2lines("2. DIM ON","Night lights",17)
    elif(display == 3):
        display_2lines("3. FULL ON","all lights",17)
    elif(display == 4):
        display_2lines("4. Turn OFF","all lights quickly",17)
    elif(display == 5):
        display_2lines("5. After","Dinner",17)
    elif(display == 6):
        display_2lines("6. Going","to bed",17)
    elif(display == 7):
        display_2lines("7. In bed", "already",17)
    elif(display == 8):
        display_2lines("8. Group Control", "Menu",13)
    elif(display == 9):
        display_2lines("9. Light Control", "Menu",13)
     
    # Poll button press and trigger action based on current display
    if(not GPIO.input(16)):
        if(display == 0):
            # Toggle between 12/24h format
            time_format =  not time_format
            time.sleep(0.5)
        elif(display == 1):
            # Turn off all lights 
            display_2lines("Turning all","lights OFF slowly",12)
            #os.popen("sudo ifdown wlan0; sleep 5; sudo ifup --force wlan0")
            debug = os.popen("curl -H \"Accept: application/json\" -X PUT --data '{\"on\":false,\"transitiontime\":100}' http://192.168.1.144/api/0DEuqTaGHB5J2V72IzV1K-r3mwpf9ddjDkDDIRdzr/groups/0/action").read()
            #print(debug)
            time.sleep(10)
        elif(display == 2):
            # Turn on NIGHT lights dim (groups 1,2,3)
            display_2lines("Turning specific","lights on DIM",12)
            debug = os.popen("curl -H \"Accept: application/json\" -X PUT --data '{\"on\":true,\"bri\":1,\"transitiontime\":100}' http://192.168.1.144/api/0DEuqTaGHB5J2V72IzV1K-r3mwpf9ddjDkDDIRdzr/groups/1/action").read()
            debug = os.popen("curl -H \"Accept: application/json\" -X PUT --data '{\"on\":true,\"bri\":1,\"transitiontime\":100}' http://192.168.1.144/api/0DEuqTaGHB5J2V72IzV1K-r3mwpf9ddjDkDDIRdzr/groups/2/action").read()
            debug = os.popen("curl -H \"Accept: application/json\" -X PUT --data '{\"on\":true,\"bri\":1,\"transitiontime\":100}' http://192.168.1.144/api/0DEuqTaGHB5J2V72IzV1K-r3mwpf9ddjDkDDIRdzr/groups/3/action").read()
            # Turn off front door light 
            #print(debug)
            time.sleep(1)
        elif(display == 3):
            display_2lines("Turning all","lights on FULL",12)
            hue_groups(lnum = "0",lon = "true",lbri = "254",lsat = "256",lx = "-1",ly = "-1",ltt = "4",lct = "-1")
            #turn off front door light... we dont want that... 
            hue_groups(lnum = "5",lon = "false",lbri = "1",lsat = "256",lx = "-1",ly = "-1",ltt = "4",lct = "-1")
        elif(display == 4):
            display_2lines("Turning all","lights OFF quickly",12)
            hue_groups(lnum = "0",lon = "false",lbri = "256",lsat = "256",lx = "-1",ly = "-1",ltt = "4",lct = "-1")
        elif(display == 5):
            display_2lines("Turning lights:","After dinner",12)
            debug = os.popen("curl -H \"Accept: application/json\" -X PUT --data '{\"on\":true,\"bri\":127,\"sat\":1,\"ct\":450,\"transitiontime\":100}' http://192.168.1.144/api/0DEuqTaGHB5J2V72IzV1K-r3mwpf9ddjDkDDIRdzr/groups/1/action").read()
            debug = os.popen("curl -H \"Accept: application/json\" -X PUT --data '{\"on\":true,\"bri\":129,\"sat\":193,\"ct\":432,\"transitiontime\":100}' http://192.168.1.144/api/0DEuqTaGHB5J2V72IzV1K-r3mwpf9ddjDkDDIRdzr/groups/2/action").read()
            debug = os.popen("curl -H \"Accept: application/json\" -X PUT --data '{\"on\":true,\"bri\":254,\"transitiontime\":100}' http://192.168.1.144/api/0DEuqTaGHB5J2V72IzV1K-r3mwpf9ddjDkDDIRdzr/groups/3/action").read()
            debug = os.popen("curl -H \"Accept: application/json\" -X PUT --data '{\"on\":true,\"bri\":1,\"transitiontime\":100}' http://192.168.1.144/api/0DEuqTaGHB5J2V72IzV1K-r3mwpf9ddjDkDDIRdzr/groups/4/action").read()
            debug = os.popen("curl -H \"Accept: application/json\" -X PUT --data '{\"on\":false,\"transitiontime\":100}' http://192.168.1.144/api/0DEuqTaGHB5J2V72IzV1K-r3mwpf9ddjDkDDIRdzr/groups/5/action").read()
            #print(debug)
        elif(display == 6):
            display_2lines("Turning lights:","About to sleep bed",12)
            hue_lights(lnum = "1",lon = "true",lbri = "1",lsat = "256",lx = "-1",ly = "-1",ltt = "100", lct = "-1")
            hue_lights(lnum = "2",lon = "false",lbri = "144",lsat = "256",lx = "-1",ly = "-1",ltt = "100", lct = "-1")
            hue_lights(lnum = "5",lon = "true",lbri = "144",lsat = "200",lx = "0.5015",ly = "0.4153",ltt = "100", lct = "-1")
            hue_lights(lnum = "6",lon = "true",lbri = "1",lsat = "256",lx = "-1",ly = "-1",ltt = "100", lct = "-1")
            hue_lights(lnum = "7",lon = "true",lbri = "127",lsat = "1",lx = "-1",ly = "-1",ltt = "100", lct = "450")
            hue_lights(lnum = "8",lon = "true",lbri = "127",lsat = "1",lx = "-1",ly = "-1",ltt = "100", lct = "450")
            hue_lights(lnum = "9",lon = "true",lbri = "144",lsat = "199",lx = "-1",ly = "-1",ltt = "100", lct = "443")
            hue_lights(lnum = "10",lon = "false",lbri = "144",lsat = "199",lx = "-1",ly = "-1",ltt = "100", lct = "443")
            hue_lights(lnum = "11",lon = "false",lbri = "1",lsat = "199",lx = "-1",ly = "-1",ltt = "100", lct = "-1")
            hue_lights(lnum = "12",lon = "false",lbri = "1",lsat = "256",lx = "-1",ly = "-1",ltt = "100", lct = "-1")
        elif(display == 7):
            display_2lines("Turning lights:","Everything dim",12)
            hue_groups(lnum = "1",lon = "true",lbri = "1",lsat = "-1",lx = "-1",ly = "-1",ltt = "100",lct = "381")
            hue_groups(lnum = "2",lon = "false",lbri = "1",lsat = "-1",lx = "-1",ly = "-1",ltt = "100",lct = "439")
            hue_groups(lnum = "3",lon = "true",lbri = "1",lsat = "-1",lx = "-1",ly = "-1",ltt = "100",lct = "-1")
            hue_groups(lnum = "4",lon = "true",lbri = "2",lsat = "-1",lx = "-1",ly = "-1",ltt = "100",lct = "-1")
            hue_groups(lnum = "5",lon = "false",lbri = "1",lsat = "-1",lx = "-1",ly = "-1",ltt = "100",lct = "-1")
        elif(display == 8):
            pos = 0
            g_light_control()
        elif(display == 9):
            pos = 0
            l_light_control()
        time.sleep(0.01)
        #prev_millis = int(round(time.time() * 1000))
        pos = 0

    #time.sleep(0.1)
