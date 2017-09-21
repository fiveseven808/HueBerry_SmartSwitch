#!/usr/bin/env python
__version__ = "v051-0920.57.a"
"""
2017-09-20 //57
* Completely unrelated to scene upgrading... but...
+ ADDED THE ABILITY TO SELECT A LIGHT OR GROUP BRIGHTNESS AS A QUICK ACTION! 

2017-09-05 //57
* I really want to update the master branch... So this is some simple modifications to undo the dev features
- Scene upgrader removed and placeholder in place right now
+ Added WPBack's 3d printable model of the hueBerry case!!!
+ Want to push to master! 

2017-07-24 //57
* Have not touched this code in 3 months it seems... I don't remember how this
    works lol. Will attempt to add scene updater tool...
* Scene updater tool will work as follows:
    * User replaces lights in system.
    * Navigate to and run Scene Updater
    * Selects how many lights to replace (and option to cancel)
    * Select 1st light to replace (and option to go back or cancel)
    * Select 1st light to replace with (and option to go back or cancel)
    * Select n light to replace (and option to go back or cancel)
    * Select n light to replace with (and option to go back or cancel)
    * Dict? List? Array? Will be created like {(lights:1, 15),(lights:2, 16),(lights:10, 17)}
    * Menu title: Lights to be replaced
        * Mappings will be displayed in a scrollable style (and option to cancel)
        * Future features:
            * Detect if a mapping error has occured (multiple lights mapped to same light, etc)
            * Click to edit individual Mappings
        * Submit button
        * Binary decision menu to confirm that it will affect all scenes
    * Will parse/grep/replace the "*lights/1*" string with the "*lights/15*"
        string in all files in the scenes directory

2017-04-30 //57
+ Fixed a bug preventing scenes from being created

2017-04-07 //57
* Mega Alpha version
* Forgot to add release notes LOL
+ Intelligent Display handling (kind of)
+ Check I2C display, if not, then SPI, if not then morse code IP address via onboard LED!
+ Rotate display is a thing now (not tested well)
+ Dynamic menu struture implemented
+ Enforced running as root
+ Created a non-root mode
+ Added a demo mode (super alpha)


--------
Things to do
Short term goals:
*
Long term goals:
* Handle adding Wifi without screen? (try except displaying on a screen?)
* If no screen is detected, signal via the onboard led that wifi adding is complete?
* Dynamic (or seperate) Menu for Util mode? (Clock, Util Settings menu, chck for programs not scenes)



--------------------
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
        sudo python hueberry.py [-d] [-m] [-s] [-nb] [-wsl] [-util] [-r180] [-spi] [-h,--help]

    -d              Sets the program to output and take input from the console

    -m              Turns on mirror mode. Outputs to the
                    display as well as the terminal.

    -s,--simulate   Set the updater to simulate mode ( no changes made )

    -nb             No Bridge mode. Run this if debugging with no bridge

    -wsl            Disables weird logging (quick fix for Windows Subsystem for Linux)

    -util           Turns on HB-Utility mode. No hue related options avaliable.
                    Faster boot time too

    -r180           Flip the display 180 degrees

    -spi            Run hueBerry with a SPI driven SSD1306 display vs I2C

    -nr, --noroot   Allows hueBerry to run as a normal user with REDUCED functionality
                    The following features WILL NOT WORK and may crash the program:
                    OTA Updater, Add wifi via txt file, Update via file on sd card,
                    View IP (possibly), Connect to Wifi, Exit to terminal

    -h,--help       Displays this help text
    
    ex: python hueberry.py -d -nb -wsl -nr
    This will allow hueberry to run in WSL without the hue system or root
    """
    print(usage)

import os
#set working directory to script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import sys
#Defaults
debug_argument = 0
mirror_mode = 0
bridge_present = 1
wsl_env = 0
simulation_arg = 0
rotate = 0
curses_test = 0
util_mode = 0
spi_display = 0
rootless = 0
for arg in sys.argv:
    if arg == '-d':
        debug_argument = 1
    if arg == '-m':
        mirror_mode = 1
    if arg == "-nb":
        bridge_present = 0
    if arg == '-wsl':
        wsl_env = 1
    if arg == '-util':
        wsl_env = 1
        bridge_present = 0
        util_mode = 1
    if arg == '-r180':
        rotate = 180
    if arg == '-curses':
        curses_test = 1
    if arg in ("-s","--simulate"):
        simulation_arg = 1
    if arg in ("-spi"):
        spi_display = 1
    if arg in ("-nr","--noroot"):
        rootless = 1
    if arg in ("-h","--help"):
        print_usage()
        sys.exit()

if debug_argument != 1:
    os.popen("python splashscreen.py &")

import threading
import time

import authenticate

import json
import colorsys
import math
import pprint
import hb_display
import hb_encoder
import hb_hue
import hb_settings
import hb_menu
import curses

print "Finished Importing all modules! hopefully this will work!"

# For when I want to measure the time of all of the modules loading
# Using the dot graph method Described here:
# http://stackoverflow.com/questions/767881/time-taken-by-an-import-in-python
#sys.exit()

#--------------------------------------------------------------------------
def get_groups_or_lights_file(g_or_l):
    try:
        demo_mode = settings.get_demo_state()
    except:
        demo_mode = 1 #becuase probably being run as a module for test
    if g_or_l == "g":
        if demo_mode == 0:
            os.popen("curl --connect-timeout 2 --silent -H \"Accept: application/json\" -X GET " + api_url + "/groups  > groups")
            cmdout = os.popen("cat groups").read()
        elif demo_mode == 1:
            cmdout = cat_maybe_demo_file('demo_groups', g_or_l)
    elif g_or_l == "l":
        if demo_mode == 0:
            os.popen("curl --connect-timeout 2 --silent -H \"Accept: application/json\" -X GET " + api_url + "/lights  > lights")
            cmdout = os.popen("cat lights | grep -P -o '\"name\":\".*?\"' | grep -o ':\".*\"' | tr -d '\"' | tr -d ':'").read()
        elif demo_mode == 1:
            file_path = str(os.path.dirname(os.path.abspath(__file__))) + '/demo_lights'
            if os.path.exists(file_path):
                cmdout = os.popen("cat demo_lights  | grep -P -o '\"name\":\".*?\"' | grep -o ':\".*\"' | tr -d '\"' | tr -d ':'").read()
                print "yep"
            else:
                cmdout = os.popen("cat lights  | grep -P -o '\"name\":\".*?\"' | grep -o ':\".*\"' | tr -d '\"' | tr -d ':'").read()
    elif g_or_l == "l_file":
        if demo_mode == 0:
            os.popen("curl --connect-timeout 2 --silent -H \"Accept: application/json\" -X GET " + api_url + "/lights  > lights")
            cmdout = os.popen("cat lights").read()
        elif demo_mode == 1:
            cmdout = cat_maybe_demo_file('demo_lights', 'l')
    return cmdout

def cat_maybe_demo_file(filename, g_or_l):
    file_path = str(os.path.dirname(os.path.abspath(__file__))) + '/' + filename
    if os.path.exists(file_path):
        cmdout = os.popen("cat " + filename).read()
    else:
        if g_or_l == 'g':
            cmdout = os.popen("cat groups").read()
        if g_or_l == 'l':
            cmdout = os.popen("cat lights").read()
    return cmdout

def get_group_names():
    result_array = []
    lstate_a = []
    cmdout = get_groups_or_lights_file("g")
    if not cmdout:
        retry = 1
        while not cmdout:
            if retry >= 3:
                hb_display.display_2lines("An error in ","get_group_name",15)
                debugmsg("error in get_group_names probably lost connection to hub")
                time.sleep(2)
                return 0,0,0,0
                break
            hb_display.display_2lines("Bridge not responding","Retrying " + str(retry),15)
            os.popen("curl --connect-timeout 2 --silent -H \"Accept: application/json\" -X GET " + api_url + "/groups  > groups")
            cmdout = os.popen("cat groups").read()
            retry = retry + 1
    wat = json.loads(cmdout)
    keyvalues =  wat.keys()
    for x, v  in wat.items():
        result_array.append(wat[x]['name'])
        lstate_a.append(wat[x]['action']['on'])
    num_groups = len(result_array)
    arraysize = len(keyvalues)
    return result_array,num_groups,lstate_a,keyvalues

