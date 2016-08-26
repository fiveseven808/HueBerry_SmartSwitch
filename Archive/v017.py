#!/usr/bin/env python
"""
v017 update
gonna try and increase the responsiveness of the brightness setting

result: looks like responsiveness has improved drastically.. limited actualy sending to bridge to every 1/4 second... 
it would probably be a bit faster if i sent a smaller, better command. or sent them with reckless abandon and didn't wait for a response... 
call seperate pythons script? with subprocess? 

result: subprocess is harder to implement... will deal with that later...

bugfix: program would hang sometimes when moving the dial when "returning" from editing a light brightness
solution: set the pos upon reutrn (not in the function) to the local display var. 
fixed the weird issue where sometimes pos would end up somewhere else like at the return screen and it'd be strange...  
maybe make that a menu option... like... back screen default... so easier to quit when moving around, hard to re-edit quickly... or edit multiples though...

bugfix: settings menu wasn't refreshing properply or returning to previous menu item properply..
solution: implemented light and group fix to settingsg menu. 

"""
import os
#set working directory to script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.popen("python splashscreen.py &")
import time
import Adafruit_SSD1306
import RPi.GPIO as GPIO
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import pigpio
import rotary_encoder
import authenticate
#import subprocess
#import huepi
#figure out how to export this to huepi

menu_timeout = 30 #seconds



#--------------------------------------------------------------------------
def get_group_names():
    os.popen("curl -H \"Accept: application/json\" -X GET " + api_url + "/groups  > lights")
    group_names = os.popen("cat lights | grep -P -o '\"name\":\".*?\"' | grep -o ':\".*\"' | tr -d '\"' | tr -d ':'").read()
    lstate = os.popen("cat lights | grep -o '\"on\":true,\|\"on\":false,' | tr -d '\"on\":' | tr -d ','").read()
    os.popen("rm lights")
    result_array = group_names.split('\n')
    num_groups = len(result_array) - 1
    lstate_a = lstate.split('\n')
    return result_array,num_groups,lstate_a

def get_light_names():
    os.popen("curl -H \"Accept: application/json\" -X GET " + api_url + "/lights  > lights")
    light_names = os.popen("cat lights | grep -P -o '\"name\":\".*?\"' | grep -o ':\".*\"' | tr -d '\"' | tr -d ':'").read()
    num_lights = os.popen("cat lights | grep -P -o '\"[0-9]*?\"' | tr -d '\"'").read()
    lstate = os.popen("cat lights | grep -o '\"on\":true,\|\"on\":false,' | tr -d '\"on\":' | tr -d ','").read()
    os.popen("rm lights")
    name_array = light_names.split('\n')
    num_array = num_lights.split('\n')
    lstate_a = lstate.split('\n')
    total = len(num_array) - 1
    return name_array,num_array,lstate_a,total

def hue_lights(lnum,lon,lbri,lsat,lx,ly,lct,ltt):
    #send command to OS to turn off all lights
    #plot.savefig('hanning' + str(num) + '.pdf')
    result = os.popen("curl --silent -H \"Accept: application/json\" -X PUT --data '{\"on\":" + str(lon) + ",\"bri\":" + str(lbri) + ",\"sat\":" + str(lsat) + ",\"xy\":[" + str(lx) + "," + str(ly) + "],\"transitiontime\":" + str(ltt) + ",\"ct\":" + str(lct) + "}' " + api_url + "/lights/" + str(lnum) + "/state" ).read()
    #subprocess.Popen("curl --silent -H \"Accept: application/json\" -X PUT --data '{\"on\":" + str(lon) + ",\"bri\":" + str(lbri) + ",\"sat\":" + str(lsat) + ",\"xy\":[" + str(lx) + "," + str(ly) + "],\"transitiontime\":" + str(ltt) + ",\"ct\":" + str(lct) + "}' " + api_url + "/lights/" + str(lnum) + "/state" )
    print(result)
    return result

