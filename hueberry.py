#!/usr/bin/env python
"""
v042
2017-02-13 1041 //57
gonna attempt to pull everything into the hueberry_api display modules

1403 //57
completed! looks good to me! haven't tested it out on actual hardware yet, but i'm liking it so far... gonna do a console interface spinoff just to see what happens

2021 //57
console display mode and mirror mode now a thing. still no controls. try them out! very cool stuff! 
console mode = redirect all output to console. (but can't control it LOL can control it with hueberry though LOL (but no lcd))
mirror mode = see exactly what's going on on the screen on the hueberry in the console! emulation!!! 
added a little routine in the beginning to go and download the new hueberry_api.py 


v041
2017-02-11 2233 //57
binarydecision() is finished!
Pass it a function for the first thing, then a word or so for the "answers"
We can now cancel scene creation!
Also added a user initiated update function! it'll go and pull the latest file down from github and compare before installing! Then it'll ask the user based on the binarydecision function! 
Lots of goodies today!

2017-02-12 //57
Implemeneted InteliDraw with InteliDraw_Test. Word wrap and scrolling is now a thing!
need to figure out where it goes. 
seperate hueberry_api module is now avaliable! need to integrate it into hueberry.py
    all major display_* functions have been transferred to that module. 
    runs independently to test all functions. fuck yeah!


v040
2017-02-10 1610 //57
Extra bigass update. Just like Windows 10, skipping a few versions to get to v040. I'm pretty sure I made a whole bunch of little updates and just didn't push them to git. Will do my best to document all of them. 
 * Changing the working directory structure for hueBerry
  * Now using /boot/hueBerry/ for upgrade and wifi settings
  * Now using /boot/hueBerry/scenes/ for scene files!
  * Psuedo Global variable used (passed around a lot lol) 
  * "Should" automatically create the directories if they don't exist already
 * Changed get_house_scene_by_light's parameter to selected_filendirect because I'm now passing it a full path name of a file 
  * Can be optimizied a little bit. I'm duplicating the variable right now lol
 * Made a new_scene_creator function that will generate a new scene with a new number based on the amount of scenes that already exist
  * i.e. if 5 scenes exist, regardless of name, the next scene will be named 6_scene.sh
 * Added new scene creation to the settings menu so the main menu is less cluttered. I can't imagine many scenes being created once the inital setup is done by the user
 * check_wifi_file and check_upgrade_file now use the new p-global directory variable
 * get_scene_total now properly queries the p-global scenes directory instead of replying back with static values
  * Also sorts the scenes alphabetically so the user can now order things
 * Adjusted the main menu to properly execute the right script from the new directories (I think?) 
 * Files can now be managed by Windows!
  * Power off the hueBerry
  * Stick the SD card into the Windows machine
  * Navigate to Boot:\hueBerry\scenes\
  * Sort by Name
  * Rename files however you please
  * The order represented by the name sort is the order they will appear on the hueBerry
  * You are free to delete ones you don't use anymore

By the way, all of this except for the new_scene_creator() function has been tested! 


v037
2017-02-04 2319 //57
bunch of tweaks here and there. biggest thing is that scene creation now has adjustable transition time :D that's cool :)
thinking about making the menu system a generic function.... pass it a bunch of things like names of functions to display shit or something
then give it a dict to build the menu from... idk... 
to "start" this effort, i've made a generic/filler funtion called binarydecision() which currently does nothing inttentionally
    the idea behind this function is to put a "yes or no" decision anywhere I want to without hard coding it in. 
    just give pass it a "question" in the form of a display_nlines function, and it'll return whether or not the person
    clicked yes or no. it wont be pretty, but it should be pretty functional. 

v036
2017-02-03 0958 //57
Tweaked the debugmsg string input for WPBack's new method. 
Added easy to turn off global variable for debugmsg: debug_state
Implemented WPBack's new function to enable CT for "Color Lights" as well as calculate and send back hue/sat to a group after 0.5s to look for color wobble 
Cleaned up ct_control a little bit. 
UNTESTED (but runs without any obvious errors) 

2017-02-03 //WPBack
Added the method ct_to_hue_sat that converts color-temperatures into hue and saturation-values scaled for the Hue-system.
For use with the old LED-strip and other lights that doesn't support CT-settings.
Not implemeted anywhere yet though, and not tested enough

v035
2017 0202
Tried to fix the 1g light strips and livingcolors bug where you can't control hue.
added fix in the CT and light_control functions

also tried to fix the CT group and adjusting 1g lightstrips and livingcolors bug, where you adjusting the CT of a group with one of the light strips or living colors in it will not update them.
new algorithm: wait until 0.5 second has passed since the knob was last touched.
*should* work but it's untested as of now
13:32

22:20
so.... the ct group thing doesn't work, but i'm saving it. it turns out that the time it takes for the bridge to convert a value to HSV or XY is too long and varies too much.
i'm keeping this for now becuase it's kind of nice to have, but it really shouldn't be merged into prod.
daniel brought up that hue + sat is actually HSV. python has a built in RGB to HSV conversion function. python kelvin to RGB module exists.
need to merge the two.... will probably worki on the CT+lightcontrol issue first.

2226
gonna attempt to fix the individual CT bit where it should go straght to hue...
2243
looks like i fixed the CT issue. i had quit the CT function too early in my last error handling. it shoul dbe a lot better now... i think there's an else statement somewhere in there that doesn't need to be... i put some markers just in case it gets called....

--------------------
How to run:
sudo python hueberry.py [-d]
http://www.diveintopython.net/scripts_and_streams/command_line_arguments.html 
this is probably a good reference on how to program this in the future 
--------------------
bug:
--------------------
philips hue bug
need to repair when no bridge found

search and test auth?
ping on startup?

check for response?
nothing found?
"""

def print_usage():
    usage = """ 
    How to run:
        sudo python hueberry.py [-d] [-h,--help]
    
    -d          Sets the program to output and take input from the console 
                (input does not work yet)
                
    -m          Turns on mirror mode. needs '-d' to work. Outputs to the 
                display as well as the terminal. 
                
    -h,--help   Displays this help text 
    """
    print(usage)

import os
import os.path
#set working directory to script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

#check requirements for new v042
try:
    import hueberry_api
except:
    print "Downloading the api thing since it doesn't exist"
    os.popen("wget https://raw.githubusercontent.com/fiveseven808/HueBerry_SmartSwitch/dev/hueberry_api.py")
    print "Finished! hopefully this will work!"

import sys
debug_argument = 0
mirror_mode = 0 
for arg in sys.argv:
    if arg == '-d':
        debug_argument = 1
    if arg == '-m':
        mirror_mode = 1
    if arg in ("-h","--help"):
        print_usage()
        sys.exit()

if debug_argument != 1:
    os.popen("python splashscreen.py &")
#    import Adafruit_SSD1306
import RPi.GPIO as GPIO
import pigpio
import rotary_encoder
# temporary enabled until i figure out how to reroute input for console mode

import threading
import time
#from PIL import Image
#from PIL import ImageFont
#from PIL import ImageDraw
import authenticate
import json
import colorsys
import math
import pprint
import hueberry_api


global logfile
logfile = "/home/pi/hueberry.log"

global debug_state
debug_state = 1

menu_timeout = 30 #seconds
print("hueBerry Started!!! Yay!")#--------------------------------------------------------------------------
#Create Required directories if they do not exist. 
maindirectory = "/boot/hueBerry/"
if (os.path.isdir(maindirectory) == False):
    os.popen("sudo mkdir /boot/hueBerry")
    print "Created Directory: " + str(maindirectory)
    
g_scenesdir = str(maindirectory) + "scenes/"
if (os.path.isdir(g_scenesdir) == False):
    os.popen("sudo mkdir /boot/hueBerry/scenes")
    print "Created Directory: " + str(g_scenesdir)
print "Main Directory is: " + str(maindirectory)
print "Scripts Directory is: " + str(g_scenesdir)