def get_light_names():
    light_names = get_groups_or_lights_file("l")
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
            os.popen("curl --connect-timeout 2 --silent -H \"Accept: application/json\" -X GET " + api_url + "/lights  > lights")
            light_names = os.popen("cat lights | grep -P -o '\"name\":\".*?\"' | grep -o ':\".*\"' | tr -d '\"' | tr -d ':'").read()
            retry = retry + 1
    demo_mode = settings.get_demo_state()
    if demo_mode == 0:
        num_lights = os.popen("cat lights | grep -P -o '\"[0-9]*?\"' | tr -d '\"'").read()
        lstate = os.popen("cat lights | grep -o '\"on\":true,\|\"on\":false,' | tr -d '\"on\":' | tr -d ','").read()
    elif demo_mode == 1:
        file_path = str(os.path.dirname(os.path.abspath(__file__))) + '/demo_lights'
        if os.path.exists(file_path):
            num_lights = os.popen("cat demo_lights | grep -P -o '\"[0-9]*?\"' | tr -d '\"'").read()
            lstate = os.popen("cat demo_lights | grep -o '\"on\":true,\|\"on\":false,' | tr -d '\"on\":' | tr -d ','").read()
        else:
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
    cmdout = get_groups_or_lights_file("l_file")
    #os.popen("cat scene_template.py >> custom_scene" + selected_filendirect + ".py" )
    wat = json.loads(cmdout)
    #Just trying to figure out how to sort this and make it a little nicer... bleh
    #test_wat = sorted(wat.items())
    #pprint.pprint(test_wat)
    #hb_display.display_custom("used jsonloads")
    arraysize = len(wat.keys())
    lstate_a = []
    result_array = []
    bri_array = []
    cmode_array = []
    hue_array = []
    ct_array = []
    sat_array = []
    xy_array = []
    for x, v  in wat.items():
            result_array.append(wat[x]['name'])
            lstate_a.append(wat[x]['state']['on'])
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
    print wat.keys()
    print wat
    while index < len(result_array):
        if(ltt == 4 and lstate_a[index] == False):
            scenecmd = "curl --connect-timeout 2 --silent -H \"Accept: application/json\" -X PUT --data '{\"on\":" + str(lstate_a[index]).lower() + "}' " + api_url + "/lights/" + str(wat.keys()[index]) + "/state"
        else:
            scenecmd = "curl --connect-timeout 2 --silent -H \"Accept: application/json\" -X PUT --data '{\"on\":" + str(lstate_a[index]).lower() + ",\"bri\":" + str(bri_array[index]) + ",\"sat\":" + str(sat_array[index]) + ",\"xy\":" + str(xy_array[index]) + ",\"transitiontime\":" + str(ltt) + ",\"hue\":" + str(hue_array[index]) + "}' " + api_url + "/lights/" + str(wat.keys()[index]) + "/state"
        #hb_display.display_2lines("Writing","Lights " + str(index + 1) + " of " + str(len(result_array)),15)
        print(scenecmd)
        groupnum = index + 1
        # Writes to file in UTF-8 vs using str() as ASCII. This prevents errors I think
        sceneobj.write("#echo \"Set Lights " + wat.keys()[index].encode('utf-8') + " = " + result_array[index].encode('utf-8') + "\"\n")
        sceneobj.write(scenecmd + "\n")
        index += 1
    sceneobj.close
    os.popen("chmod a+x " + scenefile)
    os.popen("chown pi " + scenefile)
    hb_display.display_2lines("Scenefile","Completed!",15)
    status = "completed"
    return status

def hue_lights(lnum,lon,lbri,lsat,lx,ly,lct,ltt,**options):
    #debugmsg("entering hue lights")
    demo_mode = settings.get_demo_state()
    if demo_mode == 0:
        if ('hue' in options):
            result = os.popen("curl --connect-timeout 2 --silent -H \"Accept: application/json\" -X PUT --data '{\"on\":" + str(lon) + ",\"bri\":" + str(lbri) + ",\"sat\":" + str(lsat) + ",\"xy\":[" + str(lx) + "," + str(ly) + "],\"transitiontime\":" + str(ltt) + ",\"hue\":" + str(options['hue']) + "}' " + api_url + "/lights/" + str(lnum) + "/state" ).read()
        else:
            result = os.popen("curl --connect-timeout 2 --silent -H \"Accept: application/json\" -X PUT --data '{\"on\":" + str(lon) + ",\"bri\":" + str(lbri) + ",\"sat\":" + str(lsat) + ",\"xy\":[" + str(lx) + "," + str(ly) + "],\"transitiontime\":" + str(ltt) + ",\"ct\":" + str(lct) + "}' " + api_url + "/lights/" + str(lnum) + "/state" ).read()
        #debugmsg(result)
    else:
        result = "DEMO"
    if not result:
        #print "not brite"
        hb_display.display_2lines("An error in ","hue_lights",17)
        time.sleep(2)
        return
    print(result)
    return result

def hue_groups(lnum, lon = -1, lbri = -1, lsat = -1, lx = -1, ly = -1, lct = -1, ltt = -1,**options):
    #debugmsg("entering hue groups")
    demo_mode = settings.get_demo_state()
    if demo_mode == 0:
        if ('hue' in options):
            #debugmsg("hue and before result")
            result = os.popen("curl --connect-timeout 2 --silent -H \"Accept: application/json\" -X PUT --data '{\"on\":" + str(lon) + ",\"bri\":" + str(lbri) + ",\"sat\":" + str(lsat) + ",\"xy\":[" + str(lx) + "," + str(ly) + "],\"transitiontime\":" + str(ltt) + ",\"hue\":" + str(options['hue']) + "}' " + api_url + "/groups/" + str(lnum) + "/action" ).read()
            #debugmsg("hue and after result")
        else:
            #debugmsg("everything else and before result")
            result = os.popen("curl --connect-timeout 2 -s -m 1 -H \"Accept: application/json\" -X PUT --data '{\"on\":" + str(lon) + ",\"bri\":" + str(lbri) + ",\"sat\":" + str(lsat) + ",\"xy\":[" + str(lx) + "," + str(ly) + "],\"transitiontime\":" + str(ltt) + ",\"ct\":" + str(lct) + "}' " + api_url + "/groups/" + str(lnum) + "/action").read()
            #debugmsg("everything else and after result")
    else:
        result = "DEMO"
    #debugmsg(result)
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
def light_control(mode,selection_only = 0):
    if (mode == "g"):
        hb_display.display_custom("loading groups...")
        name_array,total,lstate_a,keyvalues = get_group_names()
    elif (mode == "l"):
        hb_display.display_custom("loading lights...")
        name_array,num_lights,lstate_a,total = get_light_names()
    elif (mode == "light_select"):
        hb_display.display_custom("loading light explorer...")
        name_array,num_lights,lstate_a,total = get_light_names()
    #global pos
    encoder.pos = 0 #Reset to top menu
    old_display = 0
    refresh = 1
    exitvar = False
    menudepth = total + 1
    if (mode == "light_select"):
        menudepth = menudepth - 1
        #remove ability to reach "exit" menu if light_select
    encoder.wait_for_button_release()
    while exitvar == False:
        if(encoder.pos > menudepth):
            encoder.pos = menudepth
        elif(encoder.pos < 1):
            encoder.pos = 1
        display = encoder.pos

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

        pos,pushed = encoder.get_state()
        # Poll button press and trigger action based on current display
        if(pushed):
            if selection_only == 0:
                if(display <= total):
                    ctmode = 0
                    huemode = 0
                    ctmode = holding_button(500,"Hold for ct...","Entering ct...",21)
                    if(ctmode == 0):
                        if(mode == "g"):
                            g_control(keyvalues[display-1])
                            ctmode = holding_button(500,"Hold for ct...","Entering ct...",21)
                            if (ctmode ==0):
                                hb_display.display_custom("returning from ct...")
                        elif(mode == "l"):
                            l_control(num_lights[display-1])
                            ctmode = holding_button(500,"Hold for ct...","Entering ct...",21)
                            if (ctmode ==0):
                                hb_display.display_custom("returning from ct...")
                    if(ctmode == 1):
                        if(mode == "g"):
                            ct_control(keyvalues[display-1],"g")
                            huemode = holding_button(500,"Hold for hue...","Entering hue...",21)
                            if (huemode == 1):
                                hue_control(keyvalues[display-1],"g")
                                huemode = 0
                            elif(huemode ==0):
                                hb_display.display_custom("returning...")
                            huemode = holding_button(500,"Hold for sat...","Entering sat...",21)
                            if (huemode == 1):
                                sat_control(keyvalues[display-1],"g")
                            elif(huemode ==0):
                                hb_display.display_custom("returning from sat...")
                        elif(mode == "l"):
                            ct_control(num_lights[display-1],"l")
                            huemode = holding_button(500,"Hold for hue...","Entering hue...",21)
                            if (huemode == 1):
                                hue_control(num_lights[display-1],"l")
                                huemode = 0
                            elif(huemode ==0):
                                hb_display.display_custom("returning...")
                            huemode = holding_button(500,"Hold for sat...","Entering sat...",21)
                            if (huemode == 1):
                                sat_control(num_lights[display-1],"l")
                            elif(huemode ==0):
                                hb_display.display_custom("returning...")
                        #finished with sat for l or g
                        pos,pushed = encoder.get_state()
                        while(pushed):
                            hb_display.display_custom("returning...")
                            time.sleep(0.01)
                            pos,pushed = encoder.get_state()
                    if(mode == "g"):
                        name_array,total,lstate_a,keyvalues = get_group_names()
                    elif(mode == "l"):
                        name_array,num_lights,lstate_a,total = get_light_names()
                    refresh = 1
                    encoder.pos = display
                else:
                    time.sleep(0.25)
                    exitvar = True
                time.sleep(0.01)
                #prev_millis = int(round(time.time() * 1000))
            elif selection_only == 1:
                encoder.wait_for_button_release()
                if (mode == "g"):
                    return keyvalues[display-1]
                elif (mode == "l"):
                    return num_lights[display-1]
    return


def l_control(light):
    brite,wholejson = get_huejson_value("l",light,"bri")
    if(brite == -1):
        #print "No lights avaliable"
        return
    #brite = int(brite)      #make integer
    #if brite < 10 and brite >= 0:
    #    brite = 10
    brite = det_if_g_or_l_off("l",light)
    brite = int(brite)
    brite = brite/10        #trim it down to 25 values
    brite = int(brite)      #convert the float down to int agian
    encoder.pos = brite
    exitvar = False
    max_rot_val = 25
    bri_pre = encoder.pos * 10
    refresh = 1
    prev_mills = 0
    while exitvar == False:
        if(encoder.pos > max_rot_val):
            encoder.pos = max_rot_val
        elif(encoder.pos < 0):
            encoder.pos = 0
        mills = int(round(time.time() * 1000))
        millsdiff = mills - prev_mills
        rot_bri = encoder.pos * 10
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
        pos,pushed = encoder.get_state()
        if(pushed):
            exitvar = True
        time.sleep(0.01)

