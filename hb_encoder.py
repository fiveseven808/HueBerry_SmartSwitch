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
    def __init__(self,debug = 0,enc_plus = 16, enc_minus = 20,enc_button = 21):
        #Set the encoder + and - pins and push switch pin
        self.enc_plus = enc_plus
        self.enc_minus = enc_minus
        self.enc_button = enc_button
        #Set the debug level
        self.debug = debug
        self.pos = 0 
        self.pushed = 0
        if (self.debug == 0):
            #Setup the rotary encoder module (lol idk what it does)
            self.pi = pigpio.pi()
            self.decoder = rotary_encoder.decoder(self.pi, self.enc_plus, self.enc_minus, self.callback)
            #Set the GPIO parameters for the push switch pin
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.enc_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    def callback(self,way):
        self.pos += way
        if (self.debug == 1):
            print("pos={}".format(self.pos))
    
    def check_button(self,console_control = 0):
        self.console_control = console_control
        if (self.debug == 1 or self.console_control = 1):
            gpio_input()
        if (self.debug == 0 or self.console_control = 0):
            self.gpio_input()
        return self.pushed
        
    def console_input(self,button_only = 0):
        #Code to get the BUFFERED enter key or something from the console
        if (button_only == 1):
            return
        return
        
    
    def gpio_input(self):
        if (not GPIO.input(self.enc_button)):
            #The button is pushed
            self.pushed = 1
        elif (GPIO.input(self.enc_button)):
            self.pushed = 0 
        return self.pushed

class monitor_keyboard(object):
    def __init__(self):
        #Do things related to setting up monitoring keyboard input
        while True:
            #Check keyboard input and update a callback function accordingly 
            #i.e. if ">" then rotary.callback(1)
            # if "<" then rotary.callback(-1)
            # if "/" then rotary.pushed = 1
            # or soemthing like that
            pass
        
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
        elif char == curses.KEY_ENTER:
            #screen.addstr(0, 0, 'enter ')
            return "enter"
            
            
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
    print "testing button... please push the encoder or enter"
    while (test.check_button == 0):
        time.sleep(0.01)
    print "button pushed! yay!"