#--------------------------------------------------------------------------
def get_group_names():
    result_array = []
    lstate_a = []
    #hb_display.display_2lines("starting","group names",17)
    #debugmsg("starting curl")
    os.popen("curl -H \"Accept: application/json\" -X GET " + api_url + "/groups  > groups")
    #debugmsg("finished curl")
    #hb_display.display_2lines("finished","curl",17)
    cmdout = os.popen("cat groups").read()
    #debugmsg(cmdout)
    if not cmdout:
        #print "not brite"
        retry = 1
        while not cmdout:
            if retry >= 3:
                hb_display.display_2lines("An error in ","get_group_name",15)
                debugmsg("error in get_group_names probably lost connection to hub")
                time.sleep(2)
                return 0,0,0,0
                break
            hb_display.display_2lines("Bridge not responding","Retrying " + str(retry),15)
            os.popen("curl -H \"Accept: application/json\" -X GET " + api_url + "/groups  > groups")
            cmdout = os.popen("cat groups").read()
            retry = retry + 1
    #debugmsg("passed ifstatement")
    #print cmdout
    #os.popen("rm groups")
    wat = json.loads(cmdout)
    keyvalues =  wat.keys()
    #print keyvalues
    for x, v  in wat.items():
        result_array.append(wat[x]['name'])
        lstate_a.append(wat[x]['action']['on'])
    num_groups = len(result_array)
    #print num_groups
    #print result_array
    arraysize = len(keyvalues)
    return result_array,num_groups,lstate_a,keyvalues

def get_light_names():
    os.popen("curl -H \"Accept: application/json\" -X GET " + api_url + "/lights  > lights")
    light_names = os.popen("cat lights | grep -P -o '\"name\":\".*?\"' | grep -o ':\".*\"' | tr -d '\"' | tr -d ':'").read()
    if not light_names:
        #print "not brite"
        retry = 1
        while not light_names:
            if retry == 3:
                hb_display.display_2lines("An error in ","get_light_names",15)
                debugmsg("error in get_light_names probably lost connection to hub")
                time.sleep(2)
                return 0,0,0,0
                break
            hb_display.display_2lines("Bridge not responding","Retrying " + str(retry),15)
            os.popen("curl -H \"Accept: application/json\" -X GET " + api_url + "/lights  > lights")
            light_names = os.popen("cat lights | grep -P -o '\"name\":\".*?\"' | grep -o ':\".*\"' | tr -d '\"' | tr -d ':'").read()
            retry = retry + 1
    num_lights = os.popen("cat lights | grep -P -o '\"[0-9]*?\"' | tr -d '\"'").read()
    lstate = os.popen("cat lights | grep -o '\"on\":true,\|\"on\":false,' | tr -d '\"on\":' | tr -d ','").read()
    #os.popen("rm lights")
    name_array = light_names.split('\n')
    num_array = num_lights.split('\n')
    lstate_a = lstate.split('\n')
    total = len(num_array) - 1
    return name_array,num_array,lstate_a,total


def get_house_scene_by_light(selected_filendirect,ltt):
    rot_bri = ltt/10.0
    #hb_display.display_3lines("Set scene with","Transition Time",'%.2f'%rot_bri + " sec?",13,offset = 15)
    answer1 = "Yes?"
    answer2 = "No?"
    decision_result = binarydecision(lambda: hb_display.display_3lines("Set scene with","Transition Time",'%.2f'%rot_bri + " sec?",13,offset = 15),answer1,answer2)
    print decision_result
    if (decision_result == 2):
        print "Canceled"
        hb_display.display_2lines("Scene Creation","Canceled",15)
        time.sleep(1)
        return "Canceled"
    #Get a fresh groups json file
    hb_display.display_2lines("Grabbing","Light States",15)
    name_array,num_array,lstate_a,total = get_light_names()
    if name_array == 0:
        hb_display.display_3lines("Could not record","Scene","Please Try again",11,offset = 15)
        time.sleep(2)
        return "failed"
    #hb_display.display_custom("ran get light names")
    cmdout = os.popen("cat lights").read()
    #os.popen("cat scene_template.py >> custom_scene" + selected_filendirect + ".py" )
    wat = json.loads(cmdout)
    #Just trying to figure out how to sort this and make it a little nicer... bleh 
    #test_wat = sorted(wat.items())
    #pprint.pprint(test_wat)
    #hb_display.display_custom("used jsonloads")
    keyvalues =  wat.keys()
    arraysize = len(keyvalues)
    lstate_a = []
    result_array = []
    bri_array = []
    cmode_array = []
    hue_array = []
    ct_array = []
    sat_array = []
    xy_array = []
    #hb_display.display_custom("blanked varliables")
    #time.sleep(3)
    for x, v  in wat.items():
            result_array.append(wat[x]['name'])
            lstate_a.append(wat[x]['state']['on'])
            #debugmsg v
    #hb_display.display_custom("ran first for")
    #time.sleep(3)
    for x, v  in wat.items():
        hb_display.display_2lines("Building Array for","Light " + str(x) + " of " + str(len(result_array)),15)
        try:
            bri_array.append(wat[x]['state']['bri'])
        except:
            #debugmsg("errored on item " + x)
            bri_array.append("-1")
        try:
            cmode_array.append(wat[x]['state']['colormode'])
        except:
            #debugmsg("errored on item " + x)
            cmode_array.append("-1")
        try:
            hue_array.append(wat[x]['state']['hue'])
        except:
            #debugmsg("errored on item " + x)
            hue_array.append("-1")
        try:
            ct_array.append(wat[x]['state']['ct'])
        except:
            #debugmsg("errored on item " + x)
            ct_array.append("-1")
        try:
            sat_array.append(wat[x]['state']['sat'])
        except:
            #debugmsg("errored on item " + x)
            sat_array.append("-1")
        try:
            xy_array.append(wat[x]['state']['xy'])
        except:
            #debugmsg("errored on item " + x)
            xy_array.append("-1")
    #time.sleep(3)
    hb_display.display_2lines("Array","built!",15)
    #print result_array
    #print lstate_a
    #print bri_array
    #print cmode_array
    #print hue_array
    #print ct_array
    #print sat_array
    #print xy_array
    #ltt = 100
    #api_url = "http://testbridge/something"
    index = 0
    scenefile = str(selected_filendirect)
    print scenefile
    sceneobj = open(scenefile,"w+")
    sceneobj.write("#!/bin/bash\n#\n#This is a scenefile generated by hueBerry\n\n")
    hb_display.display_2lines("Building","Scene Script!",15)
    while index < len(result_array):
        scenecmd = "curl --silent -H \"Accept: application/json\" -X PUT --data '{\"on\":" + str(lstate_a[index]).lower() + ",\"bri\":" + str(bri_array[index]) + ",\"sat\":" + str(sat_array[index]) + ",\"xy\":" + str(xy_array[index]) + ",\"transitiontime\":" + str(ltt) + ",\"hue\":" + str(hue_array[index]) + "}' " + api_url + "/lights/" + str(keyvalues[index]) + "/state"
        #hb_display.display_2lines("Writing","Lights " + str(index + 1) + " of " + str(len(result_array)),15)
        print(scenecmd)
        groupnum = index + 1
        sceneobj.write("#echo \"Set Lights " + str(keyvalues[index]) + " = " + str(result_array[index]) + "\"\n")
        sceneobj.write(scenecmd + "\n")
        index += 1
    sceneobj.close
    os.popen("chmod a+x " + scenefile)
    os.popen("chown pi " + scenefile)
    hb_display.display_2lines("Scenefile","Completed!",15)
    status = "completed"
    return status

def hue_lights(lnum,lon,lbri,lsat,lx,ly,lct,ltt,**options):
    debugmsg("entering hue lights")
    if ('hue' in options):
        result = os.popen("curl --silent -H \"Accept: application/json\" -X PUT --data '{\"on\":" + str(lon) + ",\"bri\":" + str(lbri) + ",\"sat\":" + str(lsat) + ",\"xy\":[" + str(lx) + "," + str(ly) + "],\"transitiontime\":" + str(ltt) + ",\"hue\":" + str(options['hue']) + "}' " + api_url + "/lights/" + str(lnum) + "/state" ).read()
    else:
        result = os.popen("curl --silent -H \"Accept: application/json\" -X PUT --data '{\"on\":" + str(lon) + ",\"bri\":" + str(lbri) + ",\"sat\":" + str(lsat) + ",\"xy\":[" + str(lx) + "," + str(ly) + "],\"transitiontime\":" + str(ltt) + ",\"ct\":" + str(lct) + "}' " + api_url + "/lights/" + str(lnum) + "/state" ).read()
    debugmsg(result)
    if not result:
        #print "not brite"
        hb_display.display_2lines("An error in ","hue_lights",17)
        time.sleep(2)
        return
    print(result)
    return result
    
def new_scene_creator(g_scenesdir):
    #This function will utilize get_house_scene_by_light(selected_filendirect,ltt) somehow...
    total_scenes,total_plus_offset,scene_files = get_scene_total(g_scenesdir,offset = 0)
    new_scene_number = total_scenes + 1
    new_scene_name = str(g_scenesdir) + str(new_scene_number) + "_scene.sh"
    print "New scene will be: " + str(new_scene_name)
    ltt = set_scene_transition_time()
    result = get_house_scene_by_light(new_scene_name,ltt)
    debugmsg("ran NEW scene by individual creation with result = " + result)
    #THIS FUNCTION IS NOT TESTED
    return
    