def g_control(group):
    brite,wholejson = get_huejson_value("g",group,"bri")
    if(brite == -1):
        #print "No lights avaliable"
        return
    brite = det_if_g_or_l_off("g",group)
    brite = int(brite)
    brite = brite/10.16        #trim it down to 25 values
    brite = int(brite)      #convert the float down to int agian
    encoder.pos = brite
    exitvar = False
    max_rot_val = 25
    bri_pre = encoder.pos * 10.16
    refresh = 1
    prev_mills = 0
    while exitvar == False:
        if(encoder.pos > max_rot_val):
            encoder.pos = max_rot_val
        elif(encoder.pos < 0):
            encoder.pos = 0
        mills = int(round(time.time() * 1000))
        millsdiff = mills - prev_mills
        rot_bri = encoder.pos * 10.16
        if(bri_pre != rot_bri or refresh ==  1 ):
            hb_display.display_2lines("Group " + str(group),"Bri: " + str(int(rot_bri/2.54)) + "%",17)
            refresh = 0
        if rot_bri <= 0 and rot_bri != bri_pre:
            #print"turning off?"
            huecmd = threading.Thread(target = hue_groups, kwargs={'lnum':group,'lon':"false",'lbri':int(rot_bri),'lsat':"-1",'lx':"-1",'ly':"-1",'ltt':"5",'lct':"-1"})
            huecmd.start()
            bri_pre = rot_bri
        elif(rot_bri != bri_pre and millsdiff > 200):
            #print"millsdiff > 200"
            huecmd = threading.Thread(target = hue_groups, kwargs={'lnum':group,'lon':"true",'lbri':int(rot_bri),'lsat':"-1",'lx':"-1",'ly':"-1",'ltt':"5",'lct':"-1"})
            huecmd.start()
            bri_pre = rot_bri
            prev_mills = mills
        millsdiff = mills - prev_mills
        if(millsdiff > 5000):
            #If 5.0 seconds have passed and nothing has happened, go and refresh the display and reset the miliseconds
            rot_bri = det_if_g_or_l_off("g",group)
            #print "the rot bri is: "+str(rot_bri)
            hb_display.display_2lines("Group " + str(group),"Bri: " + str(int(int(rot_bri)/2.54)) + "%",17)
            prev_mills = mills
        pos,pushed = encoder.get_state()
        if(pushed):
            exitvar = True
        time.sleep(0.01)

def det_if_g_or_l_off(g_or_l,number):
    bri,wholejson = get_huejson_value(g_or_l,number,"bri")
    #print wholejson
    demo_mode = settings.get_demo_state()
    if g_or_l == "g":
        if demo_mode == 0:
            if (wholejson['state']['any_on'] == False):
                bri = 0
        else:
            if (wholejson[number]['state']['any_on'] == False):
                bri = 0
    if g_or_l == "l":
        if demo_mode == 0:
            if (wholejson['state']['on'] == False):
                bri = 0
        else:
            if (wholejson[number]['state']['on'] == False):
                bri = 0
    return bri

def get_huejson_value(g_or_l = 'g',num = 0,type = 'bri'):
    #g_or_l:
    #   Provide "l" if looking up a Light value
    #   Provide "g" if looking up a Group value
    #num:
    #   This is the number of the light or group that you want to retrieve brightness from
    #type:
    #   Provide a type of value you're looking for
    #   bri,ct,hue,sat,type
    #
    #If successful, the function will return back the requested value
    #This function returns -1 if there is nothing returned when the bridge is queried
    #hb_display.display_custom("Loading "+str(type)+"...")
    try:
        demo_mode = settings.get_demo_state()
    except:
        demo_mode = 1 # if we can't load settings, we're probably running tests
    if demo_mode == 0:
        if(g_or_l == "g"):
            wholejson = os.popen("curl --connect-timeout 2 --silent -H \"Accept: application/json\" -X GET " + api_url + "/groups/" + str(num)).read()
        if(g_or_l == "l"):
            wholejson = os.popen("curl --connect-timeout 2 --silent -H \"Accept: application/json\" -X GET  "+ api_url + "/lights/" + str(num)).read()
    else:
        if(g_or_l == "g"):
            wholejson = cat_maybe_demo_file("demo_groups", g_or_l)
        if(g_or_l == "l"):
            wholejson = cat_maybe_demo_file("demo_lights", g_or_l)
    if not wholejson:
        #raise NameError("shit")
        return -1,{}
    print wholejson
    wholejson = json.loads(wholejson)
    num = str(num)
    try:
        if(type == "type" and demo_mode == 0):
            value = wholejson['type']
        elif(type == "type" and demo_mode == 1):
            value = wholejson[num]['type']
        elif(type == "lights" and demo_mode == 0):
            value = wholejson[type]
        elif(type == "lights" and demo_mode == 1):
            value = wholejson[num][type]
        elif demo_mode == 0:
            if g_or_l == "g":
                value = wholejson["action"][type]
            if g_or_l == "l":
                value = wholejson["state"][type]
        elif demo_mode == 1:
            if g_or_l == "g":
                value = wholejson[num]["action"][type]
            if g_or_l == "l":
                value = wholejson[num]["state"][type]
    except:
        value = None
    if not value:
        try:
            if(g_or_l == "l"):
                hb_display.display_2lines("No devices","in lights",17)
            if(g_or_l == "g"):
                hb_display.display_2lines("No devices","in groups",17)
            time.sleep(1)
        except:
            pass # no display is defined, i.e. testing
        value = -1
    return value,wholejson


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
    brite,wholejson = get_huejson_value(mode,device,"ct")
    hb_display.display_custom("loading ct...")
    encoder.wait_for_button_release()
    demo_mode = settings.get_demo_state()
    if demo_mode == 0:
            type = wholejson['type']
    else:
            type = wholejson[device]['type']
    #print type
    if (brite == -1 and type != "Color light"):
        print "something happened"
        if (mode == "l"):
            try:
                hb_display.display_max_text("Light [" + str(wholejson['name']) + "] isn't CT-able", centered = 1, offset = 2)
            except:
                hb_display.display_max_text("Light [" + str(wholejson[device]['name']) + "] isn't CT-able", centered = 1, offset = 2)
        elif (mode == "g"):
            try:
                hb_display.display_max_text("Group [" + str(wholejson['name']) + "] isn't CT-able", centered = 1, offset = 2)
            except:
                hb_display.display_max_text("Group [" + str(wholejson[device]['name']) + "] isn't CT-able", centered = 1, offset = 2)
        time.sleep(2)
        return
    elif(type == "Color light"):
       print("color light was found")
       brite = 500         #Start at warmest color as to not shock eyes lol
    #brite = wat['action']['ct']
    print("THIS IS " +str(brite))
    brite = int(brite)      #make integer
    print("integer= "+str(brite))
    brite = 25-((brite - 153) / 14)
    print ("brite after calc: "+str(brite))
    brite = int(brite)      #convert the float down to int agian
    #global pos
    encoder.pos = brite
    exitvar = False
    max_rot_val = 25
    bri_pre = ((25-encoder.pos) * 14) + 153
    refresh = 1
    prev_mills = 0
    prev_xy = 0
    new_xy = 0
    ct4colorlights = settings.ct_for_color_lights_actions('get')
    while exitvar == False:
        pos,pushed = encoder.get_state()
        if(pos > max_rot_val):
            encoder.pos = max_rot_val
        elif(pos < 0):
            encoder.pos = 0
        mills = int(round(time.time() * 1000))
        millsdiff = mills - prev_mills
        rot_bri = ((max_rot_val-encoder.pos) * 14) + 153
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
                    print("sending ct:"+str(rot_bri))
                    huecmd.start()
            bri_pre = rot_bri
            print rot_bri
            prev_mills = mills
            millsdiff = mills - prev_mills
            prev_xy = 1
        if(mode == "g" and prev_xy != new_xy and millsdiff > 1000):
            #   as of 2/19 the main bit of this function huecmd.start()
            #   has been dsiabled so even though it calculates, it does not send
            #print("inside of the new groupxy function")
            #this function introduces color wobble, but it's good for testing so i'm gonna leave it in lol
            #hb_display.display_custom("setting group via hue")
            hue,sat = ct_to_hue_sat(raw_temp)
            #print hue
            huecmd = threading.Thread(target = hue_groups, kwargs={'lnum':device,'lon':"true",'lbri':"-1",'lsat':sat,'lx':"-1",'ly':"-1",'ltt':"4",'lct':"-1",'hue':hue})
            if ct4colorlights == True:
                set_non_ctable_bulbs_in_group(group = device, raw_temp = raw_temp)
            elif ct4colorlights == "whole_group":
                #print("affecting whole group")
                huecmd.start()
            new_xy = hue
            prev_xy = new_xy
            prev_mills = mills
            millsdiff = mills - prev_mills
            refresh = 1
        #elif(millsdiff > 250):
        #    prev_mills = mills
        if(pushed):
            exitvar = True
        time.sleep(0.01)

def set_non_ctable_bulbs_in_group(group,raw_temp = 5000):
    # Ideally, if this function works, it will attempt to set the CT of all the color but
    # non CTable bulbs in a given group.
    hue,sat = ct_to_hue_sat(raw_temp)
    lights,wholejson = get_huejson_value('g',group,'lights')
    print lights
    lightsjson = json.loads(get_groups_or_lights_file('l_file'))
    #print lightsjson
    for n in lights:
        #print n, lightsjson[n]['type']
        if lightsjson[n]['type'] == 'Color Light':
            huecmd = threading.Thread(target = hue_lights, kwargs={'lnum':n,'lon':"true",'lbri':"-1",'lsat':sat,'lx':"-1",'ly':"-1",'ltt':"4",'lct':"-1",'hue':hue})
            huecmd.start()