def hue_groups(lnum,lon,lbri,lsat,lx,ly,lct,ltt):
    #send command to OS to turn off all lights
    #plot.savefig('hanning' + str(num) + '.pdf')
    result = os.popen("curl -s -m 1 -H \"Accept: application/json\" -X PUT --data '{\"on\":" + str(lon) + ",\"bri\":" + str(lbri) + ",\"sat\":" + str(lsat) + ",\"xy\":[" + str(lx) + "," + str(ly) + "],\"transitiontime\":" + str(ltt) + ",\"ct\":" + str(lct) + "}' " + api_url + "/groups/" + str(lnum) + "/action").read()
    #subprocess.Popen("curl -s -m 1 -H \"Accept: application/json\" -X PUT --data '{\"on\":" + str(lon) + ",\"bri\":" + str(lbri) + ",\"sat\":" + str(lsat) + ",\"xy\":[" + str(lx) + "," + str(ly) + "],\"transitiontime\":" + str(ltt) + ",\"ct\":" + str(lct) + "}' " + api_url + "/groups/" + str(lnum) + "/action")
    print(result)
    return result

def g_light_control():
    display_custom("loading groups...")
    name_array,total,lstate_a = get_group_names()
    global pos
    old_display = 0
    refresh = 1
    exitvar = False
    menudepth = total + 1
    while exitvar == False:
        if(pos > menudepth):
            pos = menudepth
        elif(pos < 1):
            pos = 1
        display = pos

        #Display Selected Menu
        if (old_display != display or refresh == 1):
            if(display <= total):
                display_3lines(str(display) + ". " + str(name_array[display-1]),"Control","ON: " + str(lstate_a[display-1]),11,offset = 15)
            else:
                display_2lines("Back","One Level",17)
            old_display = display
            refresh = 0
        else:
            time.sleep(0.005)

        # Poll button press and trigger action based on current display
        if(not GPIO.input(21)):
            if(display <= total):
                g_control(display)
                name_array,total,lstate_a = get_group_names()
                refresh = 1 
                pos = display
            else:
                time.sleep(0.25)
                exitvar = True
            time.sleep(0.01)
            #prev_millis = int(round(time.time() * 1000))
    return

def l_light_control():
    display_custom("loading lights...")
    name_array,num_lights,lstate_a,total = get_light_names()
    global pos
    old_display = 0
    refresh = 1 
    exitvar = False
    menudepth = total + 1
    while exitvar == False:
        if(pos > menudepth):
            pos = menudepth
        elif(pos < 1):
            pos = 1
        display = pos

        #Display Selected Menu
        if (old_display != display or refresh == 1):
            if(display <= total):
                display_3lines(str(display) + ". " + str(name_array[display-1]),"Control","ON: " + str(lstate_a[display-1]),11,offset = 15)
            else:
                display_2lines("Back","One Level",17)
            old_display = display
            refresh = 0 
        else:
            time.sleep(0.005)

        # Poll button press and trigger action based on current display
        if(not GPIO.input(21)):
            if(display <= total):
                print(num_lights[display-1])
                l_control(num_lights[display-1])
                name_array,num_lights,lstate_a,total = get_light_names()
                refresh = 1
                pos = display
            else:
                time.sleep(0.25)
                exitvar = True
            time.sleep(0.01)
            #prev_millis = int(round(time.time() * 1000))
    return
    


def g_control(group):
    display_custom("loading brightness...")
    os.popen("curl -H \"Accept: application/json\" -X GET " + api_url + "/groups/" + str(group) + " > brite")
    brite = os.popen("cat brite | grep -o '\"bri\":[0-9]*' | grep -o ':.*' | tr -d ':'").read()
    os.popen("rm brite")
    brite = int(brite)      #make integer
    if brite < 10 and brite >= 0:
        brite = 10

    brite = brite/10        #trim it down to 25 values
    brite = int(brite)      #convert the float down to int agian
    global pos
    pos = brite
    exitvar = False
    max_rot_val = 25
    bri_pre = pos * 10
    refresh = 1
    prev_mills = 0 
    while exitvar == False:
        if(pos > max_rot_val):
            pos = max_rot_val
        elif(pos < 0):
            pos = 0
        mills = int(round(time.time() * 1000))
        millsdiff = mills - prev_mills
        rot_bri = pos * 10
        if(bri_pre != rot_bri or refresh ==  1 ):
            display_2lines("Group " + str(group),"Bri: " + str(int(rot_bri/2.5)) + "%",17)
            refresh = 0
        if rot_bri <= 0 and rot_bri != bri_pre:
            hue_groups(lnum = group,lon = "false",lbri = rot_bri,lsat = "-1",lx = "-1",ly = "-1",ltt = "5", lct = "-1")
            bri_pre = rot_bri
        elif(rot_bri != bri_pre and millsdiff > 250):
            hue_groups(lnum = group,lon = "true",lbri = rot_bri,lsat = "-1",lx = "-1",ly = "-1",ltt = "5", lct = "-1")
            bri_pre = rot_bri
            prev_mills = mills
        elif(millsdiff > 250): 
            prev_mills = mills
            
        if(not GPIO.input(21)):
            while(not GPIO.input(21)):
                display_custom("returning...")
            exitvar = True
        time.sleep(0.01)