def hue_groups(lnum,lon,lbri,lsat,lx,ly,lct,ltt,**options):
    debugmsg("entering hue groups")
    if ('hue' in options):
        #debugmsg("hue and before result")
        result = os.popen("curl --silent -H \"Accept: application/json\" -X PUT --data '{\"on\":" + str(lon) + ",\"bri\":" + str(lbri) + ",\"sat\":" + str(lsat) + ",\"xy\":[" + str(lx) + "," + str(ly) + "],\"transitiontime\":" + str(ltt) + ",\"hue\":" + str(options['hue']) + "}' " + api_url + "/groups/" + str(lnum) + "/action" ).read()
        #debugmsg("hue and after result")
    else:
        #debugmsg("everything else and before result")
        result = os.popen("curl -s -m 1 -H \"Accept: application/json\" -X PUT --data '{\"on\":" + str(lon) + ",\"bri\":" + str(lbri) + ",\"sat\":" + str(lsat) + ",\"xy\":[" + str(lx) + "," + str(ly) + "],\"transitiontime\":" + str(ltt) + ",\"ct\":" + str(lct) + "}' " + api_url + "/groups/" + str(lnum) + "/action").read()
        #debugmsg("everything else and after result")
    debugmsg(result)
    if not result:
        #print "not brite"
        hb_display.display_2lines("An error in ","hue_groups",17)
        time.sleep(2)
        return
    #print(result)
    #debugmsg("printed result")
    return result

#------------------------------------------------------------------------------------
#   This function is the main menu for any light adjustment
#   It displays lights or groups in the hue system and then allows you to control
#       brightness, color temp, hue, and saturation in a fairly intuitive manner
#
#   Usage:
#       Specify "g" or "l" depending if you want to control a group or a light
#       Quick Push:
#           Brightness or exit
#       Long push:
#           CT adjustment or move to next option
#
#   Displays:
#       Group or Light name as you scroll around. Allows you to change most attributes of the light
#------------------------------------------------------------------------------------
def light_control(mode):
    if (mode == "g"):
        hb_display.display_custom("loading groups...")
        name_array,total,lstate_a,keyvalues = get_group_names()
    elif (mode == "l"):
        hb_display.display_custom("loading lights...")
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
                hb_display.display_3lines(str(display) + ". " + str(name_array[display-1]),"Control","ON: " + str(lstate_a[display-1]),11,offset = 15)
            else:
                hb_display.display_2lines("Back","One Level",17)
            old_display = display
            refresh = 0
        else:
            time.sleep(0.005)

        # Poll button press and trigger action based on current display
        if(not GPIO.input(21)):
            if(display <= total):
                ctmode = 0
                huemode = 0
                prev_mills = int(round(time.time() * 1000))
                while(not GPIO.input(21)):
                    mills = int(round(time.time() * 1000))
                    millsdiff = mills - prev_mills
                    if(millsdiff < 500):
                        hb_display.display_custom("hold for ct...")
                    elif(millsdiff >= 500):
                        ctmode = 1
                        break
                while(not GPIO.input(21)):
                    hb_display.display_custom("entering ct...")
                if(ctmode == 0):
                    if(mode == "g"):
                        g_control(keyvalues[display-1])
                        prev_mills = int(round(time.time() * 1000))
                        while(not GPIO.input(21)):
                            mills = int(round(time.time() * 1000))
                            millsdiff = mills - prev_mills
                            if(millsdiff < 500):
                                hb_display.display_custom("hold for ct...")
                            elif(millsdiff >= 500):
                                ctmode = 1
                                break
                        if (ctmode ==0):
                            hb_display.display_custom("returning...")
                        else:
                            while(not GPIO.input(21)):
                                hb_display.display_custom("entering ct...")
                    elif(mode == "l"):
                        l_control(num_lights[display-1])
                        prev_mills = int(round(time.time() * 1000))
                        while(not GPIO.input(21)):
                            mills = int(round(time.time() * 1000))
                            millsdiff = mills - prev_mills
                            if(millsdiff < 500):
                                hb_display.display_custom("hold for ct...")
                            elif(millsdiff >= 500):
                                ctmode = 1
                                break
                        if (ctmode ==0):
                            hb_display.display_custom("returning...")
                        else:
                            while(not GPIO.input(21)):
                                hb_display.display_custom("entering ct...")


                if(ctmode == 1):
                    if(mode == "g"):
                        ct_control(keyvalues[display-1],"g")
                        prev_mills = int(round(time.time() * 1000))
                        while(not GPIO.input(21)):
                            mills = int(round(time.time() * 1000))
                            millsdiff = mills - prev_mills
                            if(millsdiff < 500):
                                hb_display.display_custom("hold for hue...")
                            elif(millsdiff >= 500):
                                huemode = 1
                                break
                        if (huemode == 1):
                            hue_control(keyvalues[display-1],"g")
                            huemode = 0
                        elif(huemode ==0):
                            hb_display.display_custom("returning...")
                        prev_mills = int(round(time.time() * 1000))
                        while(not GPIO.input(21)):
                            mills = int(round(time.time() * 1000))
                            millsdiff = mills - prev_mills
                            if(millsdiff < 500):
                                hb_display.display_custom("hold for sat...")
                            elif(millsdiff >= 500):
                                huemode = 1
                                break
                        if (huemode == 1):
                            sat_control(keyvalues[display-1],"g")
                        elif(huemode ==0):
                            hb_display.display_custom("returning...")

                    elif(mode == "l"):
                        #print("entering modified ct_control")
                        #no you're not lol
                        ct_control(num_lights[display-1],"l")
                        prev_mills = int(round(time.time() * 1000))
                        if (huemode == 0):
                            while(not GPIO.input(21)):
                                mills = int(round(time.time() * 1000))
                                millsdiff = mills - prev_mills
                                if(millsdiff < 500):
                                    hb_display.display_custom("hold for hue...")
                                elif(millsdiff >= 500):
                                    huemode = 1
                                    break
                        if (huemode == 1):
                            hue_control(num_lights[display-1],"l")
                            huemode = 0
                        elif(huemode ==0):
                            hb_display.display_custom("returning...")
                        prev_mills = int(round(time.time() * 1000))
                        while(not GPIO.input(21)):
                            mills = int(round(time.time() * 1000))
                            millsdiff = mills - prev_mills
                            if(millsdiff < 500):
                                hb_display.display_custom("hold for sat...")
                            elif(millsdiff >= 500):
                                huemode = 1
                                break
                        if (huemode == 1):
                            sat_control(num_lights[display-1],"l")
                        elif(huemode ==0):
                            hb_display.display_custom("returning...")
                if(mode == "g"):
                    name_array,total,lstate_a,keyvalues = get_group_names()
                elif(mode == "l"):
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
    hb_display.display_custom("loading brightness...")
    os.popen("curl -H \"Accept: application/json\" -X GET " + api_url + "/groups/" + str(group) + " > brite")
    brite = os.popen("cat brite | grep -o '\"bri\":[0-9]*' | grep -o ':.*' | tr -d ':'").read()
    os.popen("rm brite")
    if not brite:
        #print "not brite"
        hb_display.display_2lines("No devices","in group",17)
        time.sleep(3)
        return
    #else:
    #    print "guess it was brite"
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
            hb_display.display_2lines("Group " + str(group),"Bri: " + str(int(rot_bri/2.5)) + "%",17)
            refresh = 0
        if rot_bri <= 0 and rot_bri != bri_pre:
            #hue_groups(lnum = group,lon = "false",lbri = rot_bri,lsat = "-1",lx = "-1",ly = "-1",ltt = "5", lct = "-1")
            huecmd = threading.Thread(target = hue_groups, kwargs={'lnum':group,'lon':"false",'lbri':rot_bri,'lsat':"-1",'lx':"-1",'ly':"-1",'ltt':"5",'lct':"-1"})
            huecmd.start()
            bri_pre = rot_bri
        elif(rot_bri != bri_pre and millsdiff > 200):
            #hue_groups(lnum = group,lon = "true",lbri = rot_bri,lsat = "-1",lx = "-1",ly = "-1",ltt = "5", lct = "-1")
            huecmd = threading.Thread(target = hue_groups, kwargs={'lnum':group,'lon':"true",'lbri':rot_bri,'lsat':"-1",'lx':"-1",'ly':"-1",'ltt':"5",'lct':"-1"})
            huecmd.start()
            bri_pre = rot_bri
            prev_mills = mills
        elif(millsdiff > 200):
            prev_mills = mills
        if(not GPIO.input(21)):
            exitvar = True
        time.sleep(0.01)