def hue_control(device,mode):
    brite,wholejson = get_huejson_value(mode,device,"hue")
    #print wholejson
    hb_display.display_custom("loading hue...")
    encoder.wait_for_button_release()
    if brite == -1:
        print "something happened"
        if (mode == "l"):
            try:
                hb_display.display_max_text("Light [" + str(wholejson['name']) + "] isn't HUE-able", centered = 1, offset = 2)
            except:
                hb_display.display_max_text("Light [" + str(wholejson[device]['name']) + "] isn't HUE-able", centered = 1, offset = 2)
        elif (mode == "g"):
            try:
                hb_display.display_max_text("Group [" + str(wholejson['name']) + "] isn't HUE-able", centered = 1, offset = 2)
            except:
                hb_display.display_max_text("Group [" + str(wholejson[device]['name']) + "] isn't HUE-able", centered = 1, offset = 2)
        time.sleep(2)
        return
    print brite
    brite = int(brite)      #make integer
    brite = brite / 1310
    brite = int(round(brite))      #convert the float down to int agian
    #global pos
    encoder.pos = brite
    exitvar = False
    max_rot_val = 50
    bri_pre = encoder.pos * 1310
    refresh = 1
    prev_mills = 0
    while exitvar == False:
        pos,pushed = encoder.get_state()
        if(pos > max_rot_val):
            encoder.pos = 0
        elif(pos < 0):
            encoder.pos = max_rot_val
        mills = int(round(time.time() * 1000))
        millsdiff = mills - prev_mills
        rot_bri = encoder.pos * 1310
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

        if(pushed):
            exitvar = True
        time.sleep(0.01)

def sat_control(device,mode):
    brite,wholejson = get_huejson_value(mode,device,"sat")
    hb_display.display_custom("loading sat...")
    encoder.wait_for_button_release()
    if brite == -1:
        time.sleep(3)
        return
    brite = int(brite)      #make integer
    brite = brite / 10
    brite = int(round(brite))      #convert the float down to int agian
    #global pos
    encoder.pos = brite
    exitvar = False
    max_rot_val = 25
    bri_pre = encoder.pos * 10
    refresh = 1
    prev_mills = 0
    while exitvar == False:
        pos,pushed = encoder.get_state()
        if(pos > max_rot_val):
            encoder.pos = max_rot_val
        elif(pos < 0):
            encoder.pos = 0
        mills = int(round(time.time() * 1000))
        millsdiff = mills - prev_mills
        rot_bri = encoder.pos * 10
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
        if(pushed):
            exitvar = True
        time.sleep(0.01)


#-------------------------------------------------------------------
#---------------Settings Menu and stuff-----------------------------
#-------------------------------------------------------------------
#Search to see if an api key exists, if not, get it.
def pair_hue_bridge(bridge_present = 1,hbutil = 0):
    if os.path.isfile('./auth.json') == False:
        hb_display.display_3lines("Initial Setup:","hueBerry is","not paired",13,16)
        if bridge_present == 1:
            time.sleep(2)
            msg = "Searching for hue Bridges"
            hb_display.display_max_text(msg,centered = 1,offset = 2)
            ip = authenticate.search_for_bridge()
            if not ip:
                msg = "No Bridges found. Continuing in HB Utility Mode"
                print(msg)
                hb_display.display_max_text(msg,centered = 1,offset = 1)
                hbutil = 1
                time.sleep(2)
            else:
                hb_display.display_2lines(  "Hue Bridge",
                                            "Found!",
                                            size = 15)
                time.sleep(1)
                hbutil = 0
                decision_result = binarydecision(lambda: hb_display.display_3lines(
                                                                                    "Create Creds",
                                                                                    "Or",
                                                                                    "Util Mode?",
                                                                                    size = 13,
                                                                                    offset = 15),
                                                        answer1 = "[ Create Creds ]",
                                                        answer2 = "[ Util Mode ]")
                if decision_result == 1:
                    hb_display.display_3lines(  "Attempting Link:",
                                                "Push Bridge button" ,
                                                "Then push button below",
                                                size = 11,
                                                offset = 15)
                    encoder.wait_for_button_release()
                    while True:
                        pos,pushed = encoder.get_state()
                        if(pushed):
                            break
                        time.sleep(0.01)
                    print("hueberry ip" + str(ip))
                    hb_display.display_custom("Pairing...")
                    authenticate.authenticate('hueBerry',ip)
                elif decision_result == 2:
                    hb_display.display_2lines(  "Running in",
                                                "Util Mode...",
                                                size = 15)
                    encoder.wait_for_button_release()
                    time.sleep(.5)
                    hbutil = 1
    if bridge_present == 1 and hbutil == 0:
        #After a credential file exists
        authenticate.load_creds()
        api_key = authenticate.api_key
        bridge_ip = authenticate.bridge_ip
        api_url = 'http://%s/api/%s' % (bridge_ip,api_key)
        hb_display.display_2lines("Link Established!",bridge_ip,12)
    else:
        api_key = "null"
        bridge_ip = "127.0.0.1"
        api_url = 'http://%s/api/%s' % (bridge_ip,api_key)
        hb_display.display_2lines("FAKE Link Established!",bridge_ip,12)
    time.sleep(0.5)
    return api_url,bridge_ip

def devinfo_screen_old():
    time.sleep(.25)
    #global pos
    encoder.pos = 0 #Reset to top menu
    old_display = 0
    exitvar = False
    menudepth = 4
    refresh = 1
    ipaddress = os.popen("ifconfig wlan0 | grep 'inet addr' | awk -F: '{print $2}' | awk '{print $1}'").read()
    ssid = os.popen("iwconfig wlan0 | grep 'ESSID' | awk '{print $4}' | awk -F\\\" '{print $2}'").read()
    ipaddress_0 = os.popen("ifconfig eth0 | grep 'inet addr' | awk -F: '{print $2}' | awk '{print $1}'").read()
    ipaddress_1 = os.popen("ifconfig eth1 | grep 'inet addr' | awk -F: '{print $2}' | awk '{print $1}'").read()
    while exitvar == False:
        if(encoder.pos > menudepth):
            encoder.pos = menudepth
        elif(encoder.pos < 1):
            encoder.pos = 1
        display = encoder.pos

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
        pos,pushed = encoder.get_state()
        # Poll button press and trigger action based on current display
        if(pushed):
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
            encoder.pos = display
            pos,pushed = encoder.get_state()
            while(pushed):
                pos,pushed = encoder.get_state()
                time.sleep(0.01)
            #prev_millis = int(round(time.time() * 1000))
    return

def devinfo_screen():
    ipaddress = os.popen("ifconfig wlan0 | grep 'inet addr' | awk -F: '{print $2}' | awk '{print $1}'").read()
    ssid = os.popen("iwconfig wlan0 | grep 'ESSID' | awk '{print $4}' | awk -F\\\" '{print $2}'").read()
    ipaddress_0 = os.popen("ifconfig eth0 | grep 'inet addr' | awk -F: '{print $2}' | awk '{print $1}'").read()
    ipaddress_1 = os.popen("ifconfig eth1 | grep 'inet addr' | awk -F: '{print $2}' | awk '{print $1}'").read()
    menu_layout = (lambda: hb_display.display_3lines("hueBerry IP: " + str(ipaddress),"Bridge IP: " + str(bridge_ip) ,"WLAN SSID: " + str(ssid),9,offset = 15), None, lambda: bd_set_result(0),
                    lambda: hb_display.display_3lines("eth0 IP: " + str(ipaddress_0),"eth1 IP: " + str(ipaddress_1) ,"blah",9,offset = 15), None, lambda: bd_set_result(0),
                    "Get hue Hub", "Info", lambda: get_hue_devinfo(),
                    "Version Number", str(__version__), lambda: bd_set_result(0),
                    "Back to", "Settings", "exit")
    settings_menu = hb_menu.Menu_Creator(debug = debug_argument, menu_layout = menu_layout, rotate = rotate, spi_display = spi_display)
    settings_menu.run_2_line_menu()
    encoder.wait_for_button_release()
    return

def get_hue_devinfo():
    hb_display.display_custom("loading groups...")
    name_array,total,lstate_a,keyvalues = get_group_names()
    if not keyvalues:
        hb_display.display_max_text("Looks like you aren't connected to a bridge...           Returning...",offset = 1)
        time.sleep(1)
        return
    maxgroupid = keyvalues[total-1]
    hb_display.display_custom("loading lights...")
    name_array,num_lights,lstate_a,total = get_light_names()
    maxlightid = num_lights[total-1]
    hb_display.display_3lines("Max Light ID: " + str(maxlightid),"Max Group ID: " + str(maxgroupid) ,"something something",9,offset = 15)
    while True:
        time.sleep(0.01)
        pos,pushed = encoder.get_state()
        if(pushed):
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
    pos,pushed = encoder.get_state()
    while True:
        pos,pushed = encoder.get_state()
        if(pushed == 0):
            break
    hb_display.draw_flashlight()
    while True:
        pos,pushed = encoder.get_state()
        if(pushed):
            break
        time.sleep(0.1)

