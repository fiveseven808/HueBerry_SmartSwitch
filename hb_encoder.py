import curses

import RPi.GPIO as GPIO
import pigpio
import rotary_encoder


"""
All this class does is instantiate an instance of rotary_encoder 
so that all other hueBerry functions can reference this instance 
and check the pos variable. This avoids globals becuase the pos 
variable is specific to the object, and cannot be changed via 
other means. 
"""
class rotary(object):
    def __init__(self,self.debug = 0):
        self.pos = 0 
        if (self.debug == 0):
            self.pi = pigpio.pi()
            self.decoder = rotary_encoder.decoder(self.pi, 16, 20, self.callback)
    
    def callback(way):
        #global pos
        self.pos += way
        if (self.debug == 1):
            print("pos={}".format(pos))
        

class control(object):
    def __init__(self):
        # get the curses screen window
        self.screen = curses.initscr()
        # turn off input echoing
        curses.noecho()
        # respond to keys immediately (don't wait for enter)
        curses.cbreak()
        # map arrow keys to special values
        self.screen.keypad(True)
    def get_key(self):
        char = self.screen.getch()
        if char == ord('q'):
            #break
            return "q"
        elif char == curses.KEY_RIGHT:
            # print doesn't work with curses, use addstr instead
            #screen.addstr(0, 0, 'right')
            return "right"
        elif char == curses.KEY_LEFT:
            #screen.addstr(0, 0, 'left ')  
            return "left"
        elif char == curses.KEY_UP:
            #screen.addstr(0, 0, 'up   ') 
            return "up"
        elif char == curses.KEY_DOWN:
            #screen.addstr(0, 0, 'down ')
            return "down"
            
            
if __name__ == "__main__":
    import time
    import hb_encoder
    test = hb_encoder.rotary(debug = 1)
    test.callback(1)
    time.sleep(1)
    test.callback(1)
    time.sleep(1)
    test.callback(1)
    time.sleep(1)
    test.callback(-1)