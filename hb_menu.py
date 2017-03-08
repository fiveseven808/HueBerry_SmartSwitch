import hb_encoder
import hb_display
import time

class Menu_Creator(object):
    def __init__(self, menu_layout, debug = 0, mirror_mode = 0, rotate = 0):
        debug_argument = debug
        self.offset = 0 #carryover
        self.post_offset = 0 #carryover
        self.menu_layout = menu_layout
        self.exitvar = 0
        # Create Display Object
        # Maybe instead of create? get passed display object from hueberry? would make this less independent though... and confusing...
        if(mirror_mode == 1):
            self.hb_display = hb_display.display(console = 1,mirror = mirror_mode)
        else:
            self.hb_display = hb_display.display(console = debug_argument,mirror = mirror_mode, rotation = rotate)
        # Create Encoder Object
        if (debug_argument == 0):
            self.encoder = hb_encoder.RotaryClass()
        elif (debug_argument == 1):
            self.encoder = hb_encoder.RotaryClass(debug = 1)

    def run_simple_menu(self):
        """
        menu_layout = ("1st menu",lambda: printmenu("oshit! it works!"),
                    "2nd menu",lambda: printmenu("doing a second thing"),
                    "quit",lambda: sys.exit())
        """
        timeout = 0
        displaytemp = 0
        prev_secs = 0
        old_display = 0
        refresh = 1
        pushed = 0
        menu_timeout = 30
        depth_divisor = 2 # how many menu items per line. i.e. 1 title + 1 function = 2
        self.encoder.wait_for_button_release()
        while True:
            total_screens = len(self.menu_layout)
            total_plus_offset = total_screens + self.offset
            menudepth = (total_plus_offset + self.post_offset - depth_divisor)/depth_divisor
            # Cycle through different displays
            if(self.encoder.pos > menudepth):
                self.encoder.pos = menudepth
            elif(self.encoder.pos < 0):
                self.encoder.pos = 0
            display = self.encoder.pos*2 # because pos is a pre/bounded variable, and encoder.pos has been forced down.
            display_number = (display/2)+1
            #Display Selected Menu
            if (old_display != display or refresh == 1):
                if(display >= self.offset and display <= (total_plus_offset-1)):
                    self.hb_display.display_2lines(str(display_number) + ". " + str(self.menu_layout[display-self.offset]),"Run?",15)
                refresh = 0
                old_display = display
            time.sleep(0.005)
            secs = int(round(time.time()))
            timeout_secs = secs - prev_secs
            if(display != 0 and displaytemp != display):
                prev_secs = secs
                displaytemp = display
            elif(display != 0 and timeout_secs >= menu_timeout):
                self.encoder.pos = 0
                display_temp = 0
            elif(display == 0):
                displaytemp = display
            pos,pushed = self.encoder.get_state() # after loading everything, get state#
            if (pushed):
                if(display >= self.offset and display < total_plus_offset):
                    #print display
                    if self.menu_layout[display+(depth_divisor-1)] == "exit":
                        #print "exiting"
                        #time.sleep(2)
                        break
                    self.menu_layout[display+(depth_divisor-1)]()
                time.sleep(0.01)
                #prev_millis = int(round(time.time() * 1000))
                self.encoder.pos = 0
                refresh = 1
            #time.sleep(0.1)

    def run_2_line_menu(self):
        """
        menu_layout = ("Name 1", "Name 2", lambda: do_thing_1(),
                        "Name 3", "Name 4", lambda: do_thing_2(),
                        "Back to", "Main Menu", "exit")
        """
        timeout = 0
        displaytemp = 0
        prev_secs = 0
        old_display = 0
        refresh = 1
        pushed = 0
        menu_timeout = 30
        depth_divisor = 3 # how many menu items per line. i.e. 1 title + 1 function = 2
        self.encoder.wait_for_button_release()
        while True:
            total_screens = len(self.menu_layout)
            total_plus_offset = total_screens + self.offset
            menudepth = (total_plus_offset + self.post_offset - depth_divisor)/depth_divisor
            # Cycle through different displays
            if(self.encoder.pos > menudepth):
                self.encoder.pos = menudepth
            elif(self.encoder.pos < 0):
                self.encoder.pos = 0
            display = self.encoder.pos*3 # because pos is a pre/bounded variable, and encoder.pos has been forced down.
            display_number = (display/3)+1
            #Display Selected Menu
            if (old_display != display or refresh == 1):
                if(display >= self.offset and display <= (total_plus_offset-1)):
                    if callable(self.menu_layout[display-self.offset]) == False:
                        self.hb_display.display_2lines(str(display_number) + ". "+str(self.menu_layout[display-self.offset]),str(self.menu_layout[display-self.offset+1]),17)
                    else:
                        self.menu_layout[display-self.offset]()
                refresh = 0
                old_display = display
            #elif(display != 0):
            #    time.sleep(0.005)
            time.sleep(0.005)

            secs = int(round(time.time()))
            timeout_secs = secs - prev_secs
            if(display != 0 and displaytemp != display):
                prev_secs = secs
                displaytemp = display
            elif(display != 0 and timeout_secs >= menu_timeout):
                self.encoder.pos = 0
                display_temp = 0
            elif(display == 0):
                displaytemp = display
            #if(display != 0):
            #    print timeout_secs

            # Poll button press and trigger action based on current display
            #if(not GPIO.input(21)):
            #print self.exitvar
            pos,pushed = self.encoder.get_state() # after loading everything, get state#
            if (pushed):
                if(display >= self.offset and display < total_plus_offset):
                    """
                    #print display, self.offset
                    selected_scenenumber = display-self.offset+1
                    #print selected_scenenumber
                    result = holding_button(1000,"Hold to edit: " + scene_files[display-self.offset],"Will edit: " + scene_files[display-self.offset],21)
                    selected_file = str(g_scenesdir) + str(scene_files[display-self.offset])
                    if result == 0:
                        self.hb_display.display_2lines("Turning lights:",str(scene_files[display-self.offset]),12)
                        #print scene_files[display-self.offset]
                        print "running the below thing"
                        #selected_file = str(g_scenesdir) + str(scene_files[display-self.offset])
                        os.popen("\"" + str(selected_file) + "\"")
                        print(str(selected_file))
                        time.sleep(1)
                        debugmsg("Running: " + str(scene_files[display-self.offset]))
                    elif result == 1:
                        ltt = set_scene_transition_time()
                        result = get_house_scene_by_light(selected_file,ltt)
                        debugmsg("Ran scene editing by group with result = " + result)
                    else:
                        self.hb_display.display_2lines("Something weird","Happened...",12)
                        time.sleep(5)
                    """
                    #print display
                    if self.menu_layout[display+(depth_divisor-1)] == "exit":
                        # If a menu item has "exit" as the function/action thing, then exit
                        return 0
                    # Position [1] or [2] can be interpeted as type (all caps)
                    if self.menu_layout[1] == "BD_TYPE" or self.menu_layout[2] == "BD_TYPE":
                        # If BD_TYPE menu
                        if display != 0 :
                            return self.menu_layout[display+(depth_divisor-1)]()
                        if display == 0:
                            # Make sure to do nothing when the "Question" for BD_TYPE is selected
                            pass
                    else: # If normal type menu
                        # This is where the object that's selected actually runs...
                        self.menu_layout[display+(depth_divisor-1)]()
                time.sleep(0.01)
                refresh = 1
                #prev_millis = int(round(time.time() * 1000))
                self.encoder.pos = display/depth_divisor #resume where you came from
            #time.sleep(0.1)
        return

    def single_value_menu(self):
        """
        datastructure = (group_or_light_or_something, bri_or_hue_or_something,
                        max_rot_value, lambda: func_2_run_off_of_pos(),
                        timeout, lambda: timeout_func(),
                        lambda: pos_to_value_func())
        """
        """
        brite,wholejson = get_huejson_value("g",group,"bri")
        if(brite == -1):
            #print "No lights avaliable"
            return
        #else:
        #    print "guess it was brite"
        brite = int(brite)      #make integer
        if brite < 10 and brite >= 0:
            brite = 10
        if (wholejson['state']['any_on'] == False):
            brite = 0
        """
        title1 = self.menu_layout[1]
        title2 = self.menu_layout[2]
        max_rot_val = self.menu_layout[3]
        main_func = self.menu_layout[4]
        timeout_ms = self.menu_layout[5]
        tiemout_func = self.menu_layout[6]
        pos_value_func = self.menu_layout[7]
        #The above is deermined by the calling function and passed to the below in the big dict
        brite = brite/10.16        #trim it down to 25 values
        #Make this "starting" value something that pulls from a return from a function? perhaps? or mayube it's predetermined and sent lol
        brite = int(brite)      #convert the float down to int agian
        #Need to detmermine initial encoder position
        encoder.pos = brite
        max_rot_val = 25
        #bri_pre = encoder.pos * 10
        bri_pre = encoder.pos * 10.16
        refresh = 1
        prev_mills = 0
        self.encoder.wait_for_button_release()
        while True:
            pos,pushed = encoder.get_state()
            if(pos > max_rot_val):
                encoder.pos = max_rot_val
            elif(pos < 0):
                encoder.pos = 0
            mills = int(round(time.time() * 1000))
            millsdiff = mills - prev_mills
            #rot_bri = encoder.pos * 10
            rot_bri = encoder.pos * 10.16
            if(bri_pre != rot_bri or refresh ==  1 ):
                hb_display.display_2lines("Group " + str(group),"Bri: " + str(int(rot_bri/2.54)) + "%",17)
                refresh = 0
            if rot_bri <= 0 and rot_bri != bri_pre:
                #print"turning off?"
                #hue_groups(lnum = group,lon = "false",lbri = rot_bri,lsat = "-1",lx = "-1",ly = "-1",ltt = "5", lct = "-1")
                huecmd = threading.Thread(target = hue_groups, kwargs={'lnum':group,'lon':"false",'lbri':int(rot_bri),'lsat':"-1",'lx':"-1",'ly':"-1",'ltt':"5",'lct':"-1"})
                huecmd.start()
                bri_pre = rot_bri
            elif(rot_bri != bri_pre and millsdiff > 200):
                #print"millsdiff > 200"
                #hue_groups(lnum = group,lon = "true",lbri = rot_bri,lsat = "-1",lx = "-1",ly = "-1",ltt = "5", lct = "-1")
                huecmd = threading.Thread(target = hue_groups, kwargs={'lnum':group,'lon':"true",'lbri':int(rot_bri),'lsat':"-1",'lx':"-1",'ly':"-1",'ltt':"5",'lct':"-1"})
                huecmd.start()
                bri_pre = rot_bri
                prev_mills = mills
            millsdiff = mills - prev_mills
            if(millsdiff > 5000):
                #If 5.0 seconds have passed and nothing has happened, go and refresh the display and reset the miliseconds
                rot_bri,wholejson = get_huejson_value("g",group,"bri")
                #print "the rot bri is: "+str(rot_bri)
                hb_display.display_2lines("Group " + str(group),"Bri: " + str(int(int(rot_bri)/2.54)) + "%",17)
                prev_mills = mills
            if(pushed):
                exitvar = True
            time.sleep(0.01)
            refresh = 1


def printmenu(text):
    print(text)
    time.sleep(1)

# For testing
if __name__ == "__main__":
    import hb_menu
    import sys
    tm_menu = ("1st menu",lambda: printmenu("oshit! it works!"),
                "2nd menu",lambda: printmenu("doing a second thing"),
                "3rd menu",lambda: printmenu("doing a third thing"),
                "quit",lambda: sys.exit())
    testmenu = hb_menu.Menu_Creator(debug = 1,menu_layout = tm_menu)
    testmenu.run_simple_menu()