def wifi_settings(debug_file = None):
    hb_display.display_custom("scanning for wifi...")
    #global pos
    encoder.pos = 0 #Reset to top menu
    timeout = 0
    if debug_file == None:
        os.popen("wpa_cli scan")
        time.sleep(3) # to allow the scan results to populate
        os.popen("wpa_cli scan_results > /tmp/wifi_all")
        # Only display WPS enabled points
        os.popen("cat /tmp/wifi_all | grep WPS | sort -r -k3 -n > /tmp/wifi")
        ssids = os.popen("cat /tmp/wifi | awk '{print $5}'").read()
        powers = os.popen("cat /tmp/wifi | awk '{print $3}'").read()
        macs = os.popen("cat /tmp/wifi | awk '{print $1}'").read()
    elif debug_file:
        ssids = os.popen("cat " + str(debugfile) + " | awk '{print $5}'").read()
        powers = os.popen("cat " + str(debugfile) + " | awk '{print $3}'").read()
        macs = os.popen("cat " + str(debugfile) + " | awk '{print $1}'").read()
    ssid_array = ssids.split('\n')
    mac_array = macs.split('\n')
    p_array = powers.split('\n')
    total = len(ssid_array) - 1
    menudepth = total + 1
    while True:
        pos,pushed = encoder.get_state()
        if(pos > menudepth):
            encoder.pos = menudepth
        elif(pos < 0):
            encoder.pos = 0
        display = encoder.pos

        #Display Selected Menu
        if(display == 0):
            hb_display.display_3lines("Scroll to see","Avaliable [WPS]" ,"SSIDs",11,offset = 15)
        elif(display <= total):
            hb_display.display_3lines(str(display) + ". " + str(ssid_array[display-1]),"Signal: " + str(p_array[display-1]),"Connect ?",11,offset = 15)
        else:
            hb_display.display_2lines("Back to","Settings Menu",17)

        # Poll button press and trigger action based on current display
        if(pushed):
            if(display <= total and display > 0):
                timeout = 0
                hb_display.display_3lines("Connecting To:",str(ssid_array[display-1]) ,"Push WPS button then click ",9,offset = 15)
                while True:
                    pos,pushed = encoder.get_state()
                    if(pushed == 0):
                        break
                    time.sleep(0.01)
                while True:
                    hb_display.display_3lines("Connecting To:",str(ssid_array[display-1]) ,"Push WPS button then click ",9,offset = 15)
                    pos,pushed = encoder.get_state()
                    if(pushed):
                        time.sleep(0.01)
                        break
                    time.sleep(0.01)
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
                    pos,pushed = encoder.get_state()
                    if(pushed):
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

def settings_menu(g_scenesdir,util_mode = 0):
    ml = ()
    ml = ml + ("System", "[ Menu ]", lambda: system_menu())
    ml = ml + ("Check for", "Upgrades?", lambda: user_init_upgrade_precheck())
    if util_mode == 0:
        ml = ml + ("Create a", "New Scene", lambda: create_scene_stub(g_scenesdir))
    ml = ml + ("[ Scene ]", "[ Explorer ]", lambda: scene_explorer(g_scenesdir))
    #ml = ml + ("Plugin", "Manager", lambda: plugin_manager(plugins_dir))
    ml = ml + ("Preferences", "[ Menu ]", lambda: preferences_menu())
    ml = ml + ("Back to", "Main Menu", "exit")
    menu_layout = ml
    settings_menu = hb_menu.Menu_Creator(debug = debug_argument, menu_layout = menu_layout, rotate = rotate, spi_display = spi_display)
    settings_menu.run_2_line_menu()
    encoder.wait_for_button_release()
    scene_refresh = 1
    return scene_refresh

def system_menu():
    ml = ()
    ml = ml + ("Device", "Info", lambda: devinfo_screen())
    if util_mode == 0:
        ml = ml + ("Re-Pair", "Hue Bridge", lambda: re_pair_bridge_stub())
    ml = ml + ("Shutdown", "hueBerry", lambda: shutdown_hueberry())
    ml = ml + ("Restart", "hueBerry", lambda: restart_hueberry())
    ml = ml + ("Flashlight", "Function", lambda: flashlight_mode())
    ml = ml + ("Connect to", "WiFi", lambda: wifi_settings())
    if spi_display == 1:
        ml = ml + ("Exit to","Terminal", lambda: exit_dump_to_spi())
    ml = ml + ("Back to", "Main Menu", "exit")
    menu_layout = ml
    system_menu = hb_menu.Menu_Creator(debug = debug_argument, menu_layout = menu_layout, rotate = rotate, spi_display = spi_display)
    system_menu.run_2_line_menu()
    encoder.wait_for_button_release()
    return

def exit_dump_to_spi():
    os.popen("sudo modprobe fbtft_device name=adafruit13m debug=1 speed=2000000 gpios=reset:24,dc:23")
    time.sleep(1)
    os.popen("con2fbmap 1 1")
    os.popen("sudo setfont tom-thumb.psf")
    while True:
        time.sleep(2)
        pos,pushed = encoder.get_state()
        if pushed == 1:
            print("\n\nStarting hueBerry!...")
            time.sleep(2)
            os.popen("sudo "+str(hb_path)+"/r2hb")
            break
    exit()

def preferences_menu():
    menu_layout = ("Toggle time", "Mode 24/12h", lambda: toggle_time_format_stub(),
                    "Change", "Quick actions", lambda: quick_action_settings(),
                    "Toggle Screen", "Saver", lambda: screensaver_settings(),
                    #"Set Night Mode", "Settings", lambda: nightmode_settings(),
                    "Toggle CT for", "Color Lights", lambda: toggle_ct4colorlights(),
                    "Enable CT func for", "Whole Group", lambda: ct4colorlights_whole_group(),
                    "Toggle", "DEMO MODE", lambda: toggle_demo(),
                    "Back to", "Settings", "exit")
    menu = hb_menu.Menu_Creator(debug = debug_argument, menu_layout = menu_layout, rotate = rotate, spi_display = spi_display)
    menu.run_2_line_menu()
    encoder.wait_for_button_release()
    return

def toggle_ct4colorlights():
    settings.ct_for_color_lights_actions('toggle')
    if (settings.ct_for_color_lights_actions('get')):
        hb_display.display_2lines("CT for CL", "Enabled", 17)
    else:
        hb_display.display_2lines("CT for CL", "Disabled", 17)
    time.sleep(1)
    encoder.wait_for_button_release()

def ct4colorlights_whole_group():
    settings.ct_for_color_lights_actions('whole_group')
    hb_display.display_2lines("CT for WHOLE GROUP", "Enabled", 17)
    time.sleep(1)
    encoder.wait_for_button_release()

def toggle_demo():
    # Put something here to toggle the demo mode...
    settings.toggle_demo_state()
    if (settings.get_demo_state()):
        hb_display.display_2lines("DEMO State", "Enabled", 17)
    else:
        hb_display.display_2lines("DEMO State", "Disabled", 17)
    time.sleep(1)
    encoder.wait_for_button_release()


def user_init_upgrade_precheck():
    result = holding_button(2000,"Hold to FORCE", "Will FORCE UPDATE", 21)
    if result == 1:
        user_init_upgrade(force = 1)
    elif result == 0:
        user_init_upgrade()

def re_pair_bridge_stub():
    decision_result = binarydecision(lambda: hb_display.display_2lines( "Confirm Deletetion",
                                                                        "of Bridge Pairing?",
                                                                        size = 17),
                                            answer1 = "[ Delete ]",
                                            answer2 = "[ Cancel ]")
    if decision_result == 2:
        return "CANCELED"
    os.popen("rm auth.json")
    hb_display.display_max_text("Auth file has been successfully DELETED",
                                centered = 1,
                                offset = 2)
    time.sleep(1)
    pair_hue_bridge()
    return "AUTH DELETED FINISHED RE-PAIR ATTEMPT"

def create_scene_stub(g_scenesdir):
    new_scene_creator(g_scenesdir)
    scene_refresh = 1

def toggle_time_format_stub():
    settings.ToggleTimeFormat()
    if (settings.GetTimeFormat()):
        hb_display.display_2lines("Time mode", "Set to 12h", 17)
    else:
        hb_display.display_2lines("Time mode", "Set to 24h", 17)
    time.sleep(1)
    encoder.wait_for_button_release()


#----------------------------------------------------------------------------
#       Quick Actions stuff
#----------------------------------------------------------------------------

def quick_action_settings():
    menu_layout = ("Change quick", "Press action", lambda: settings.set_quick_press_action(set_action("Quick")),
                    "Change long", "Press action", lambda: settings.set_long_press_action(set_action("Long")),
                    "Back to", "Pref Menu", "exit")
    menu = hb_menu.Menu_Creator(debug = debug_argument, menu_layout = menu_layout, rotate = rotate, spi_display = spi_display)
    menu.run_2_line_menu()
    encoder.wait_for_button_release()
    return

def screensaver_settings():
    settings.toggle_screen_blanking()
    if (settings.get_screen_blanking()):
        hb_display.display_2lines("Screen Blanking", "Enabled", 17)
    else:
        hb_display.display_2lines("Screen Blanking", "Disabled", 17)
    time.sleep(1)
    encoder.wait_for_button_release()

