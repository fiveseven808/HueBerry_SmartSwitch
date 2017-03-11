"""
This module is a nice little condensed API for hueBerry modules
"""
import hb_display
import hb_encoder

class HB_PAPI(object):
    def __init__(self,debug = 0, mirror_mode = 0, rotate = 0):
        self.debug_argument = debug
        self.hb_display = hb_display.display(console = self.debug_argument,mirror = mirror_mode, rotation = rotate)
        self.encoder = hb_encoder.RotaryClass(debug = self.debug_argument)

    def get_state(self):
        self.pos,self.pushed = self.encoder.get_state()
        return self.pos,self.pushed

if __name__ == "__main__":
    import hbplugin
    hbapi = hbplugin.HB_PAPI(debug = 1)

    #Call a function within hb_display for lower level api
    hbapi.hb_display.display_time(time_format = 1)

    #Check for an input using the hueBerry API
    pos, pushed = hbapi.get_state()
    print("pos is: "+str(pos)+" and pushed is: "+str(pushed))
