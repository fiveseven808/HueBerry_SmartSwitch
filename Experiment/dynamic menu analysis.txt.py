Dynamic menu study

1st pull values from somewhere to get multi array of values
	the ones that matter seem to be the size of the array (can be determined here)
	the state of the lights = dynamic property
	the name of the lights = menu items
	

#Looks like the display section and push button section are two different if statements just like the static menu code. the difference seems to be that the "display" portion seems to be dynamically generated via the following bit of code
menudepth = total + 1

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
    
#-------------------------------
#What we can do is make "total" a dynamic variable that gets set by a function. 
#we'll make the function do something like 
def get_scene_total(offset):
    #search all of the scenes in the scenes directory
    #count how many there are (maybe dump names into a dict then do a len()?) 
    #add that number to the offset
    return total_sceens,total_plus_offset,allscenes_dict
    
#-------------------------------
#Then what we can do is we'll make the display dynamically update like this 
offset = 5 #clock + 4 presets
post_offset = 3 #settings, light, group menu after scenes)
total_screens,total_plus_offset,allscenes_dict = get_scene_total(offset)
menudepth = total_plus_offset + post_offset

if(pos > menudepth):
    pos = menudepth
elif(pos < 0):
    pos = 0
display = pos

if(display == 0):
        cur_min = int(time.strftime("%M"))
        if(old_min != cur_min or refresh == 1):
            display_time()
            old_min = cur_min
            refresh = 0
        timeout = 0
        #Sleep to conserve CPU Cycles
        time.sleep(0.01)
#Display Selected Menu
if (old_display != display):
    if(display == 1):
        display_2lines(str(display) + ". Turn OFF","all lights slowly",17)
    elif(display == 2):
        display_2lines(str(display) + ". DIM ON","Night lights",17)
    elif(display == 3):
        display_2lines(str(display) + ". FULL ON","all lights",17)
    elif(display == 4):
        display_2lines(str(display) + ". Turn OFF","all lights quickly",17)
    #begin scene selection
    elif(display >= offset && display < total_plus_offset): 
        display_2lines(str(display) + ". " + str(allscenes_dict[display-offset]),"Play?",15)
    elif(display == (menudepth-2)):
        display_2lines(str(display) + ". Settings", "Menu",13)
    elif(display == (menudepth-1)):
        display_2lines(str(display) + ". Light Control", "Menu",13)
    elif(display == (menudepth)):
        display_2lines(str(display) + ". Group Control", "Menu",13)
    old_display = display
    old_min = 60
elif(display != 0):
    time.sleep(0.005)
    old_min = 60
    
 #GPIO button push section# Poll button press and trigger action based on current display
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
        time.sleep(1)
        debugmsg("turning all lights off")
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
        time.sleep(.5)
        debugmsg("turning on night lights dim")
    elif(display == 3):
        display_2lines("Turning all","lights on FULL",12)
        hue_groups(lnum = "0",lon = "true",lbri = "254",lsat = "256",lx = "-1",ly = "-1",ltt = "4",lct = "-1")
        ##turn off front door light... we dont want that...
        #hue_groups(lnum = "5",lon = "false",lbri = "1",lsat = "256",lx = "-1",ly = "-1",ltt = "4",lct = "-1")
        debugmsg("turning all lights on full")
    elif(display == 4):
        display_2lines("Turning all","lights OFF quickly",12)
        hue_groups(lnum = "0",lon = "false",lbri = "256",lsat = "256",lx = "-1",ly = "-1",ltt = "4",lct = "-1")
        debugmsg("turning all lights off quick")
    elif(display >= offset && display < total_plus_offset):
        selected_scenenumber = display-offset+1
        result = holding_button(5000,"Hold to edit S" + str(display-offset),"Will record S" + str(selected_scenenumber),21)
        if result == 0:
            display_2lines("Turning lights:","Scene " + str(selected_scenenumber),12)
            os.popen("./" + str(selected_scenenumber) + "_scene.sh")
            time.sleep(1)
            debugmsg("turning lights scene" + str(selected_scenenumber))
        elif result == 1:
            scenenumber = 1
            ltt = 100
            #result = get_house_scene_by_group(scenenumber,ltt)
            result = get_house_scene_by_light(selected_scenenumber,ltt)
            debugmsg("ran scene by group creation with result = " + result)
        else:
            display_2lines("Something weird","Happened...",12)
            time.sleep(5)
    elif(display == (menudepth-2)):
        pos = 0
        settings_menu()
    elif(display == (menudepth-1)):
        pos = 0
        light_control("l")
    elif(display == (menudepth)):
        pos = 0
        light_control("g")
    time.sleep(0.01)
    #prev_millis = int(round(time.time() * 1000))
    pos = 0