def set_action(type):
    result = 0
    menu_layout = ( "Choose " + str(type), "Action:", "BD_TYPE",
                    "Set to", "Do nothing", lambda: bd_set_result(1),
                    "Set to", "Turn all on", lambda: bd_set_result(2),
                    "Set to", "Turn all off", lambda: bd_set_result(3),
                    "Set to", "Toggle all", lambda: bd_set_result(4),
                    "Load a", "Specific Scene", lambda:scene_pick_menu(type = type, g_scenesdir = g_scenesdir),
                    "Toggle a", "Specific Light", lambda:light_group_pick_menu(type = type, mode = "l"),
                    "Toggle a", "Specific Group", lambda:light_group_pick_menu(type = type, mode = "g"),
                    #Not yet implemented... Need to modify hueberry settings and whatever interprets the settings...
                    "Modify", "Specific Light", lambda:light_group_pick_menu(type = type, mode = "l", toggle = "no"),
                    "Modify", "Specific Group", lambda:light_group_pick_menu(type = type, mode = "g", toggle = "no"),
                    "Back to", "Previous Menu", lambda: bd_set_result(-1))
    menu = hb_menu.Menu_Creator(debug = debug_argument, menu_layout = menu_layout, rotate = rotate, spi_display = spi_display)
    result = menu.run_2_line_menu()
    encoder.wait_for_button_release()
    return result - 1

def light_group_pick_menu(type, mode, toggle = "yes"):
    number = light_control( mode = mode,
                            selection_only = 1)
    encoder.wait_for_button_release()
    # [unimplemented] Ask if you want to set a custom brightness?
    if toggle == "yes" :
        action = "set_group_or_light"
    elif toggle == "no" :
        action = "set_group_or_light_FULLCONTROL"
    if type == "Quick":
        settings.set_quick_press_action(action = action,
                                        mode = mode,
                                        number = number)
    if type == "Long":
        settings.set_long_press_action( action = action,
                                        mode = mode,
                                        number = number)
    hb_display.display_2lines(mode+" "+number, "Set!", 17)
    time.sleep(1)
    return -1 #Because I already set it

def scene_pick_menu(type, g_scenesdir):
    selected_file, scene_name = scene_explorer( g_scenesdir = g_scenesdir,
                                                selection_only = 1)
    encoder.wait_for_button_release()
    if type == "Quick":
        settings.set_quick_press_action(action = "set_quick_scene",
                                        number = scene_name,
                                        file_name = selected_file)
    if type == "Long":
        settings.set_long_press_action( action = "set_quick_scene",
                                        number = scene_name,
                                        file_name = selected_file)
    hb_display.display_2lines(scene_name, "Scene Set!", 17)
    time.sleep(1)
    return -1 #Because I already set it
    
#----------------------------------------------------------------------------
#       New Scene Creator
#----------------------------------------------------------------------------
def new_scene_creator(g_scenesdir):
    #This function will utilize get_house_scene_by_light(selected_filendirect,ltt) somehow...
    total_scenes,total_plus_offset,scene_files = get_scene_total(g_scenesdir, offset = 0)
    new_scene_number = total_scenes + 1
    new_scene_name = str(g_scenesdir) + str(new_scene_number) + "_scene.sh"
    print "New scene will be: " + str(new_scene_name)
    ltt = set_scene_transition_time()
    result = get_house_scene_by_light(new_scene_name, ltt)
    debugmsg("ran NEW scene by individual creation with result = " + result)
    return
    
#----------------------------------------------------------------------------
#       Scene Explorer stuff
#----------------------------------------------------------------------------
def scene_explorer(g_scenesdir,selection_only = 0):
    #This function will act like a browser so you can delete or rename certain scenes
    encoder.wait_for_button_release()
    display = 0
    offset = 0 #or 1? for like... instructions so you know where you are?
    scene_refresh = 1
    encoder.pos = 0
    post_offset = 2 # idk what this is. probably to put menu items after the calculated stuff?
    old_display = -1
    exitvar = False
    while exitvar == False:
        # Display the current scene
        if (scene_refresh == 1):
            total_screens, total_plus_offset, scene_files = get_scene_total(g_scenesdir, offset)
            scene_refresh = 0
        menudepth = total_plus_offset + post_offset - 1
        if selection_only == 1:
            menudepth = menudepth - 1
        # Cycle through different displays
        if(encoder.pos > menudepth):
            encoder.pos = menudepth
        elif(encoder.pos < 0):
            encoder.pos = 0
        display = encoder.pos
        if (old_display != display):
            # Normal Mode Scene Explorer Mode
            if selection_only == 0:
                if (display >= offset and display <= (total_plus_offset-1)):
                    hb_display.display_2lines(  "[ " + str(scene_files[display-offset]) + " ]",
                                                "Run | Hold-Edit",
                                                size = 15)
                # Item located at menudepth - 1
                elif (display <= (menudepth - 1)):
                    hb_display.display_2lines(  "Scene Upgrader",
                                                "Thing...",
                                                size = 17)
                else:
                    hb_display.display_2lines(  "Back to",
                                                "Settings Menu",
                                                size = 17)
            # Selection Mode (Re-use case)
            elif selection_only == 1:
                if (display >= offset and display <= (total_plus_offset-1)):
                    hb_display.display_2lines(  "[ " + str(scene_files[display-offset]) + " ]",
                                                "Select",
                                                size = 15)
            old_display = display
        pos,pushed = encoder.get_state()
        if(pushed):
            # Normal Mode Scene Explorer Mode
            if selection_only == 0:
                if(display >= offset and display < (total_plus_offset)):
                    #print display, offset
                    selected_scenenumber = display-offset+1
                    #print selected_scenenumber
                    result = holding_button(1000,
                                            "Hold to edit: " + scene_files[display-offset],
                                            "Will edit: " + scene_files[display-offset],21)
                    selected_file = str(g_scenesdir) + str(scene_files[display-offset])
                    if result == 0:
                        hb_display.display_2lines(  "Turning lights:",
                                                    str(scene_files[display-offset]),
                                                    size = 15)
                        #print "running the below thing"
                        os.popen("\"" + str(selected_file) + "\"")
                        #print(str(selected_file))
                        time.sleep(1)
                        #debugmsg("Running: " + str(scene_files[display-offset]))
                    elif result == 1:
                        scene_manager(selected_file,str(scene_files[display-offset]))
                # Item located at menudepth - 1
                elif (display <= (menudepth - 1)):
                    #Run scene updater
                    output = scene_upgrade_menu(g_scenesdir)
                    #hb_display.display_custom(output)
                    #time.sleep(3)
                else:
                    time.sleep(0.25)
                    exitvar = True
            # Selection Mode (Re-use case)
            elif selection_only == 1:
                return str(g_scenesdir) + str(scene_files[display-offset]), scene_files[display-offset]
                # return selected_file, scene_name #Equivilant
            scene_refresh = 1
            old_display = -1 #to refresh
        time.sleep(0.01)
    return

def scene_manager(file_location, file_name):
    menu_layout = ("Editing Scene:", "[ " + file_name + " ]", lambda: bd_set_result(0), #do nothing lol
                    "Delete", "Scene", lambda: delete_scene(file_location, file_name),
                    #"Rename", "Scene", lambda: rename_scene(file_location, file_name),
                    "Re-Program", "w/Current State", lambda: reprogram_scene(file_location, file_name),
                    "Back to", "Scene Explorer", "exit")
    menu = hb_menu.Menu_Creator(debug = debug_argument, menu_layout = menu_layout, rotate = rotate, spi_display = spi_display)
    menu.run_2_line_menu()
    encoder.wait_for_button_release()
    return

def delete_scene(file_location, file_name):
    print file_location
    decision_result = binarydecision(lambda: hb_display.display_2lines("Really delete",
                                                                        str(file_name) + "?",
                                                                        size = 17),
                        answer1 = "[ Yes ]",
                        answer2 = "[ No ]")
    if (decision_result == 2):
        hb_display.display_2lines("Scene Deletion","Canceled",15)
        time.sleep(1)
        return
    os.popen("rm " + file_location)
    hb_display.display_2lines(str(file_name),"DELETED",17)
    time.sleep(1)
    return "BREAK_MENU"

def reprogram_scene(file_location, file_name):
    # Wait for release is already built in to this function
    ltt = set_scene_transition_time()
    result = get_house_scene_by_light(file_location,ltt)
    return
    
def scene_upgrade_menu(scenes_dir):
    #take the scene dir and then ask what light is now what light
    # i.e. light 6 is now going to become light 7. 
    #recursive function???
    """
    menu_layout = ("Scene Upgrade", "Menu! ->", lambda: bd_set_result(0), #do nothing lol
                    "Start Old bulb", "To New Bulb", lambda: scene_upgrade_phase1(scenes_dir),
                    "Set Group", "To Ignore", lambda: scene_upgrade_phase1(scenes_dir),
                    "Back to", "Scene Explorer", "exit")
    menu = hb_menu.Menu_Creator(debug = debug_argument, menu_layout = menu_layout, rotate = rotate, spi_display = spi_display)
    result = menu.run_2_line_menu()
    result = "startUpgrade"
    if (result[1] == "startUpgrade"):
        #do present a menu to select the old bulb
        
        encoder.wait_for_button_release()
    """
    hb_display.display_2lines("Feature", "Coming Soon!", 14)
    time.sleep(3)
    return
    
def scene_upgrade_phase1(scenes_dir):
    #This needs to be a bulb explorer, not scene  eplorer
    selected_file, scene_name = scene_explorer( g_scenesdir = g_scenesdir,
                                                selection_only = 1)
    encoder.wait_for_button_release()
    # say something like "now pick the new bulb!"
    #then bring up the bulb explorer
    #then say like, upgrading scenes: or something
    #then say that the scene is upgraded! 
    hb_display.display_2lines(scene_name, "Scene Set!", 17)
    time.sleep(1)
    return -1
#----------------------------------------------------------------------------
#       END | Scene Explorer stuff | END
#----------------------------------------------------------------------------