#------------------------------------------------------------------------------------
#Method to convert color temperature into hue and saturation scaled for the Hue-system
#Not tested so much yet
#------------------------------------------------------------------------------------
def ct_to_hue_sat(ct):
    #Method from http://www.tannerhelland.com/4435/convert-temperature-rgb-algorithm-code/
    debugmsg("converting ct " + str(ct) + "into Hue and Saturation")
    #check range
    print ct
    if (ct < 1000):
        ct = 1000.0
    elif (ct > 40000):
        ct = 40000.0
    ct = ct / 100.0
    #calculate red
    if (ct <= 50):
        #red = 255.0
        red = ct - 10.0
        #brian red = 110.4708025861 * math.log(red) - 161.1195681661
        red = 99.4708025861 * math.log(red) - 141.1195681661

    else:
        red = ct - 10.0
        #red = 329.698727446 * math.pow(red, -0.1332047592)
        red = 329.698727446 * math.pow(red, -0.532047592)
        if (red < 0):
            red = 0.0
        elif (red > 255):
            red = 255.0
    #calculate green
    if (ct <= 50):
        green = ct
        #green = 99.4708025861 * math.log(green) - 161.1195681661
        green = 92.4708025861 * math.log(green) - 161.1195681661
        if (green < 0):
            green = 0.0
        elif (green > 255):
            green = 255.0
    else:
        #green = ct - 60.0
        green = ct - 50.0
        #green = 288.1221695283 * math.pow(green, -0.0755148492)
        green = 280.1221695283 * math.pow(green, -0.0755148492)
        if (green < 0):
            green = 0.0
        elif (green > 255):
            green = 255.0
    #calculate blue
    if (ct <= 16):
        blue = 255.0
    else:
        if (ct <= 19):
            blue = 0.0
        else:
            blue = ct - 10.0
            #blue = 138.5177312231 * math.log(blue) - 305.0447927307
            blue = 143.5177312231 * math.log(blue) - 295.0447927307
        if (blue < 0):
            blue = 0.0
        elif (blue > 255):
            blue = 255.0
    #Convert to Hue, Saturation and Value
    print(red,green,blue)
    h, s, v = colorsys.rgb_to_hsv(red/255.0, green/255.0, blue/255.0)
    #debugmsg("raw hue: " + str(360*h) + "saturation: " + str(s*100) + "value: " + str(v))
    h = int(h * 65535)
    s = int(s * 254)
    #h = h + 910
    debugmsg("hue: " + str(h) + "saturation: " + str(s) + "value: " + str(v))
    return h, s

#------------------------------------------------------------------------------------
#   This function controls the color temperature of a light or group
#   Usage:
#       Specify the group or light ID in device
#       Specify "g" or "l" depending if you want to control a group or a light
#
#   Displays:
#       Group or Light ID and current CT level in Kelvin
#------------------------------------------------------------------------------------
def ct_control(device,mode):
    hb_display.display_custom("loading ct...")
    if (mode == "g"):
        os.popen("curl -H \"Accept: application/json\" -X GET " + api_url + "/groups/" + str(device) + " > brite")
    elif (mode == "l"):
        os.popen("curl -H \"Accept: application/json\" -X GET " + api_url + "/lights/" + str(device) + " > brite")
    whole_json = os.popen("cat brite").read()
    wat = json.loads(whole_json)
    brite = os.popen("cat brite | grep -o '\"ct\":[0-9]*' | grep -o ':.*' | tr -d ':'").read()
    #os.popen("rm brite")
    type = wat['type']
    print type
    #if (type == "Color light"):
    #    #print("color light")
    #    hb_display.display_custom("Light " + str(device) + " will Hue instead")
    #    skip_to_hue = 1
    #    time.sleep(.5)
    #    return skip_to_hue
    if (not brite and type != "Color light"):
        print "not brite"
        hb_display.display_2lines("No capable","devices available",12)
        time.sleep(3)
        return
    elif(type == "Color light"):
       print("color light was found") 
       brite = 500         #Start at warmest color as to not shock eyes lol 
    #brite = wat['action']['ct']
    print("THIS IS " +str(brite))
    brite = int(brite)      #make integer
    print brite
    brite = 25-((brite - 153) / 14)
    print brite
    brite = int(brite)      #convert the float down to int agian
    global pos
    pos = brite
    exitvar = False
    max_rot_val = 25
    bri_pre = ((25-pos) * 14) + 153
    refresh = 1
    prev_mills = 0
    prev_xy = 0
    new_xy = 0
    while exitvar == False:
        if(pos > max_rot_val):
            pos = max_rot_val
        elif(pos < 0):
            pos = 0
        mills = int(round(time.time() * 1000))
        millsdiff = mills - prev_mills
        rot_bri = ((max_rot_val-pos) * 14) + 153
        if(bri_pre != rot_bri or refresh ==  1 ):
            raw_temp = int((-12.968*rot_bri)+8484)
            tempcalc = ((-12.968*rot_bri)+8484)/100
            tempcalc = (round(tempcalc))*100
            tempcalc = int(tempcalc)
            if(mode == "g"):
                hb_display.display_2lines("Group " + str(device),"CT: " + str(int(tempcalc)) + "K",17)
            elif(mode == "l"):
                hb_display.display_2lines("Light " + str(device),"CT: " + str(int(tempcalc)) + "K",17)
            refresh = 0
        if(rot_bri != bri_pre and millsdiff > 250):
            #print("inside old group function " + str(mode) + " " + str(prev_xy))
            if(rot_bri > 500):
                rotbri = 500
            if(mode == "g"):
                huecmd = threading.Thread(target = hue_groups, kwargs={'lnum':device,'lon':"true",'lbri':"-1",'lsat':"-1",'lx':"-1",'ly':"-1",'ltt':"4",'lct':rot_bri})
                huecmd.start()
            elif(mode == "l"):
                if (type == "Color light"):
                    hue,sat = ct_to_hue_sat(raw_temp)
                    huecmd = threading.Thread(target = hue_lights, kwargs={'lnum':device,'lon':"true",'lbri':"-1",'lsat':sat,'lx':"-1",'ly':"-1",'ltt':"4",'lct':"-1",'hue':hue})
                    huecmd.start()
                else:
                    huecmd = threading.Thread(target = hue_lights, kwargs={'lnum':device,'lon':"true",'lbri':"-1",'lsat':"-1",'lx':"-1",'ly':"-1",'ltt':"4",'lct':rot_bri})
                    huecmd.start()
            bri_pre = rot_bri
            print rot_bri
            prev_mills = mills
            millsdiff = mills - prev_mills
            prev_xy = 1
        if(mode == "g" and prev_xy != new_xy and millsdiff > 1000):
            print("inside of the new groupxy function")
            #this function introduces color wobble, but it's good for testing so i'm gonna leave it in lol
            hb_display.display_custom("setting group via hue")
            hue,sat = ct_to_hue_sat(raw_temp)
            huecmd = threading.Thread(target = hue_groups, kwargs={'lnum':device,'lon':"true",'lbri':"-1",'lsat':sat,'lx':"-1",'ly':"-1",'ltt':"4",'lct':"-1",'hue':hue})
            #huecmd.start()
            new_xy = hue
            prev_xy = new_xy
            prev_mills = mills
            millsdiff = mills - prev_mills
            refresh = 1
        #elif(millsdiff > 250):
        #    prev_mills = mills
        if(not GPIO.input(21)):
            exitvar = True
        time.sleep(0.01)