def l_control(light):
    display_custom("loading brightness...")
    os.popen("curl -H \"Accept: application/json\" -X GET  "+ api_url + "/lights/" + str(light) + " > brite")
    brite = os.popen("cat brite | grep -o '\"bri\":[0-9]*' | grep -o ':.*' | tr -d ':'").read()
    os.popen("rm brite")
    brite = int(brite)      #make integer
    if brite < 10 and brite >= 0:
        brite = 10

    brite = brite/10        #trim it down to 25 values
    brite = int(brite)      #convert the float down to int agian
    global pos
    pos = brite
    exitvar = False
    max_rot_val = 25
    bri_pre = pos * 10
    refresh = 1
    prev_mills = 0 
    while exitvar == False:
        if(pos > max_rot_val):
            pos = max_rot_val
        elif(pos < 0):
            pos = 0
        mills = int(round(time.time() * 1000))
        millsdiff = mills - prev_mills
        rot_bri = pos * 10
        if(bri_pre != rot_bri or refresh == 1 ):
            display_2lines("Light " + str(light),"Bri: " + str(int(rot_bri/2.5)) + "%",17)
            refresh = 0 
        if rot_bri <= 0 and rot_bri != bri_pre:
            hue_lights(lnum = light,lon = "false",lbri = rot_bri,lsat = "-1",lx = "-1",ly = "-1",ltt = "5", lct = "-1")
            bri_pre = rot_bri
        elif(rot_bri != bri_pre and millsdiff > 250):
            hue_lights(lnum = light,lon = "true",lbri = rot_bri,lsat = "-1",lx = "-1",ly = "-1",ltt = "5", lct = "-1")
            bri_pre = rot_bri
            prev_mills = mills
        elif(millsdiff > 250): 
            prev_mills = mills

        if(not GPIO.input(21)):
            while(not GPIO.input(21)):
                display_custom("returning...")
            exitvar = True
        time.sleep(0.01)
#-------------------------------------------------------------------
#---------------Settings Menu and stuff-----------------------------
#-------------------------------------------------------------------
def pair_hue_bridge():
    pos = 0
    if os.path.isfile('./auth.json') == False:
        while True:
            display_3lines("Attempting Link","Push Bridge button" ,"Then push this button",11,offset = 15)
            if(not GPIO.input(21)):
                break
        display_custom("doing a thing...") 
        ip = authenticate.search_for_bridge()
        authenticate.authenticate('hueBerry',ip)
        authenticate.load_creds()
        api_key = authenticate.api_key
        bridge_ip = authenticate.bridge_ip
        display_2lines("Link Successful",bridge_ip,12)
        time.sleep(1)
    else:
        authenticate.load_creds()
        api_key = authenticate.api_key
        bridge_ip = authenticate.bridge_ip
        api_url = 'http://%s/api/%s' % (bridge_ip,api_key)
        display_2lines("Already Paired!",bridge_ip,12)
        time.sleep(1)
        
def devinfo_screen():
    ipaddress = os.popen("ifconfig wlan0 | grep 'inet addr' | awk -F: '{print $2}' | awk '{print $1}'").read()
    ssid = os.popen("iwconfig wlan0 | grep 'ESSID' | awk '{print $4}' | awk -F\\\" '{print $2}'").read()
    while True:
        display_3lines("hueBerry IP: " + str(ipaddress),"Bridge IP: " + str(bridge_ip) ,"WLAN SSID: " + str(ssid),9,offset = 15)
        if(not GPIO.input(21)):
            break
            
def shutdown_hueberry():
    display_3lines("Shutting down now...","Don't remove power" ,"Until Display is off",11,offset = 15)
    os.popen("sudo shutdown now")
    while True:
        time.sleep(1)
        
def flashlight_mode():
    while True:
        if(GPIO.input(21)):
            break
    draw.rectangle((0,0,width,height), outline=0, fill=1)
    disp.image(image)
    disp.display()
    while True:
        if(not GPIO.input(21)):
            break
        time.sleep(0.1)