def check_wifi_file(maindirectory):
    ADDWIFIPATH = str(maindirectory) + 'add_wifi.txt'
    print "Checking if add wifi file exists in: " + str(ADDWIFIPATH)
    if os.path.exists(ADDWIFIPATH):
        hb_display.display_3lines("Wifi Creds Detected","Loading File...","Click to continue",13,16)
        while True:
            time.sleep(0.01)
            pos,pushed = encoder.get_state()
            if(pushed):
                break
        ssids = os.popen("cat " + str(ADDWIFIPATH)).read()
        ssid_array = ssids.split('\r\n') # Try and parse out microsoft created files
        if len(ssid_array) <= 1: # If it doesn't parse out properly
            ssid_array = ssids.split('\n') # Try and parse the "normal" way
            if len(ssid_array) <= 1: # If it still doesn't work
                os.rename(ADDWIFIPATH,ADDWIFIPATH + ".FAILED") # File must not be formatted right
                text = "Something went wrong adding wifi... File is not formatted properly"
                debugmsg(text)
                hb_display.display_max_text(text)
                time.sleep(4)
                return #go back and resume boot
        hb_display.display_3lines("SSID: " + ssid_array[0].encode('utf-8'),"PSK: " + ssid_array[1].encode('utf-8'),"Continue?",11,offset = 15)
        while True:
            time.sleep(0.01)
            pos,pushed = encoder.get_state()
            if(pushed):
                break
        with open("/etc/wpa_supplicant/wpa_supplicant.conf", "a") as myfile:
            myfile.write("\nnetwork={\n\tssid=\"" + ssid_array[0].encode('utf-8') + "\"\n\tpsk=\"" + ssid_array[1].encode('utf-8') + "\"\n}\n")
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
            pos,pushed = encoder.get_state()
            if(pushed):
                break
        hb_display.display_3lines("Performing","Upgrade","Please Wait...",13,16)
        os.popen("python " + ADDWIFIPATH)
        while True:
            time.sleep(1)

def user_init_upgrade(force = 0):
    hb_display.display_2lines("Checking for","Updates! :)",15)
    wget_results = os.popen("sudo rm new_upgrade_hb.py; wget https://raw.githubusercontent.com/fiveseven808/HueBerry_SmartSwitch/dev/upgrade_hb.py --output-document=new_upgrade_hb.py -o upgrade.log; cat upgrade.log |  grep ERROR").read()
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
    if os.path.isfile('./upgrade_hb.py') == False:
        #Make sure to make some noise if this is a much older version.
        diff_result = 1
    else:
        diff_result = os.popen("diff upgrade_hb.py new_upgrade_hb.py").read()
    #diff_result = os.popen("diff upgrade_hb.py upgrade_hb.py").read()
    if force == 1:
        diff_result = 1
        # If set to force, put something in diff_result to force it
    if not diff_result:
        print("There are no changes or upgrades avaliable")
        hb_display.display_2lines("You are","up to date! :)",15)
        time.sleep(2)
        return
    else:
        print("It looks like there are changes avaliable. Installing...")
        answer1 = "[ Yes! ]"
        answer2 = "[ Cancel ]"
        #decision_result = binarydecision(lambda: hb_display.display_3lines("Upgrade Avaliable!","Upgrade to","Latest version?",13,offset = 15),answer1,answer2)
        decision_result = user_upgrade_menu()
        if (decision_result != 1):
            hb_display.display_2lines("Canceling...","Returning...",15)
            os.popen("rm new_upgrade_hb.py")
            time.sleep(1)
            return
        hb_display.display_2lines("Upgrading!!!","Please wait...",15)
        import new_upgrade_hb
        #import upgrade_hb
        #upgrader = new_upgrade_hb.upgrader(simulate = 1)
        if diff_result == 1:
            #Legacy switch, currently does nothing...
            upgrader = new_upgrade_hb.Upgrader(legacy = 1)
        else:
            upgrader = new_upgrade_hb.Upgrader(console = debug_argument,simulate = simulation_arg)
        #upgrader = upgrade_hb.upgrader(simulate = 1)
        #Do a blind upgrade lol don't even check
        #upgrader.check_modules_exist()
        upgrader.download_all_modules()
        upgrader.out_with_the_old()
        upgrader.display_exit_msg()
        hb_display.display_2lines("Upgrade Finished!","Rebooting...",13)
        #time.sleep(1)
        print("Upgrade Finished! hueBerry is now rebooting to complete the installation.")
        os.popen("sudo shutdown -r now")
    return

def user_upgrade_menu():
    bd_result = 0
    menu_layout = (lambda:  hb_display.display_3lines("Upgrade Avaliable!","Upgrade to","Latest version?",13,offset = 15), None, "BD_TYPE",
                    "View", "Changelog", lambda: user_upgrade_changelog(),
                    "Choose", "[ Upgrade Now! ]", lambda: bd_set_result(1),
                    "Choose", "[ Cancel ]", lambda: bd_set_result(2))
    menu = hb_menu.Menu_Creator(debug = debug_argument, menu_layout = menu_layout, rotate = rotate, spi_display = spi_display)
    bd_result = menu.run_2_line_menu()
    if bd_result == 0:
        hb_display.display_2lines(  "Returning to",
                                    "Settings Menu",
                                    size = 17)
        time.sleep(1)
    encoder.wait_for_button_release()
    return bd_result

def user_upgrade_changelog():
    import new_upgrade_hb
    #import upgrade_hb
    upgrader = new_upgrade_hb.Upgrader()
    hb_display.display_textbrowser(text = upgrader.display_exit_msg())
    return

def debugmsg(message):
    try:
        global logfile
        global debug_state
        if wsl_env == 0:
            if debug_state == 1:
                current_time = time.strftime("%m / %d / %Y %-H:%M")
                with open(logfile, "a") as myfile:
                    myfile.write(current_time + " " + message + "\n")
            else:
                return
    except:
        pass #Give up if not set, probably running as a module

def holding_button(holding_time_ms,display_before,display_after,button_pin):
    #If this function is activated, then we're checking for the button being held
    #ex: result = holding_button(500,"hold to activate","activating",21)
    held_down = 0
    prev_mills = int(round(time.time() * 1000))
    #pos,pushed = encoder.get_state()
    pushed = 1
    while(pushed):
        mills = int(round(time.time() * 1000))
        millsdiff = mills - prev_mills
        if(millsdiff < holding_time_ms):
            hb_display.display_max_text(display_before,centered = 1,offset = 2)
        elif(millsdiff >= holding_time_ms):
            hb_display.display_max_text(display_after,centered = 1, offset = 2)
            held_down = 1
        pos,pushed = encoder.get_state()
        time.sleep(0.01)
    time.sleep(0.1)
    successvar = held_down
    return successvar

def set_scene_transition_time():
    encoder.pos = 2                 # Start at 40ms
    exitvar = False
    max_rot_val = 150       # 30 sec max transition time
    bri_pre = encoder.pos/5.0       # 20ms per rotation
    refresh = 1
    prev_mills = 0
    encoder.wait_for_button_release()
    while exitvar == False:
        pos,pushed = encoder.get_state()
        if(pos > max_rot_val):
            encoder.pos = max_rot_val
        elif(pos < 0):
            encoder.pos = 0
        mills = int(round(time.time() * 1000))
        millsdiff = mills - prev_mills
        rot_bri = encoder.pos/5.0
        if(bri_pre != rot_bri or refresh ==  1 ):
            if(encoder.pos == 2):
                hb_display.display_2lines("Transition Time",'%.2f'%rot_bri + "* sec",15)
            else:
                hb_display.display_2lines("Transition Time",'%.2f'%rot_bri + " sec",15)
            refresh = 0
        if rot_bri <= 0 and rot_bri != bri_pre:
            bri_pre = rot_bri
        elif(rot_bri != bri_pre and millsdiff > 200):
            bri_pre = rot_bri
            prev_mills = mills
        elif(millsdiff > 200):
            prev_mills = mills
        if(pushed):
            exitvar = True
        time.sleep(0.01)
    transition_time = encoder.pos*2
    return transition_time

def binarydecision(binary_decision_question_function,answer1,answer2):
    bd_result = 0
    menu_layout = (lambda: binary_decision_question_function(), None, "BD_TYPE",
                    "Choose", str(answer1), lambda: bd_set_result(1),
                    "Choose", str(answer2), lambda: bd_set_result(2))
    menu = hb_menu.Menu_Creator(debug = debug_argument, menu_layout = menu_layout, rotate = rotate, spi_display = spi_display)
    bd_result = menu.run_2_line_menu()
    encoder.wait_for_button_release()
    return bd_result

def bd_set_result(value):
    return value

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

def clock_sub_menu():
    result = holding_button(1000,settings.get_quick_press_action_string(),settings.get_long_press_action_string(),21)
    if (result == 0):
        action_dict = settings.get_quick_press_action_dict()
    else:
        action_dict = settings.get_long_press_action_dict()
    action = action_dict["action"]
    mode = action_dict["mode"]
    number = action_dict["number"]
    selected_file = action_dict["file_name"]
    #print action_dict
    #sys.exit()
    if action == 1:
        # Turn lights on
        hue_groups(lnum = "0",lon = "true",lbri = "256",lsat = "256",lx = "-1",ly = "-1",ltt = "-1",lct = "-1")
    elif action == 2:
        # Turn lights off
        hue_groups(lnum = "0",lon = "false",lbri = "256",lsat = "256",lx = "-1",ly = "-1",ltt = "-1",lct = "-1")
    elif action == 3:
        # Toggle lights
        toggle_hue_groups(0)
    elif action == "set_group_or_light":
        if mode == "g":
            toggle_hue_groups(number)
        elif mode == "l":
            toggle_hue_lights(number)
    elif action == "set_group_or_light_FULLCONTROL":
        if mode == "g":
            g_control(number)
        elif mode == "l":
            l_control(number)
    elif action == "set_quick_scene":
        print "Checking if file exists in: " + str(selected_file)
        if os.path.exists(selected_file):
            os.popen("\"" + str(selected_file) + "\"")
        else:
            hb_display.display_max_text(str(number)+"     Does not exist :(",centered = 1, offset = 1)
            time.sleep(2)