def hue_control(device,mode):
    while(not GPIO.input(21)):
        hb_display.display_custom("loading hue...")
    if (mode == "g"):
        os.popen("curl -H \"Accept: application/json\" -X GET " + api_url + "/groups/" + str(device) + " > brite")
    elif (mode == "l"):
        os.popen("curl -H \"Accept: application/json\" -X GET " + api_url + "/lights/" + str(device) + " > brite")
    brite = os.popen("cat brite | grep -o '\"hue\":[0-9]*' | grep -o ':.*' | tr -d ':'").read()
    os.popen("rm brite")
    if not brite:
        #print "not brite"
        hb_display.display_2lines("No devices","in group",17)
        time.sleep(3)
        return
    bri_length = len(brite)
    print bri_length
    if (bri_length > 0):
        brite = int(brite)      #make integer
        brite = brite / 1310
        brite = int(round(brite))      #convert the float down to int agian
    else:
        print "something happened"
        if (mode == "l"):
            hb_display.display_custom("Light " + str(device) + " isn't HUE-able")
        elif (mode == "g"):
            hb_display.display_custom("Group " + str(device) + " isn't HUE-able")
        time.sleep(.5)
        return
    global pos
    pos = brite
    exitvar = False
    max_rot_val = 50
    bri_pre = brite
    refresh = 1
    prev_mills = 0
    while exitvar == False:
        if(pos > max_rot_val):
            pos = 0
        elif(pos < 0):
            pos = max_rot_val
        mills = int(round(time.time() * 1000))
        millsdiff = mills - prev_mills
        rot_bri = pos * 1310
        if(bri_pre != rot_bri or refresh ==  1 ):
            if(mode == "g"):
                hb_display.display_2lines("Group " + str(device),"Hue: " + str(int(rot_bri)) ,17)
            elif(mode == "l"):
                hb_display.display_2lines("Light " + str(device),"Hue: " + str(int(rot_bri)) ,17)
            refresh = 0
        if(rot_bri != bri_pre and millsdiff > 250):
            if(mode == "g"):
                #hue_groups(lnum = device,lon = "true",lbri = "-1",lsat = "-1",lx = "-1",ly = "-1",ltt = "5", lct = "-1", hue = rot_bri)
                huecmd = threading.Thread(target = hue_groups, kwargs={'lnum':device,'lon':"true",'lbri':"-1",'lsat':"250",'lx':"-1",'ly':"-1",'ltt':"5",'lct':"-1",'hue':rot_bri})
                huecmd.start()
            elif(mode == "l"):
                #hue_lights(lnum = device,lon = "true",lbri = "-1",lsat = "-1",lx = "-1",ly = "-1",ltt = "5", lct = "-1", hue = rot_bri)
                huecmd = threading.Thread(target = hue_lights, kwargs={'lnum':device,'lon':"true",'lbri':"-1",'lsat':"250",'lx':"-1",'ly':"-1",'ltt':"5",'lct':"-1",'hue':rot_bri})
                huecmd.start()
            bri_pre = rot_bri
            print rot_bri
            prev_mills = mills
        elif(millsdiff > 250):
            prev_mills = mills

        if(not GPIO.input(21)):
            exitvar = True
        time.sleep(0.01)

def sat_control(device,mode):
    while(not GPIO.input(21)):
        hb_display.display_custom("loading sat...")
    if (mode == "g"):
        os.popen("curl -H \"Accept: application/json\" -X GET " + api_url + "/groups/" + str(device) + " > brite")
    elif (mode == "l"):
        os.popen("curl -H \"Accept: application/json\" -X GET " + api_url + "/lights/" + str(device) + " > brite")
    brite = os.popen("cat brite | grep -o '\"sat\":[0-9]*' | grep -o ':.*' | tr -d ':'").read()
    os.popen("rm brite")
    if not brite:
        #print "not brite"
        hb_display.display_2lines("No devices","in group",17)
        time.sleep(3)
        return
    bri_length = len(brite)
    print bri_length
    if (bri_length > 0):
        brite = int(brite)      #make integer
        brite = brite / 10
        brite = int(round(brite))      #convert the float down to int agian
    else:
        if (mode == "l"):
            hb_display.display_custom("Light " + str(device) + " isn't SAT-able")
        elif (mode == "g"):
            hb_display.display_custom("Group " + str(device) + " isn't SAT-able")
        time.sleep(.5)
        return
    global pos
    pos = brite
    exitvar = False
    max_rot_val = 25
    bri_pre = brite
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
            if(mode == "g"):
                hb_display.display_2lines("Group " + str(device),"Sat: " + str(int(rot_bri)) ,17)
            elif(mode == "l"):
                hb_display.display_2lines("Light " + str(device),"Sat: " + str(int(rot_bri)) ,17)
            refresh = 0
        if(rot_bri != bri_pre and millsdiff > 250):
            if(mode == "g"):
                #hue_groups(lnum = device,lon = "true",lbri = "-1",lsat = rot_bri,lx = "-1",ly = "-1",ltt = "5", lct = "-1")
                huecmd = threading.Thread(target = hue_groups, kwargs={'lnum':device,'lon':"true",'lbri':"-1",'lsat':rot_bri,'lx':"-1",'ly':"-1",'ltt':"5",'lct':"-1"})
                huecmd.start()
            elif(mode == "l"):
                #hue_lights(lnum = device,lon = "true",lbri = "-1",lsat = rot_bri,lx = "-1",ly = "-1",ltt = "5", lct = "-1")
                huecmd = threading.Thread(target = hue_lights, kwargs={'lnum':device,'lon':"true",'lbri':"-1",'lsat':rot_bri,'lx':"-1",'ly':"-1",'ltt':"5",'lct':"-1"})
                huecmd.start()
            bri_pre = rot_bri
            print rot_bri
            prev_mills = mills
        elif(millsdiff > 250):
            prev_mills = mills
        if(not GPIO.input(21)):
            exitvar = True
        time.sleep(0.01)

def l_control(light):
    hb_display.display_custom("loading brightness...")
    os.popen("curl -H \"Accept: application/json\" -X GET  "+ api_url + "/lights/" + str(light) + " > brite")
    brite = os.popen("cat brite | grep -o '\"bri\":[0-9]*' | grep -o ':.*' | tr -d ':'").read()
    os.popen("rm brite")
    if not brite:
        #print "not brite"
        hb_display.display_2lines("No devices","in lights",17)
        time.sleep(3)
        return
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
            hb_display.display_2lines("Light " + str(light),"Bri: " + str(int(rot_bri/2.5)) + "%",17)
            refresh = 0
        if rot_bri <= 0 and rot_bri != bri_pre:
            huecmd = threading.Thread(target = hue_lights, kwargs={'lnum':light,'lon':"false",'lbri':rot_bri,'lsat':"-1",'lx':"-1",'ly':"-1",'ltt':"5",'lct':"-1"})
            huecmd.start()
            bri_pre = rot_bri
        elif(rot_bri != bri_pre and millsdiff > 100):
            huecmd = threading.Thread(target = hue_lights, kwargs={'lnum':light,'lon':"true",'lbri':rot_bri,'lsat':"-1",'lx':"-1",'ly':"-1",'ltt':"5",'lct':"-1"})
            huecmd.start()
            bri_pre = rot_bri
            prev_mills = mills
        elif(millsdiff > 100):
            prev_mills = mills

        if(not GPIO.input(21)):
            exitvar = True
        time.sleep(0.01)
#-------------------------------------------------------------------
#---------------Settings Menu and stuff-----------------------------
#-------------------------------------------------------------------
def pair_hue_bridge():
    pos = 0
    if os.path.isfile('./auth.json') == False:
        while True:
            hb_display.display_3lines("Attempting Link","Push Bridge button" ,"Then push this button",11,offset = 15)
            if(not GPIO.input(21)):
                break
        hb_display.display_custom("doing a thing...")
        ip = authenticate.search_for_bridge()
        authenticate.authenticate('hueBerry',ip)
        authenticate.load_creds()
        api_key = authenticate.api_key
        bridge_ip = authenticate.bridge_ip
        hb_display.display_2lines("Link Successful",bridge_ip,12)
        time.sleep(1)
    else:
        authenticate.load_creds()
        api_key = authenticate.api_key
        bridge_ip = authenticate.bridge_ip
        api_url = 'http://%s/api/%s' % (bridge_ip,api_key)
        hb_display.display_2lines("Already Paired!",bridge_ip,12)
        time.sleep(1)

