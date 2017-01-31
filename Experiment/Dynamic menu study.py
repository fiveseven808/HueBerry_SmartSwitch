import os 
import json

def light_control(mode):
    if (mode == "g"):
        display_custom("loading groups...")
        name_array,total,lstate_a,keyvalues = get_group_names()
    elif (mode == "l"):
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
                ctmode = 0
                huemode = 0
                prev_mills = int(round(time.time() * 1000))
                while(not GPIO.input(21)):
                    mills = int(round(time.time() * 1000))
                    millsdiff = mills - prev_mills
                    if(millsdiff < 500):
                        display_custom("hold for ct...")
                    elif(millsdiff >= 500):
                        ctmode = 1
                        break
                while(not GPIO.input(21)):
                    display_custom("entering ct...")
                if(ctmode == 0):
                    if(mode == "g"):
                        g_control(keyvalues[display-1])
                        prev_mills = int(round(time.time() * 1000))
                        while(not GPIO.input(21)):
                            mills = int(round(time.time() * 1000))
                            millsdiff = mills - prev_mills
                            if(millsdiff < 500):
                                display_custom("hold for ct...")
                            elif(millsdiff >= 500):
                                ctmode = 1
                                break
                        if (ctmode ==0):
                            display_custom("returning...")
                        else:
                            while(not GPIO.input(21)):
                                display_custom("entering ct...")
                    elif(mode == "l"):
                        l_control(num_lights[display-1])
                        prev_mills = int(round(time.time() * 1000))
                        while(not GPIO.input(21)):
                            mills = int(round(time.time() * 1000))
                            millsdiff = mills - prev_mills
                            if(millsdiff < 500):
                                display_custom("hold for ct...")
                            elif(millsdiff >= 500):
                                ctmode = 1
                                break
                        if (ctmode ==0):
                            display_custom("returning...")
                        else:
                            while(not GPIO.input(21)):
                                display_custom("entering ct...")
                        

                if(ctmode == 1):
                    if(mode == "g"):
                        ct_control(keyvalues[display-1],"g")
                        prev_mills = int(round(time.time() * 1000))
                        while(not GPIO.input(21)):
                            mills = int(round(time.time() * 1000))
                            millsdiff = mills - prev_mills
                            if(millsdiff < 500):
                                display_custom("hold for hue...")
                            elif(millsdiff >= 500):
                                huemode = 1
                                break
                        if (huemode == 1):
                            hue_control(keyvalues[display-1],"g")
                            huemode = 0
                        elif(huemode ==0):
                            display_custom("returning...")
                        prev_mills = int(round(time.time() * 1000))
                        while(not GPIO.input(21)):
                            mills = int(round(time.time() * 1000))
                            millsdiff = mills - prev_mills
                            if(millsdiff < 500):
                                display_custom("hold for sat...")
                            elif(millsdiff >= 500):
                                huemode = 1
                                break
                        if (huemode == 1):
                            sat_control(keyvalues[display-1],"g")
                        elif(huemode ==0):
                            display_custom("returning...")
                           
                    elif(mode == "l"):
                        ct_control(num_lights[display-1],"l") 
                        prev_mills = int(round(time.time() * 1000))
                        while(not GPIO.input(21)):
                            mills = int(round(time.time() * 1000))
                            millsdiff = mills - prev_mills
                            if(millsdiff < 500):
                                display_custom("hold for hue...")
                            elif(millsdiff >= 500):
                                huemode = 1
                                break
                        if (huemode == 1):
                            hue_control(num_lights[display-1],"l")
                            huemode = 0
                        elif(huemode ==0):
                            display_custom("returning...")
                        prev_mills = int(round(time.time() * 1000))
                        while(not GPIO.input(21)):
                            mills = int(round(time.time() * 1000))
                            millsdiff = mills - prev_mills
                            if(millsdiff < 500):
                                display_custom("hold for sat...")
                            elif(millsdiff >= 500):
                                huemode = 1
                                break
                        if (huemode == 1):
                            sat_control(num_lights[display-1],"l")
                        elif(huemode ==0):
                            display_custom("returning...")
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