def toggle_hue_groups(group,bri = 256):
    discard,wholejson = get_huejson_value("g",group,"bri")
    if discard == -1:
        hb_display.display_custom("Error: can't JSON")
        time.sleep(1)
        return
    if(wholejson['state']['any_on'] == True):
        #print("lights were on. not now")
        hue_groups(lnum = group,lon = "false",lbri = bri,lsat = "256",lx = "-1",ly = "-1",ltt = "-1",lct = "-1")
    else:
        #print("lights were off. not now")
        hue_groups(lnum = group,lon = "true",lbri = bri,lsat = "256",lx = "-1",ly = "-1",ltt = "-1",lct = "-1")

def toggle_hue_lights(light,bri = 256):
    discard,wholejson = get_huejson_value("l",light,"bri")
    if discard == -1:
        hb_display.display_custom("Error: can't JSON")
        time.sleep(1)
        return
    if(wholejson['state']['on'] == True):
        #print("lights were on. not now")
        hue_lights(lnum = light,lon = "false",lbri = bri,lsat = "256",lx = "-1",ly = "-1",ltt = "-1",lct = "-1")
    else:
        #print("lights were off. not now")
        hue_lights(lnum = light,lon = "true",lbri = bri,lsat = "256",lx = "-1",ly = "-1",ltt = "-1",lct = "-1")


def mainloop_test():
    timeout = 0
    displaytemp = 0
    prev_secs = int(round(time.time())) # set to current time
    old_min = 60
    old_display = 0
    refresh = 1
    pushed = 0
    scene_refresh = 1 #Do the initial scene refresh
    debugmsg("-----------------------------")
    debugmsg("Starting hueBerry program version " + __file__)
    offset = 5 #clock (0) + 4 presets
    post_offset = 3 #settings, light, group menu after scenes)
    timeout_secs = 0
    while True:
        if (scene_refresh == 1):
            total_screens,total_plus_offset,scene_files = get_scene_total(g_scenesdir,offset)
            scene_refresh = 0
        menudepth = total_plus_offset + post_offset - 1
        # Cycle through different displays
        if(encoder.pos > menudepth):
            encoder.pos = menudepth
        elif(encoder.pos < 0):
            encoder.pos = 0
        """
        if (    screen_dark == 1 and
                encoder.pos != display and
                settings.get_twist_wake_setting() == 1):
            encoder.pos = 0
            prev_secs = int(round(time.time()))
            refresh = 1
        else:
            display = encoder.pos # because pos is a pre/bounded variable, and encoder.pos has been forced down.
        """
        display = encoder.pos # because pos is a pre/bounded variable, and encoder.pos has been forced down.

        # Check to see if display has timed out
        secs = int(round(time.time()))
        timeout_secs = secs - prev_secs
        if debug_argument == 1:
            print("Screen timeout seconds = "+str(timeout_secs))
        if(display != 0 and displaytemp != display):
            prev_secs = secs
            displaytemp = display
        elif(display != 0 and timeout_secs >= menu_timeout):
            encoder.pos = 0
            display_temp = 0
        elif(display == 0):
            displaytemp = display

        #Display Selected Menu
        if(display == 0):
            if settings.get_screen_blanking() and timeout_secs >= menu_timeout:
                if screen_dark == 0:
                    hb_display.display_custom("")
                    screen_dark = 1
            else:
                screen_dark = 0
                cur_min = int(time.strftime("%M"))
                if(old_min != cur_min or refresh == 1):
                    hb_display.display_time(settings.GetTimeFormat())
                    old_min = cur_min
                    refresh = 0
                timeout = 0
                #Sleep to conserve CPU Cycles
            time.sleep(0.01)
        if (old_display != display):
            if(display == 1):
                hb_display.display_2lines(str(display) + ". Turn OFF","all lights slowly",17)
            elif(display == 2):
                hb_display.display_2lines(str(display) + ". DIM all","Active lights",17)
            elif(display == 3):
                hb_display.display_2lines(str(display) + ". FULL ON","all lights",17)
            elif(display == 4):
                hb_display.display_2lines(str(display) + ". Turn OFF","all lights quickly",17)
            #begin scene selection
            elif(display >= offset and display <= (total_plus_offset-1)):
                hb_display.display_2lines(str(display) + ". " + str(scene_files[display-offset]),"Run?",15)
            elif(display == (menudepth-2)):
                hb_display.display_2lines(str(display) + ". Settings", "[ Menu ]",14)
            elif(display == (menudepth-1)):
                hb_display.display_2lines(str(display) + ". Light Control", "[ Menu ]",14)
            elif(display == (menudepth-0)):
                hb_display.display_2lines(str(display) + ". Group Control", "[ Menu ]",14)
            old_display = display
            old_min = 60
        elif(display != 0):
            time.sleep(0.005)
            old_min = 60

        # Poll button press and trigger action based on current display
        pos,pushed = encoder.get_state() # after loading everything, get state#
        if (pushed):
            if(display == 0):
                clock_sub_menu()
                refresh = 1
            elif(display == 1):
                # Turn off all lights
                hb_display.display_2lines("Turning all","lights OFF slowly",12)
                #os.popen("sudo ifdown wlan0; sleep 5; sudo ifup --force wlan0")
                debug = os.popen("curl --connect-timeout 2 --silent -H \"Accept: application/json\" -X PUT --data '{\"on\":false,\"transitiontime\":100}' " + api_url + "/groups/0/action").read()
                #print(debug)
                time.sleep(1)
                debugmsg("turning all lights off")
            elif(display == 2):
                # Turn on NIGHT lights dim (groups 1,2,3)
                hb_display.display_2lines("Turning All","lights On -> DIM",12)
                hue_groups(lnum = "0",lbri = "1",ltt="100")
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
                encoder.pos = 0
                scene_refresh = settings_menu(g_scenesdir,util_mode = util_mode)
                #InteliDraw_Test()
                scene_refresh = 1 # lol override. this might be useful lol
            elif(display == (menudepth-1)):
                encoder.pos = 0
                light_control("l")
            elif(display == (menudepth)):
                encoder.pos = 0
                light_control("g") #temp for test lol
                #scene_explorer(g_scenesdir)
            refresh = 1
            time.sleep(0.01)
            #prev_millis = int(round(time.time() * 1000))
            encoder.pos = 0
            prev_secs = int(round(time.time()))  #just performed action, reset the screensaver timer

if __name__ == "__main__":
    if not os.geteuid() == 0 and rootless == 0:
        sys.exit('\nhueBerry must be run as root due to file access limitations\nRun with -h for more details\n')
    #------------------------------------------------------------------------------------------------------------------------------
    # Main Loop I think
    global logfile
    hb_path = os.path.dirname(os.path.realpath(__file__))
    if wsl_env == 0:
        logfile = str(hb_path)+"/hueberry.log"
    else:
        logfile = str(hb_path)+"/hueberry.log"

    global debug_state
    debug_state = 1

    menu_timeout = 30 #seconds
    print("hueBerry Started!!! Yay!")#--------------------------------------------------------------------------
    #Create Required directories if they do not exist.
    if rootless == 0:
        maindirectory = "/boot/hueBerry/"
    elif rootless == 1: # Running without root
        maindirectory = hb_path + "/ROOTLESS/"

    if (os.path.isdir(maindirectory) == False):
        os.popen("mkdir \"" + str(maindirectory) + "\"")
        print "Created Directory: " + str(maindirectory)
    g_scenesdir = str(maindirectory) + "scenes/"
    if (os.path.isdir(g_scenesdir) == False):
        os.popen("mkdir \"" + str(g_scenesdir) + "\"")
        print "Created Directory: " + str(g_scenesdir)
    print "Main Directory is: " + str(maindirectory)
    print "Scripts Directory is: " + str(g_scenesdir)
    #Instantiate the hueberry display object
    # Create Display Object
    if(mirror_mode == 1):
        hb_display = hb_display.display(console = 1,mirror = mirror_mode)
    else:
        hb_display = hb_display.display(console = debug_argument,mirror = mirror_mode, rotation = rotate, spi_display = spi_display)
    # Create Encoder Object
    if (debug_argument == 0):
        encoder = hb_encoder.RotaryClass()
    elif (debug_argument == 1):
        if curses_test == 0:
            encoder = hb_encoder.RotaryClass(debug = 1)
        else:
            curses_object = curses.initscr()
            encoder = hb_encoder.RotaryClass(debug = 1, encoder_object = curses_object)
    #--------------------------------------------------
    #prev_millis = 0
    #display = 0
    #--------------------------------------------------
    #Search to see if an Upgrade file exists, if so, run it
    check_upgrade_file(maindirectory)
    #--------------------------------------------------
    #Search to see if an Add Wifi file exists, if so, add it then delete it.
    check_wifi_file(maindirectory)
    #--------------------------------------------------
    #Load the Authentication Module so that the hueberry method can do what it needs to do.
    authenticate = authenticate.Authenticate()
    #Load the Hue API module so that the hueberry can control hue lights lol
    hueapi = hb_hue.HueAPI()
    #Load the settings-module
    settings = hb_settings.Settings()
    api_url,bridge_ip = pair_hue_bridge(bridge_present = bridge_present)
    #------------------------------------------
    # My attempt at methoding the main function...
    mainloop_test()
    #------------------------------------------