def devinfo_screen():
    time.sleep(.25)
    global pos
    pos = 0
    old_display = 0
    exitvar = False
    menudepth = 4
    refresh = 1

    ipaddress = os.popen("ifconfig wlan0 | grep 'inet addr' | awk -F: '{print $2}' | awk '{print $1}'").read()
    ssid = os.popen("iwconfig wlan0 | grep 'ESSID' | awk '{print $4}' | awk -F\\\" '{print $2}'").read()
    ipaddress_0 = os.popen("ifconfig eth0 | grep 'inet addr' | awk -F: '{print $2}' | awk '{print $1}'").read()
    ipaddress_1 = os.popen("ifconfig eth1 | grep 'inet addr' | awk -F: '{print $2}' | awk '{print $1}'").read()
    while exitvar == False:
        if(pos > menudepth):
            pos = menudepth
        elif(pos < 1):
            pos = 1
        display = pos

        #Display Selected Menu
        if (old_display != display or refresh == 1):
            if(display == 1):
                hb_display.display_3lines("hueBerry IP: " + str(ipaddress),"Bridge IP: " + str(bridge_ip) ,"WLAN SSID: " + str(ssid),9,offset = 15)
            elif(display == 2):
                hb_display.display_3lines("eth0 IP: " + str(ipaddress_0),"eth1 IP: " + str(ipaddress_1) ,"blah",9,offset = 15)
            elif(display == 3):
                hb_display.display_2lines("Get hue Hub","Info",17)
            else:
                hb_display.display_2lines("Back to","Settings Menu",17)
            old_display = display
            refresh = 0
        else:
            time.sleep(0.005)

        # Poll button press and trigger action based on current display
        if(not GPIO.input(21)):
            if(display == 1):
                ipaddress = os.popen("ifconfig wlan0 | grep 'inet addr' | awk -F: '{print $2}' | awk '{print $1}'").read()
                ssid = os.popen("iwconfig wlan0 | grep 'ESSID' | awk '{print $4}' | awk -F\\\" '{print $2}'").read()
                hb_display.display_3lines("hueBerry IP: " + str(ipaddress),"Bridge IP: " + str(bridge_ip) ,"WLAN SSID: " + str(ssid),9,offset = 15)
            elif(display == 2):
                ipaddress_0 = os.popen("ifconfig eth0 | grep 'inet addr' | awk -F: '{print $2}' | awk '{print $1}'").read()
                ipaddress_1 = os.popen("ifconfig eth1 | grep 'inet addr' | awk -F: '{print $2}' | awk '{print $1}'").read()
                hb_display.display_3lines("eth0 IP: " + str(ipaddress_0),"eth1 IP: " + str(ipaddress_1) ,"blah",9,offset = 15)
            elif(display == 3):
                get_hue_devinfo()
            else:
                time.sleep(0.25)
                exitvar = True
            refresh = 1
            pos = display
            while(not GPIO.input(21)):
                time.sleep(0.01)
            #prev_millis = int(round(time.time() * 1000))
    return

def get_hue_devinfo():
    hb_display.display_custom("loading groups...")
    name_array,total,lstate_a,keyvalues = get_group_names()
    maxgroupid = keyvalues[total-1]
    hb_display.display_custom("loading lights...")
    name_array,num_lights,lstate_a,total = get_light_names()
    maxlightid = num_lights[total-1]
    hb_display.display_3lines("Max Light ID: " + str(maxlightid),"Max Group ID: " + str(maxgroupid) ,"something something",9,offset = 15)
    while True:
        time.sleep(0.01)
        if(not GPIO.input(21)):
            break

def shutdown_hueberry():
    hb_display.display_3lines("Shutting down now...","Don't remove power" ,"Until Display is off",11,offset = 15)
    os.popen("sudo shutdown now")
    while True:
        time.sleep(1)

def restart_hueberry():
    hb_display.display_3lines("Restarting now...","Don't remove power" ,"Please Wait",11,offset = 15)
    os.popen("sudo shutdown -r now")
    while True:
        time.sleep(1)

def flashlight_mode():
    while True:
        if(GPIO.input(21)):
            break
    hb_display.draw_flashlight()
    while True:
        if(not GPIO.input(21)):
            break
        time.sleep(0.1)

def wifi_settings():
    hb_display.display_custom("scanning for wifi...")
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
            hb_display.display_3lines("Scroll to see","Avaliable [WPS]" ,"SSIDs",11,offset = 15)
        elif(display <= total):
            hb_display.display_3lines(str(display) + ". " + str(ssid_array[display-1]),"Signal: " + str(p_array[display-1]),"Connect ?",11,offset = 15)
        else:
            hb_display.display_2lines("Back to","Settings Menu",17)

        # Poll button press and trigger action based on current display
        if(not GPIO.input(21)):
            if(display <= total and display > 0):
                timeout = 0
                hb_display.display_3lines("Connecting To:",str(ssid_array[display-1]) ,"Push WPS button then click ",9,offset = 15)
                while True:
                    if(GPIO.input(21)):
                        break
                while True:
                    hb_display.display_3lines("Connecting To:",str(ssid_array[display-1]) ,"Push WPS button then click ",9,offset = 15)
                    if(not GPIO.input(21)):
                        time.sleep(0.01)
                        break
                hb_display.display_2lines("Pairing","Please Wait...",15)
                os.popen("wpa_cli wps_pbc " + str(mac_array[display-1]))
                # hb_display.display_custom("something")
                time.sleep(2)
                while(timeout <= 60):
                    ipaddress = os.popen("ifconfig wlan0 | grep 'inet addr' | awk -F: '{print $2}' | awk '{print $1}'").read()
                    addr_len = len(ipaddress)
                    hb_display.display_3lines("Waiting for an IP",".","IP: " + str(ipaddress),11,offset = 15)
                    if(addr_len > 4 ):
                        print("i have an ip address!!! at " + str(ipaddress))
                        break
                    timeout += 1
                    time.sleep(.25)
                    hb_display.display_3lines("Waiting for an IP",". .","IP: " + str(ipaddress),11,offset = 15)
                    time.sleep(.25)
                    hb_display.display_3lines("Waiting for an IP",". . .","IP: " + str(ipaddress),11,offset = 15)
                    time.sleep(.5)
                    if(not GPIO.input(21)):
                        break
                if(timeout >= 300):
                    hb_display.display_2lines("Connection failed...","Try again",15)
                elif(addr_len < 4):
                    hb_display.display_2lines("Connection canceled...","Try again",15)
                else:
                    hb_display.display_2lines("Success!!!","IP: " + str(ipaddress),13)
                time.sleep(5)
            else:
                time.sleep(0.25)
                break
            time.sleep(0.01)


def settings_menu(g_scenesdir):
    time.sleep(.25)
    global pos
    pos = 0
    old_display = 0
    exitvar = False
    menudepth = 9
    refresh = 1
    scene_refresh = 0
    while exitvar == False:
        if(pos > menudepth):
            pos = menudepth
        elif(pos < 1):
            pos = 1
        display = pos

        #Display Selected Menu
        if (old_display != display or refresh == 1):
            if(display == 1):
                hb_display.display_2lines(str(display) + ". Device","Info",17)
            elif(display == 2):
                hb_display.display_2lines(str(display) + ". Re-Pair","Hue Bridge",17)
            elif(display == 3):
                hb_display.display_2lines(str(display) + ". Shutdown","hueBerry",17)
            elif(display == 4):
                hb_display.display_2lines(str(display) + ". Restart","hueBerry",17)
            elif(display == 5):
                hb_display.display_2lines(str(display) + ". Flashlight","Function",17)
            elif(display == 6):
                hb_display.display_2lines(str(display) + ". Connect to","WiFi",17)
            elif(display == 7):
                hb_display.display_2lines(str(display) + ". Check for","Upgrades?",17)
            elif(display == 8):
                hb_display.display_2lines(str(display) + ". Create a","New Scene",17)
            else:
                hb_display.display_2lines("Back to","Main Menu",17)
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
                restart_hueberry()
            elif(display == 5):
                flashlight_mode()
            elif(display == 6):
                wifi_settings()
            elif(display == 7):
                user_init_upgrade()
            elif(display == 8):
                new_scene_creator(g_scenesdir)
                scene_refresh = 1
            else:
                time.sleep(0.25)
                exitvar = True
            refresh = 1
            pos = display
            while(not GPIO.input(21)):
                time.sleep(0.01)
            #prev_millis = int(round(time.time() * 1000))
    return scene_refresh

#----------------------------------------------------------------------------

#----------------------------------------------------------------------------


def long_press(message,pin):
    prev_mills = int(round(time.time() * 1000))
    while(not GPIO.input(pin)):
        mills = int(round(time.time() * 1000))
        millsdiff = mills - prev_mills
        if(millsdiff < 500):
            hb_display.display_custom("hold for ct...")
        elif(millsdiff >= 500):
            ctmode = 1
            break

def check_wifi_file(maindirectory):
    ADDWIFIPATH = str(maindirectory) + 'add_wifi.txt'
    print "Checking if add wifi file exists in: " + str(ADDWIFIPATH)
    if os.path.exists(ADDWIFIPATH):
        hb_display.display_3lines("Wifi Creds Detected","Loading File...","Click to continue",13,16)
        while True:
            time.sleep(0.01)
            if(not GPIO.input(21)):
                break
        ssids = os.popen("cat " + str(ADDWIFIPATH) + " | awk '{print $1}'").read()
        ssid_array = ssids.split('\n')
        hb_display.display_3lines("SSID: " + str(ssid_array[0]),"PSK: " + str(ssid_array[1]),"Continue?",11,offset = 15)
        while True:
            time.sleep(0.01)
            if(not GPIO.input(21)):
                break
        with open("/etc/wpa_supplicant/wpa_supplicant.conf", "a") as myfile:
            myfile.write("\nnetwork={\n\tssid=\"" + str(ssid_array[0]) + "\"\n\tpsk=\"" + str(ssid_array[1]) + "\"\n}\n")
        os.rename(ADDWIFIPATH,ADDWIFIPATH + ".added")
        hb_display.display_3lines("Added to database!","Rebooting... ","Please Wait",13,16)
        os.popen("sudo shutdown -r now")
        while True:
            time.sleep(1)

