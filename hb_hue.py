import time
import os
import console_colors
import sys
import math
import colorsys
bcolors = console_colors.bcolors

"""
This class contains all of the hue api calls that I've written for the hueberry project! :D

"""
class HueAPI(object):
    def __init__(self,debug = 0,fakeauth = 0):
        #Set the debug level
        self.debug = debug
        self.fakeauth = fakeauth
        if (self.debug == 0):
            pass

    def load_creds_from_authenticate(self):
        if self.fakeauth == 0:
            import authenticate
            authenticate = authenticate.Authenticate()
            #Loads from ./auth.json in the format from authenticate
            authenticate.load_creds()
            self.api_key = authenticate.api_key
            self.bridge_ip = authenticate.bridge_ip
            self.api_url = 'http://%s/api/%s' % (self.bridge_ip,self.api_key)
            self.debugmsg(self.api_url)
        elif self.fakeauth == 1:
            self.api_key = "null"
            self.bridge_ip = "127.0.0.1"
            self.api_url = 'http://%s/api/%s' % (self.bridge_ip,self.api_key)
            self.debugmsg("FAKE Link Established! "+ self.bridge_ip)
        return self.api_url


    def get_huejson_value(self,g_or_l,num,type):
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
        if(g_or_l == "g"):
            os.popen("curl --silent -H \"Accept: application/json\" -X GET " + self.api_url + "/groups/" + str(num) + " > brite")
        if(g_or_l == "l"):
            os.popen("curl --silent -H \"Accept: application/json\" -X GET  "+ self.api_url + "/lights/" + str(num) + " > brite")
        wholejson = os.popen("cat brite").read() #in case i wana do something properly lol
        wholejson = json.loads(wholejson)
        if(type == "bri"):
            value = os.popen("cat brite | grep -o '\"bri\":[0-9]*' | grep -o ':.*' | tr -d ':'").read()
        if(type == "ct"):
            value = os.popen("cat brite | grep -o '\"ct\":[0-9]*' | grep -o ':.*' | tr -d ':'").read()
        if(type == "hue"):
            value = os.popen("cat brite | grep -o '\"hue\":[0-9]*' | grep -o ':.*' | tr -d ':'").read()
        if(type == "sat"):
            value = os.popen("cat brite | grep -o '\"sat\":[0-9]*' | grep -o ':.*' | tr -d ':'").read()
        if(type == "type"):
            value = wholejson['type']
        os.popen("rm brite")
        if not value:
            if(g_or_l == "l"):
                #hb_display.display_2lines("No devices","in lights",17)
                pass
            if(g_or_l == "g"):
                #hb_display.display_2lines("No devices","in groups",17)
                pass
            #time.sleep(3)
            value = -1
        return value,wholejson

    def get_group_names(self):
        result_array = []
        lstate_a = []
        #hb_display.display_2lines("starting","group names",17)
        self.debugmsg("starting curl")
        os.popen("curl --silent -H \"Accept: application/json\" -X GET " + self.api_url + "/groups   > groups")
        self.debugmsg("finished curl")
        #hb_display.display_2lines("finished","curl",17)
        cmdout = os.popen("cat groups").read()
        self.debugmsg(cmdout)
        if not cmdout:
            #print "not brite"
            retry = 1
            while not cmdout:
                if retry >= 3:
                    #hb_display.display_2lines("An error in ","get_group_name",15)
                    self.debugmsg("error in get_group_names probably lost connection to hub")
                    time.sleep(2)
                    return 0,0,0,0
                    break
                #hb_display.display_2lines("Bridge not responding","Retrying " + str(retry),15)
                os.popen("curl --silent -H \"Accept: application/json\" -X GET " + self.api_url + "/groups  > groups")
                cmdout = os.popen("cat groups").read()
                retry = retry + 1
        #self.debugmsg("passed ifstatement")
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

    def get_light_names(self):
        os.popen("curl --silent -H \"Accept: application/json\" -X GET " + self.api_url + "/lights  > lights")
        light_names = os.popen("cat lights | grep -P -o '\"name\":\".*?\"' | grep -o ':\".*\"' | tr -d '\"' | tr -d ':'").read()
        if not light_names:
            #print "not brite"
            retry = 1
            while not light_names:
                if retry == 3:
                    #hb_display.display_2lines("An error in ","get_light_names",15)
                    self.debugmsg("error in get_light_names probably lost connection to hub")
                    time.sleep(2)
                    return 0,0,0,0
                    break
                #hb_display.display_2lines("Bridge not responding","Retrying " + str(retry),15)
                os.popen("curl --silent -H \"Accept: application/json\" -X GET " + self.api_url + "/lights  > lights")
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

    def hue_lights(self,lnum,lon,lbri,lsat,lx,ly,lct,ltt,**options):
        self.debugmsg("entering hue lights")
        if ('hue' in options):
            result = os.popen("curl --silent -H \"Accept: application/json\" -X PUT --data '{\"on\":" + str(lon) + ",\"bri\":" + str(lbri) + ",\"sat\":" + str(lsat) + ",\"xy\":[" + str(lx) + "," + str(ly) + "],\"transitiontime\":" + str(ltt) + ",\"hue\":" + str(options['hue']) + "}' " + self.api_url + "/lights/" + str(lnum) + "/state" ).read()
        else:
            result = os.popen("curl --silent -H \"Accept: application/json\" -X PUT --data '{\"on\":" + str(lon) + ",\"bri\":" + str(lbri) + ",\"sat\":" + str(lsat) + ",\"xy\":[" + str(lx) + "," + str(ly) + "],\"transitiontime\":" + str(ltt) + ",\"ct\":" + str(lct) + "}' " + self.api_url + "/lights/" + str(lnum) + "/state" ).read()
        self.debugmsg(result)
        if not result:
            #print "not brite"
            #hb_display.display_2lines("An error in ","hue_lights",17)
            time.sleep(2)
            return
        print(result)
        return result

    def hue_groups(self,lnum,lon = "true",lbri = -1,lsat = -1,lx = -1,ly = -1,lct = -1,ltt = -1,**options):
        self.debugmsg("entering hue groups")
        if ('hue' in options):
            #self.debugmsg("hue and before result")
            result = os.popen("curl --silent -H \"Accept: application/json\" -X PUT --data '{\"on\":" + str(lon) + ",\"bri\":" + str(lbri) + ",\"sat\":" + str(lsat) + ",\"xy\":[" + str(lx) + "," + str(ly) + "],\"transitiontime\":" + str(ltt) + ",\"hue\":" + str(options['hue']) + "}' " + self.api_url + "/groups/" + str(lnum) + "/action" ).read()
            #self.debugmsg("hue and after result")
        else:
            #self.debugmsg("everything else and before result")
            result = os.popen("curl -s -m 1 -H \"Accept: application/json\" -X PUT --data '{\"on\":" + str(lon) + ",\"bri\":" + str(lbri) + ",\"sat\":" + str(lsat) + ",\"xy\":[" + str(lx) + "," + str(ly) + "],\"transitiontime\":" + str(ltt) + ",\"ct\":" + str(lct) + "}' " + self.api_url + "/groups/" + str(lnum) + "/action").read()
            #self.debugmsg("everything else and after result")
        self.debugmsg(result)
        if not result:
            #print "not brite"
            #hb_display.display_2lines("An error in ","hue_groups",17)
            time.sleep(2)
            return
        #print(result)
        #self.debugmsg("printed result")
        return result

    #------------------------------------------------------------------------------------
    #Method to convert color temperature into hue and saturation scaled for the Hue-system
    #Not tested so much yet
    #------------------------------------------------------------------------------------
    def ct_to_hue_sat(self,ct):
        #Method from http://www.tannerhelland.com/4435/convert-temperature-rgb-algorithm-code/
        self.debugmsg("converting ct " + str(ct) + "into Hue and Saturation")
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
        #self.debugmsg("raw hue: " + str(360*h) + "saturation: " + str(s*100) + "value: " + str(v))
        h = int(h * 65535)
        s = int(s * 254)
        #h = h + 910
        self.debugmsg("hue: " + str(h) + "saturation: " + str(s) + "value: " + str(v))
        return h, s

    def debugmsg(self,message):
        #global logfile
        debug_state = self.debug
        if debug_state == 1:
            current_time = time.strftime("%m / %d / %Y %-H:%M")
            #with open(logfile, "a") as myfile:
            #    myfile.write(current_time + " " + message + "\n")
            print(current_time + " " + message + "\n")
        else:
            return

if __name__ == "__main__":
    import hb_hue
    import time
    print("Running hb_hue module self test...")
    hbapi = hb_hue.HueAPI(debug = 1,fakeauth = 1)
    print("Object initialized")
    hbapi.load_creds_from_authenticate()
    print("loaded creds")
    hbapi.get_group_names()
    print("got group names")
    hbapi.get_light_names()
    print("got light names")
    hbapi.hue_groups(lnum = 0, lon = "false")
    time.sleep(0.4)
    hbapi.hue_groups(lnum = 0, lon = "true")
    hbapi.ct_to_hue_sat(2600)
