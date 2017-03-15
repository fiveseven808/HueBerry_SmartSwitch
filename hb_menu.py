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
                        return_status = self.menu_layout[display+(depth_divisor-1)]()
                    if return_status == "BREAK_MENU":
                        return
                time.sleep(0.01)
                refresh = 1
                #prev_millis = int(round(time.time() * 1000))
                self.encoder.pos = display/depth_divisor #resume where you came from
            #time.sleep(0.1)
        return

    def single_value_menu(self, main_title,value_title,
                                calc_func, rev_calc,
                                action_func,
                                start_pos,a_param,
                                min_val, max_val,
                                timeout, timeout_func):
        #Need to detmermine initial encoder position
        self.encoder.pos = int(start_pos)
        max_rot_val = max_val
        bri_pre = calc_func(self.encoder.pos)
        refresh = 1
        prev_mills = 0
        self.encoder.wait_for_button_release()
        pos = self.encoder.pos
        while True:
            if(self.encoder.pos > max_rot_val):
                self.encoder.pos = max_rot_val
            elif(self.encoder.pos < min_val):
                self.encoder.pos = min_val
            mills = int(round(time.time() * 1000))
            millsdiff = mills - prev_mills
            rot_bri = calc_func(self.encoder.pos)
            if(bri_pre != rot_bri or refresh ==  1 ):
                self.hb_display.display_2lines(main_title,value_title + str(int(rot_bri)) + "%",17)
                refresh = 0
            if rot_bri <= min_val and rot_bri != bri_pre:
                print"turning off since below min value"
                #hue_groups(lnum = group,lon = "false",lbri = rot_bri,lsat = "-1",lx = "-1",ly = "-1",ltt = "5", lct = "-1")
                #huecmd = threading.Thread(target = hue_groups, kwargs={'lnum':group,'lon':"false",'lbri':int(rot_bri),'lsat':"-1",'lx':"-1",'ly':"-1",'ltt':"5",'lct':"-1"})
                #huecmd.start()
                bri_pre = rot_bri
            elif(rot_bri != bri_pre and millsdiff > 200):
                print"millsdiff > 200"
                print"running actionfunc with rot_bri calcuated result"
                action_func(pos)
                #hue_groups(lnum = group,lon = "true",lbri = rot_bri,lsat = "-1",lx = "-1",ly = "-1",ltt = "5", lct = "-1")
                #huecmd = threading.Thread(target = hue_groups, kwargs={'lnum':group,'lon':"true",'lbri':int(rot_bri),'lsat':"-1",'lx':"-1",'ly':"-1",'ltt':"5",'lct':"-1"})
                #huecmd.start()
                bri_pre = rot_bri
                prev_mills = mills
            millsdiff = mills - prev_mills
            if(millsdiff > timeout):
                #If 5.0 seconds have passed and nothing has happened, go and refresh the display and reset the miliseconds
                #rot_bri,wholejson = get_huejson_value("g",group,"bri")
                self.hb_display.display_2lines(main_title,value_title + str(int(rot_bri)) + "%",17)
                timeout_func(pos)
                print "the rot bri after 5 sec is: "+str(rot_bri)
                prev_mills = mills
            pos,pushed = self.encoder.get_state()
            if(pushed):
                return #exit function goes here
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
