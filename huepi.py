#!/usr/bin/env python


def get_group_names():
    os.popen("curl -H \"Accept: application/json\" -X GET  http://192.168.1.144/api/0DEuqTaGHB5J2V72IzV1K-r3mwpf9ddjDkDDIRdzr/groups  > lights")
    group_names = os.popen("cat lights | grep -P -o '\"name\":\".*?\"' | grep -o ':\".*\"' | tr -d '\"' | tr -d ':'").read()
    os.popen("rm lights")
    result_array = group_names.split('\n')
    num_groups = len(result_array) - 1
    return result_array,num_groups

def get_light_names():
    os.popen("curl -H \"Accept: application/json\" -X GET  http://192.168.1.144/api/0DEuqTaGHB5J2V72IzV1K-r3mwpf9ddjDkDDIRdzr/lights  > lights")
    light_names = os.popen("cat lights | grep -P -o '\"name\":\".*?\"' | grep -o ':\".*\"' | tr -d '\"' | tr -d ':'").read()
    num_lights = os.popen("cat lights | grep -P -o '\"[0-9]*?\"' | tr -d '\"'").read()
    os.popen("rm lights")
    name_array = light_names.split('\n')
    num_array = num_lights.split('\n')
    total = len(num_array) - 1
    return name_array,num_array,total

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
    
def g_light_control():
    display_custom("loading groups...")
    name_array,total = get_group_names()
    global pos
    exitvar = False 
    menudepth = total + 1
    while exitvar == False: 
        if(pos > menudepth):
            pos = menudepth
        elif(pos < 1):
            pos = 1
        display = pos

        #Display Selected Menu
        if(display <= total):
            display_2lines(str(display) + " " + str(name_array[display-1]),"Control",11)
        else:
            display_2lines("Back","One Level",17)
            
        # Poll button press and trigger action based on current display
        if(not GPIO.input(16)):
            if(display <= total):
                g_control(display)
                time.sleep(0.01)
            else:
                time.sleep(0.25)
                exitvar = True
            time.sleep(0.01)
            #prev_millis = int(round(time.time() * 1000))
    return
    
def l_light_control():
    display_custom("loading lights...")
    name_array,num_lights,total = get_light_names()
    global pos
    exitvar = False 
    menudepth = total + 1
    while exitvar == False: 
        if(pos > menudepth):
            pos = menudepth
        elif(pos < 1):
            pos = 1
        display = pos

        #Display Selected Menu
        if(display <= total):
            display_2lines(str(display) + " " + str(name_array[display-1]),"Control",11)
        else:
            display_2lines("Back","One Level",17)
            
        # Poll button press and trigger action based on current display
        if(not GPIO.input(16)):
            if(display <= total):
                print(num_lights[display-1])
                l_control(num_lights[display-1])
                time.sleep(0.01)
            else:
                time.sleep(0.25)
                exitvar = True
            time.sleep(0.01)
            #prev_millis = int(round(time.time() * 1000))
    return

def g_control(group):  
    display_custom("loading brightness...")
    os.popen("curl -H \"Accept: application/json\" -X GET  http://192.168.1.144/api/0DEuqTaGHB5J2V72IzV1K-r3mwpf9ddjDkDDIRdzr/groups/" + str(group) + " > brite")
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
    while exitvar == False: 
        if(pos > max_rot_val):
            pos = max_rot_val
        elif(pos < 0):
            pos = 0

        rot_bri = pos * 10 
        display_2lines("Group " + str(group),"Bri: " + str(int(rot_bri/2.5)) + "%",17)
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
    display_custom("loading brightness...")
    os.popen("curl -H \"Accept: application/json\" -X GET  http://192.168.1.144/api/0DEuqTaGHB5J2V72IzV1K-r3mwpf9ddjDkDDIRdzr/lights/" + str(light) + " > brite")
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
    while exitvar == False: 
        if(pos > max_rot_val):
            pos = max_rot_val
        elif(pos < 0):
            pos = 0

        rot_bri = pos * 10 
        display_2lines("Light " + str(light),"Bri: " + str(int(rot_bri/2.5)) + "%",17)
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