def wifi_settings():
    display_custom("scanning for wifi...")
    global pos
    pos = 0
    timeout = 0 
    os.popen("wpa_cli scan")
    os.popen("wpa_cli scan_results | grep WPS | sort -r -k3 > /tmp/wifi")
    ssids = os.popen("cat /tmp/wifi | awk '{print $5}'").read()
    powers = os.popen("cat /tmp/wifi | awk '{print $3}'").read()
    macs = os.popen("cat /tmp/wifi | awk '{print $1}'").read()
    ssid_array = ssids.split('\n')
    mac_array = macs.split('\n')
    p_array = powers.split('\n')
    total = len(ssid_array) - 1
    menudepth = total + 1
    while True:
        if(pos > menudepth):
            pos = menudepth
        elif(pos < 0):
            pos = 0
        display = pos

        #Display Selected Menu
        if(display == 0):
            display_3lines("Scroll to see","Avaliable [WPS]" ,"SSIDs",11,offset = 15)
        elif(display <= total):
            display_3lines(str(display) + ". " + str(ssid_array[display-1]),"Signal: " + str(p_array[display-1]),"Connect ?",11,offset = 15)
        else:
            display_2lines("Back to","Settings Menu",17)

        # Poll button press and trigger action based on current display
        if(not GPIO.input(21)):
            if(display <= total and display > 0):
                timeout = 0
                display_3lines("Connecting To:",str(ssid_array[display-1]) ,"Push WPS button then click ",9,offset = 15)
                while True:
                    if(GPIO.input(21)):
                        break
                while True:
                    display_3lines("Connecting To:",str(ssid_array[display-1]) ,"Push WPS button then click ",9,offset = 15)
                    if(not GPIO.input(21)):
                        time.sleep(0.01)
                        break
                display_2lines("Pairing","Please Wait...",15)
                os.popen("wpa_cli wps_pbc " + str(mac_array[display-1]))
                # display_custom("something")
                time.sleep(2)
                while(timeout <= 60):
                    ipaddress = os.popen("ifconfig wlan0 | grep 'inet addr' | awk -F: '{print $2}' | awk '{print $1}'").read()
                    addr_len = len(ipaddress)
                    display_3lines("Waiting for an IP",".","IP: " + str(ipaddress),11,offset = 15)
                    if(addr_len > 4 ):
                        print("i have an ip address!!! at " + str(ipaddress))
                        break
                    timeout += 1
                    time.sleep(.25)
                    display_3lines("Waiting for an IP",". .","IP: " + str(ipaddress),11,offset = 15)
                    time.sleep(.25)
                    display_3lines("Waiting for an IP",". . .","IP: " + str(ipaddress),11,offset = 15)
                    time.sleep(.5)
                    if(not GPIO.input(21)):
                        break
                if(timeout >= 300):
                    display_2lines("Connection failed...","Try again",15)
                elif(addr_len < 4):
                    display_2lines("Connection canceled...","Try again",15)
                else:
                    display_2lines("Success!!!","IP: " + str(ipaddress),13)
                time.sleep(5)
            else:
                time.sleep(0.25)
                break
            time.sleep(0.01)
    
        
def settings_menu():
    time.sleep(.25)
    global pos
    pos = 0
    old_display = 0
    exitvar = False
    menudepth = 6
    refresh = 1 
    while exitvar == False:
        if(pos > menudepth):
            pos = menudepth
        elif(pos < 1):
            pos = 1
        display = pos

        #Display Selected Menu
        if (old_display != display or refresh == 1):
            if(display == 1):
                display_2lines(str(display) + ". Device","Info",17)
            elif(display == 2):
                display_2lines(str(display) + ". Re-Pair","Hue Bridge",17)
            elif(display == 3):
                display_2lines(str(display) + ". Shutdown","hueBerry",17)
            elif(display == 4):
                display_2lines(str(display) + ". Flashlight","Function",17)
            elif(display == 5):
                display_2lines(str(display) + ". Connect to","WiFi",17)
            else:
                display_2lines("Back to","Main Menu",17)
            old_display = display
            refresh = 0 
        else:
            time.sleep(0.005)

        # Poll button press and trigger action based on current display
        if(not GPIO.input(21)):
            if(display == 1):
                devinfo_screen()
            elif(display == 2):
                os.popen("rm auth.json")
                pair_hue_bridge()
            elif(display == 3):
                shutdown_hueberry()
            elif(display == 4):
                flashlight_mode()
            elif(display == 5):
                wifi_settings()
            else:
                time.sleep(0.25)
                exitvar = True
            refresh = 1
            pos = display
            time.sleep(0.01)
                #prev_millis = int(round(time.time() * 1000))
    return
        