def check_upgrade_file(maindirectory):
    ADDWIFIPATH = str(maindirectory) + 'upgrade.py'
    print "Checking if upgrade file exists in: " + str(ADDWIFIPATH)
    if os.path.exists(ADDWIFIPATH):
        hb_display.display_3lines("New Firmware Detected","Loading File...","Click to continue",13,16)
        while True:
            time.sleep(0.01)
            if(not GPIO.input(21)):
                break
        hb_display.display_3lines("Performing","Upgrade","Please Wait...",13,16)
        os.popen("python " + ADDWIFIPATH)
        while True:
            time.sleep(1)
            
def user_init_upgrade():
    hb_display.display_2lines("Checking for","Updates! :)",15)
    #wget_results = os.popen("wget https://raw.githubusercontent.com/fiveseven808/HueBerry_SmartSwitch/master/wrong.py --output-document=something.py -o upgrade.log; cat upgrade.log |  grep ERROR").read()
    wget_results = os.popen("wget https://raw.githubusercontent.com/fiveseven808/HueBerry_SmartSwitch/dev/hueberry.py --output-document=new_hueberry.py -o upgrade.log; cat upgrade.log |  grep ERROR").read()
    #wget_results = os.popen("wget https://raw.githubusercontent.com/fiveseven808/HueBerry_SmartSwitch/master/hueberry.py --output-document=new_hueberry.py -o upgrade.log; cat upgrade.log |  grep ERROR").read()
    if wget_results:
        print("Could not download the file for whatever reason")
        print("Returning to previous state")
        print("There are no changes or upgrades avaliable")
        hb_display.display_2lines("Could not connect","to server :(",13)
        time.sleep(2)
        return
    else:
        print("File Downloaded Successfully! Comparing...")
        hb_display.display_2lines("Comparing","Versions...",15)
    #Change this to an upgrade only file. Smaller, easier and quicker to check if it just contains a version number and a changelog
    diff_result = os.popen("diff hueberry.py new_hueberry.py").read()
    #diff_result = os.popen("diff hueberry.py hueberry.py").read()
    if not diff_result:
        print("There are no changes or upgrades avaliable")
        hb_display.display_2lines("You are","up to date! :)",15)
        time.sleep(2)
        return
    else:
        print("It looks like there are changes avaliable. Installing...")
        answer1 = "Upgrade Now!"
        answer2 = "Cancel"
        decision_result = binarydecision(lambda: hb_display.display_3lines("Upgrade Avaliable!","Upgrade to","Latest version?",13,offset = 15),answer1,answer2)
        if (decision_result != 1):
            hb_display.display_2lines("Canceling...","Returning...",15)
            #os.popen("rm new_hueberry.py")
            time.sleep(1)
            return
        hb_display.display_2lines("Upgrading!!!","Please wait...",15)
        os.popen("sudo mv hueberry.py hueberry_old.py")
        os.popen("sudo mv new_hueberry.py hueberry.py")
        #lol this probably isn't very secure... but if you have access to the pi then you have issues already 
        os.popen("sudo chown pi hueberry.py")
        os.popen("sudo chown pi hueberry_old.py")
        hb_display.display_2lines("Upgrade Finished!","Rebooting...",13)
        #print("Upgrade Finished! Please reboot your hueBerry to complete the installation.")
        os.popen("sudo shutdown -r now")
    return

def debugmsg(message):
    global logfile
    global debug_state
    if debug_state == 1:
        current_time = time.strftime("%m / %d / %Y %-H:%M")
        with open(logfile, "a") as myfile:
            myfile.write(current_time + " " + message + "\n")
    else:
        return

def holding_button(holding_time_ms,display_before,display_after,button_pin):
    #If this function is activated, then we're checking for the button being held
    #ex: result = holding_button(500,"hold to activate","activating",21)
    held_down = 0
    prev_mills = int(round(time.time() * 1000))
    while(not GPIO.input(button_pin)):
        mills = int(round(time.time() * 1000))
        millsdiff = mills - prev_mills
        if(millsdiff < holding_time_ms):
            hb_display.display_custom(display_before)
        elif(millsdiff >= holding_time_ms):
            hb_display.display_custom(display_after)
            held_down = 1
        time.sleep(0.01)
    time.sleep(0.1)
    successvar = held_down
    return successvar
    
def set_scene_transition_time():
    #placeholder 
    #hb_display.display_custom("doing a thing")
    global pos
    pos = 2                 # Start at 40ms
    exitvar = False
    max_rot_val = 150       # 30 sec max transition time
    bri_pre = pos/5.0       # 20ms per rotation
    refresh = 1
    prev_mills = 0
    while exitvar == False: 
        if(pos > max_rot_val):
            pos = max_rot_val
        elif(pos < 0):
            pos = 0
        mills = int(round(time.time() * 1000))
        millsdiff = mills - prev_mills
        rot_bri = pos/5.0
        if(bri_pre != rot_bri or refresh ==  1 ):
            hb_display.display_2lines("Transition Time",'%.2f'%rot_bri + " sec",15)
            refresh = 0
        if rot_bri <= 0 and rot_bri != bri_pre:
            #huecmd = threading.Thread(target = hue_groups, kwargs={'lnum':group,'lon':"false",'lbri':rot_bri,'lsat':"-1",'lx':"-1",'ly':"-1",'ltt':"5",'lct':"-1"})
            #huecmd.start()
            bri_pre = rot_bri
        elif(rot_bri != bri_pre and millsdiff > 200):
            #huecmd = threading.Thread(target = hue_groups, kwargs={'lnum':group,'lon':"true",'lbri':rot_bri,'lsat':"-1",'lx':"-1",'ly':"-1",'ltt':"5",'lct':"-1"})
            #huecmd.start()
            bri_pre = rot_bri
            prev_mills = mills
        elif(millsdiff > 200):
            prev_mills = mills
        if(not GPIO.input(21)):
            exitvar = True
        time.sleep(0.01)
    transition_time = pos*2
    return transition_time
    
def binarydecision(binary_decision_question_function,answer1,answer2):
    #def binarydecision(displayfunction,messagedict,)
    #take input as a function? then run the function. or store it. this will be the "display" thing. i.e. this function will get hb_display.display_3lines(something) passed to it, and then run it as pos == 0 or something... 
    #as of now 2/4/17 this is just a placeholder stolen from the function above. not called, and no functionality has been implemented
    #disassemble question dict
    #line1 = question_line1
    #line2 = question_line2
    global pos
    pos = 0                 # Start at 0
    exitvar = False
    max_rot_val = 2       # binar question
    old_pos = 0       # idk
    refresh = 1
    prev_mills = 0
    while exitvar == False: 
        if(pos > max_rot_val):
            pos = max_rot_val
        elif(pos < 0):
            pos = 0
        mills = int(round(time.time() * 1000))
        millsdiff = mills - prev_mills
        if(old_pos != pos or refresh ==  1 ):
            old_pos = pos
            if (pos == 0):
                #hb_display.display_2lines(str(line1),str(line2),15)
                binary_decision_question_function()
                result = 0
                #print "pos = "+str(pos)
                #print "old pos = "+str(old_pos)
            elif (pos == 1):
                hb_display.display_2lines("Choose",str(answer1),15)
                result = 1
                #print "pos = "+str(pos)
                #print "old pos = "+str(old_pos)
            elif (pos == 2):
                hb_display.display_2lines("Choose",str(answer2),15)
                result = 2
                #print "pos = "+str(pos)
                #print "old pos = "+str(old_pos)
            else:
                print("fuck, something went wrong in binary decision")
            refresh = 0
        if(not GPIO.input(21) and result > 0 ):
            exitvar = True
        time.sleep(0.01)
    return result

def get_scene_total(g_scenesdir,offset):
    #search all of the scenes in the scenes directory
    #count how many there are (maybe dump names into a dict then do a len()?)
    #add that number to the offset
    #direc = "/boot/hueBerry/scenes/"
    direc = g_scenesdir
    scene_files = [i for i in os.listdir(direc)]
    scene_files = sorted(scene_files)
    print "Loading Scene Files: " + str(scene_files)
    total_scenes = len(scene_files)
    #total_scenes = 3           #static value
    total_plus_offset = total_scenes + offset
    #allscenes_dict = ["Scene 1","Scene 2","Scene 3"]   #Static value
    return total_scenes,total_plus_offset,scene_files

