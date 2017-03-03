import hb_encoder
import hb_display
import time

class Simple_Menu(object):
    def __init__(self, menu_titles, menu_functions, debug = 0, mirror_mode = 0):
        while True:
            total_screens = len(self.menu_titles)
            total_plus_offset = total_screens + self.offset
            menudepth = total_plus_offset + self.post_offset - 1
            # Cycle through different displays
            if(self.encoder.pos > menudepth):
                self.encoder.pos = menudepth
            elif(self.encoder.pos < 0):
                self.encoder.pos = 0
            display = self.encoder.pos # because pos is a pre/bounded variable, and encoder.pos has been forced down.
            #Display Selected Menu
            if (old_display != display or refresh == 1):
                if(display >= self.offset and display <= (total_plus_offset-1)):
                    self.hb_display.display_2lines(str(display) + ". " + str(self.menu_titles[display-self.offset]),"Run?",15)
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
                    print display
                    self.menu_functions[display]()
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
    tm_titles = ("1st menu",
                "2nd menu",
                "3rd menu",
                "quit")
    tm_functions = (lambda: printmenu("oshit1"),
                    lambda: printmenu("oshit2"),
                    lambda: printmenu("oshit3"),
                    lambda: sys.exit())
    testmenu = hb_menu.Simple_Menu(debug = 1,menu_titles = tm_titles, menu_functions = tm_functions)
    testmenu.run_menu()