#----------------------------------------------------------------------------

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
        #font = ImageFont.truetype('BMW_outline.otf', 40)
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

def display_3lines(line1,line2,line3,size,offset):
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
    y_pos += offset
    draw.text((x_pos, y_pos), line2, font=font, fill=255)
    x_pos = (disp.width/2)-(string_width(font,line3)/2)
    y_pos += offset
    draw.text((x_pos, y_pos), line3, font=font, fill=255)
    disp.image(image)
    disp.display()


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
#--------------------------------------------------
# Set up GPIO with internal pull-up
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(4, GPIO.OUT)
#GPIO.output(4,1)
# 128x64 display with hardware I2C
disp = Adafruit_SSD1306.SSD1306_128_64(rst=24)
# Initialize library
disp.begin()
# Get display width and height
width = disp.width
height = disp.height
# Clear display
#disp.clear()
#disp.display()
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

#--------------------------------------------------
#Search to see if an api key exists, if not, get it. 
if os.path.isfile('./auth.json') == False:
    display_3lines("Initial Setup:","hueBerry is","not paired",13,16)
    time.sleep(5)
    while True:
        display_3lines("Attempting Link:","Push Bridge button" ,"Then push button below",11,offset = 15)
        if(not GPIO.input(21)):
            break
    display_custom("Pairing...") 
    ip = authenticate.search_for_bridge()
    authenticate.authenticate('hueBerry',ip)
    authenticate.load_creds()
    api_key = authenticate.api_key
    bridge_ip = authenticate.bridge_ip
    display_2lines("Link Successful!",bridge_ip,12)
    time.sleep(1)
else:
    authenticate.load_creds()
    api_key = authenticate.api_key
    bridge_ip = authenticate.bridge_ip
    api_url = 'http://%s/api/%s' % (bridge_ip,api_key)
    display_2lines("Link Established",bridge_ip,12)
    time.sleep(0.1)

#----------------- set variables---------------
global pos
pos = 0
timeout = 0 
displaytemp = 0 
prev_secs = 0
old_min = 60 
old_display = 0
refresh = 1 

def callback(way):
        global pos
        pos += way
        #print("pos={}".format(pos))

pi = pigpio.pi()
decoder = rotary_encoder.decoder(pi, 16, 20, callback)

