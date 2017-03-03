import hb_encoder
import hb_display
import time

class Menu_Creator(object):
    def __init__(self, menu_layout, debug = 0, mirror_mode = 0):
        debug_argument = debug
        self.offset = 0 #carryover
        self.post_offset = 0 #carryover
        self.menu_layout = menu_layout
        self.exitvar = 0
        # Create Display Object
        if(mirror_mode == 1):
            self.hb_display = hb_display.display(console = 1,mirror = mirror_mode)
        else:
            self.hb_display = hb_display.display(console = debug_argument,mirror = mirror_mode)
        # Create Encoder Object
        if (debug_argument == 0):
            self.encoder = hb_encoder.RotaryClass()
        elif (debug_argument == 1):
            self.encoder = hb_encoder.RotaryClass(debug = 1)

    def run_simple_menu(self):
        timeout = 0
        displaytemp = 0
        prev_secs = 0
        old_display = 0
        refresh = 1
        pushed = 0
        menu_timeout = 30
        while True:
            total_screens = len(self.menu_layout)
            total_plus_offset = total_screens + self.offset
            menudepth = total_plus_offset + self.post_offset - 1
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
                old_display = display
            elif(display != 0):
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
                    self.menu_layout[display+1]()
                elif(display == (menudepth)):
                    self.encoder.pos = 0
                    light_control("g") #temp for test lol
                    #scene_explorer(g_scenesdir)
                time.sleep(0.01)
                #prev_millis = int(round(time.time() * 1000))
                self.encoder.pos = 0
            #time.sleep(0.1)

    def run_2_line_menu(self):
        timeout = 0
        displaytemp = 0
        prev_secs = 0
        old_display = 0
        refresh = 1
        pushed = 0
        menu_timeout = 30
        while self.exitvar == 0:
            total_screens = len(self.menu_layout)
            total_plus_offset = total_screens + self.offset
            menudepth = total_plus_offset + self.post_offset - 1
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
                    self.hb_display.display_2lines(str(display_number) + ". "+str(self.menu_layout[display-self.offset]),str(self.menu_layout[display-self.offset+1]),17)
                old_display = display
            elif(display != 0):
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
            print self.exitvar
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
                    self.menu_layout[display+2]()
                elif(display == (menudepth)):
                    self.encoder.pos = 0
                    light_control("g") #temp for test lol
                    #scene_explorer(g_scenesdir)
                time.sleep(0.01)
                #prev_millis = int(round(time.time() * 1000))
                self.encoder.pos = 0
            #time.sleep(0.1)

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