#------------------------------------------------------------------------------------------------------------------------------
# Main Loop I think
if debug_argument != 1:
    # Set up GPIO with internal pull-up
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
elif debug_argument == 1:
    width = 128
    height = 64
    #temporary until i figure out how to redirect intput
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
 
#Instantiate the hueberry display object
if (debug_argument == 0): 
    hb_display = hueberry_api.display()
elif (debug_argument == 1):
    if (mirror_mode == 0):
        hb_display = hueberry_api.display(console = 1)
    elif (mirror_mode == 1):
        hb_display = hueberry_api.display(console = 1,mirror = 1)

#--------------------------------------------------
prev_millis = 0
display = 0
time_format = True

#--------------------------------------------------
#Search to see if an Upgrade file exists, if so, run it
check_upgrade_file(maindirectory)
#--------------------------------------------------
#Search to see if an Add Wifi file exists, if so, add it then delete it.
check_wifi_file(maindirectory)


#--------------------------------------------------
#Search to see if an api key exists, if not, get it.
if os.path.isfile('./auth.json') == False:
    hb_display.display_3lines("Initial Setup:","hueBerry is","not paired",13,16)
    time.sleep(5)
    while True:
        hb_display.display_3lines("Attempting Link:","Push Bridge button" ,"Then push button below",11,offset = 15)
        if(not GPIO.input(21)):
            break
    hb_display.display_custom("Pairing...")
    ip = authenticate.search_for_bridge()
    authenticate.authenticate('hueBerry',ip)
    authenticate.load_creds()
    api_key = authenticate.api_key
    bridge_ip = authenticate.bridge_ip
    hb_display.display_2lines("Link Successful!",bridge_ip,12)
    time.sleep(1)
else:
    authenticate.load_creds()
    api_key = authenticate.api_key
    bridge_ip = authenticate.bridge_ip
    api_url = 'http://%s/api/%s' % (bridge_ip,api_key)
    hb_display.display_2lines("Link Established",bridge_ip,12)
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

scene_refresh = 1 #Do the initial scene refresh

def callback(way):
        global pos
        pos += way
        #print("pos={}".format(pos))

pi = pigpio.pi()
decoder = rotary_encoder.decoder(pi, 16, 20, callback)

debugmsg("-----------------------------")
debugmsg("Starting hueBerry program version " + __file__)

offset = 5 #clock (0) + 4 presets
post_offset = 3 #settings, light, group menu after scenes)
while True:    
    if (scene_refresh == 1):
        total_screens,total_plus_offset,scene_files = get_scene_total(g_scenesdir,offset)
        scene_refresh = 0
    menudepth = total_plus_offset + post_offset - 1
    # Cycle through different displays
    if(pos > menudepth):
        pos = menudepth
    elif(pos < 0):
        pos = 0
    display = pos
    #Display Selected Menu
    if(display == 0):
        cur_min = int(time.strftime("%M"))
        if(old_min != cur_min or refresh == 1):
            hb_display.display_time()
            old_min = cur_min
            refresh = 0
        timeout = 0
        #Sleep to conserve CPU Cycles
        time.sleep(0.01)
    if (old_display != display):
        if(display == 1):
            hb_display.display_2lines(str(display) + ". Turn OFF","all lights slowly",17)
        elif(display == 2):
            hb_display.display_2lines(str(display) + ". DIM ON","Night lights",17)
        elif(display == 3):
            hb_display.display_2lines(str(display) + ". FULL ON","all lights",17)
        elif(display == 4):
            hb_display.display_2lines(str(display) + ". Turn OFF","all lights quickly",17)
        #begin scene selection
        elif(display >= offset and display <= (total_plus_offset-1)):
            #print(display, offset, total_plus_offset, menudepth)
            #print(scene_files)
            #print (display-offset)
            hb_display.display_2lines(str(display) + ". " + str(scene_files[display-offset]),"Run?",15)
        elif(display == (menudepth-2)):
            hb_display.display_2lines(str(display) + ". Settings", "Menu",13)
        elif(display == (menudepth-1)):
            hb_display.display_2lines(str(display) + ". Light Control", "Menu",13)
        elif(display == (menudepth-0)):
            hb_display.display_2lines(str(display) + ". Group Control", "Menu",13)
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
            hb_display.display_2lines("Turning all","lights OFF slowly",12)
            #os.popen("sudo ifdown wlan0; sleep 5; sudo ifup --force wlan0")
            debug = os.popen("curl -H \"Accept: application/json\" -X PUT --data '{\"on\":false,\"transitiontime\":100}' " + api_url + "/groups/0/action").read()
            #print(debug)
            time.sleep(1)
            debugmsg("turning all lights off")
        elif(display == 2):
            # Turn on NIGHT lights dim (groups 1,2,3)
            hb_display.display_2lines("Turning specific","lights on DIM",12)
            debug = os.popen("curl -H \"Accept: application/json\" -X PUT --data '{\"on\":false,\"bri\":1,\"transitiontime\":-1}' " + api_url + "/groups/1/action").read()
            hue_lights(lnum = "8",lon = "true",lbri = "1",lsat = "1",lx = "-1",ly = "-1",ltt = "4", lct = "400")
            debug = os.popen("curl -H \"Accept: application/json\" -X PUT --data '{\"on\":false,\"bri\":1,\"transitiontime\":-1}' " + api_url + "/groups/2/action").read()
            hue_lights(lnum = "5",lon = "true",lbri = "1",lsat = "200",lx = "0.5015",ly = "0.4153",ltt = "4", lct = "-1")
            debug = os.popen("curl -H \"Accept: application/json\" -X PUT --data '{\"on\":false,\"bri\":1,\"transitiontime\":-1}' " + api_url + "/groups/3/action").read()
            hue_groups(lnum = "6",lon = "true",lbri = "1",lsat = "200",lx = "-1",ly = "-1",ltt = "4",lct = "400")
            # Turn off front door light
            #print(debug)
            time.sleep(.5)
            debugmsg("turning on night lights dim")
        elif(display == 3):
            hb_display.display_2lines("Turning all","lights on FULL",12)
            hue_groups(lnum = "0",lon = "true",lbri = "254",lsat = "256",lx = "-1",ly = "-1",ltt = "-1",lct = "-1")
            ##turn off front door light... we dont want that...
            #hue_groups(lnum = "5",lon = "false",lbri = "1",lsat = "256",lx = "-1",ly = "-1",ltt = "-1",lct = "-1")
            debugmsg("turning all lights on full")
        elif(display == 4):
            hb_display.display_2lines("Turning all","lights OFF quickly",12)
            hue_groups(lnum = "0",lon = "false",lbri = "256",lsat = "256",lx = "-1",ly = "-1",ltt = "-1",lct = "-1")
            debugmsg("turning all lights off quick")
        elif(display >= offset and display < total_plus_offset):
            #print display, offset
            selected_scenenumber = display-offset+1
            #print selected_scenenumber
            result = holding_button(1000,"Hold to edit: " + scene_files[display-offset],"Will edit: " + scene_files[display-offset],21)
            selected_file = str(g_scenesdir) + str(scene_files[display-offset])
            if result == 0:
                hb_display.display_2lines("Turning lights:",str(scene_files[display-offset]),12)
                #print scene_files[display-offset]
                print "running the below thing"
                #selected_file = str(g_scenesdir) + str(scene_files[display-offset])
                os.popen("\"" + str(selected_file) + "\"")
                print(str(selected_file))
                time.sleep(1)
                debugmsg("Running: " + str(scene_files[display-offset]))
            elif result == 1:
                ltt = set_scene_transition_time()
                result = get_house_scene_by_light(selected_file,ltt)
                debugmsg("Ran scene editing by group with result = " + result)
            else:
                hb_display.display_2lines("Something weird","Happened...",12)
                time.sleep(5)
        elif(display == (menudepth-2)):
            pos = 0
            scene_refresh = settings_menu(g_scenesdir)
            #InteliDraw_Test()
            scene_refresh = 1 # lol override. this might be useful lol 
        elif(display == (menudepth-1)):
            pos = 0
            light_control("l")
        elif(display == (menudepth)):
            pos = 0
            light_control("g")
        time.sleep(0.01)
        #prev_millis = int(round(time.time() * 1000))
        pos = 0

    #time.sleep(0.1)