while True:

    # Cycle through different displays
    if(pos > 10):
        pos = 10
    elif(pos < 0):
        pos = 0
    display = pos
    #Display Selected Menu 
    if(display == 0):
        cur_min = int(time.strftime("%M"))
        if(old_min != cur_min or refresh == 1):
            display_time()
            old_min = cur_min
            refresh = 0
        timeout = 0
        #Sleep to conserve CPU Cycles
        time.sleep(0.01)
    if(old_display != display):   
        if(display == 1):
            display_2lines(str(display) + ". Turn OFF","all lights slowly",17)
        elif(display == 2):
            display_2lines(str(display) + ". DIM ON","Night lights",17)
        elif(display == 3):
            display_2lines(str(display) + ". FULL ON","all lights",17)
        elif(display == 4):
            display_2lines(str(display) + ". Turn OFF","all lights quickly",17)
        elif(display == 5):
            display_2lines(str(display) + ". After","Dinner",17)
        elif(display == 6):
            display_2lines(str(display) + ". Going","to bed",17)
        elif(display == 7):
            display_2lines(str(display) + ". In bed", "already",17)
        elif(display == 8):
            display_2lines(str(display) + ". Settings", "Menu",13)
        elif(display == 9):
            display_2lines(str(display) + ". Light Control", "Menu",13)
        elif(display == 10):
            display_2lines(str(display) + ". Group Control", "Menu",13)
        old_display = display
        old_min = 60
    elif(display != 0):
        time.sleep(0.005)
        old_min = 60
    
    secs = int(round(time.time())) 
    timeout_secs = secs - prev_secs 
    if(display != 0 and displaytemp != display): 
        prev_secs = secs
        displaytemp = display  
    elif(display != 0 and timeout_secs >= menu_timeout):
        pos = 0
        display_temp = 0 
    elif(display == 0):
        displaytemp = display 
    #if(display != 0):
    #    print timeout_secs
    
    # Poll button press and trigger action based on current display
    if(not GPIO.input(21)):
        if(display == 0):
            # Toggle between 12/24h format
            time_format =  not time_format
            refresh = 1 
            while(not GPIO.input(21)):
                time.sleep(0.01)
        elif(display == 1):
            # Turn off all lights
            display_2lines("Turning all","lights OFF slowly",12)
            #os.popen("sudo ifdown wlan0; sleep 5; sudo ifup --force wlan0")
            debug = os.popen("curl -H \"Accept: application/json\" -X PUT --data '{\"on\":false,\"transitiontime\":100}' " + api_url + "/groups/0/action").read()
            #print(debug)
            time.sleep(10)
        elif(display == 2):
            # Turn on NIGHT lights dim (groups 1,2,3)
            display_2lines("Turning specific","lights on DIM",12)
            debug = os.popen("curl -H \"Accept: application/json\" -X PUT --data '{\"on\":false,\"bri\":1,\"transitiontime\":4}' " + api_url + "/groups/1/action").read()
            hue_lights(lnum = "8",lon = "true",lbri = "1",lsat = "1",lx = "-1",ly = "-1",ltt = "4", lct = "400")
            debug = os.popen("curl -H \"Accept: application/json\" -X PUT --data '{\"on\":false,\"bri\":1,\"transitiontime\":4}' " + api_url + "/groups/2/action").read()
            hue_lights(lnum = "5",lon = "true",lbri = "1",lsat = "200",lx = "0.5015",ly = "0.4153",ltt = "4", lct = "-1")
            debug = os.popen("curl -H \"Accept: application/json\" -X PUT --data '{\"on\":false,\"bri\":1,\"transitiontime\":4}' " + api_url + "/groups/3/action").read()
            hue_groups(lnum = "6",lon = "true",lbri = "1",lsat = "200",lx = "-1",ly = "-1",ltt = "4",lct = "400")
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
            debug = os.popen("curl -H \"Accept: application/json\" -X PUT --data '{\"on\":true,\"bri\":127,\"sat\":1,\"ct\":450,\"transitiontime\":100}' " + api_url + "/groups/1/action").read()
            debug = os.popen("curl -H \"Accept: application/json\" -X PUT --data '{\"on\":true,\"bri\":129,\"sat\":193,\"ct\":432,\"transitiontime\":100}' " + api_url + "/groups/2/action").read()
            debug = os.popen("curl -H \"Accept: application/json\" -X PUT --data '{\"on\":true,\"bri\":254,\"transitiontime\":100}' " + api_url + "/groups/3/action").read()
            debug = os.popen("curl -H \"Accept: application/json\" -X PUT --data '{\"on\":true,\"bri\":1,\"transitiontime\":100}' " + api_url + "/groups/4/action").read()
            debug = os.popen("curl -H \"Accept: application/json\" -X PUT --data '{\"on\":false,\"transitiontime\":100}' " + api_url + "/groups/5/action").read()
            hue_groups(lnum = "6",lon = "true",lbri = "127",lsat = "200",lx = "-1",ly = "-1",ltt = "100",lct = "443")
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
            hue_groups(lnum = "6",lon = "true",lbri = "64",lsat = "200",lx = "-1",ly = "-1",ltt = "100",lct = "443")
        elif(display == 7):
            display_2lines("Turning lights:","Everything dim",12)
            hue_groups(lnum = "1",lon = "true",lbri = "1",lsat = "-1",lx = "-1",ly = "-1",ltt = "100",lct = "381")
            hue_groups(lnum = "2",lon = "false",lbri = "1",lsat = "-1",lx = "-1",ly = "-1",ltt = "100",lct = "439")
            hue_groups(lnum = "3",lon = "true",lbri = "1",lsat = "-1",lx = "-1",ly = "-1",ltt = "100",lct = "-1")
            hue_groups(lnum = "4",lon = "true",lbri = "2",lsat = "-1",lx = "-1",ly = "-1",ltt = "100",lct = "-1")
            hue_groups(lnum = "5",lon = "false",lbri = "1",lsat = "-1",lx = "-1",ly = "-1",ltt = "100",lct = "-1")
            hue_groups(lnum = "6",lon = "true",lbri = "1",lsat = "200",lx = "-1",ly = "-1",ltt = "100",lct = "443")
        elif(display == 8):
            pos = 0
            settings_menu()
        elif(display == 9):
            pos = 0
            l_light_control()
        elif(display == 10):
            pos = 0
            g_light_control()
        time.sleep(0.01)
        #prev_millis = int(round(time.time() * 1000))
        pos = 0

    #time.sleep(0.1)

    

