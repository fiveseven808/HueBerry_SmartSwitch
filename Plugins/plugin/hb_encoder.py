#import curses
import time
import os
import console_colors
import sys
bcolors = console_colors.bcolors

#Check if Raspbian
temp = os.popen("cat /etc/os-release | grep raspbian").read()
result_array = temp.split('\n')
num_groups = len(result_array) - 1
if(num_groups != 4):
    print(bcolors.RED+"This OS is not Raspbian. RPi specific modules will not be loaded."+bcolors.ENDC)
    time.sleep(1)
    #sys.exit()
else:
    print(bcolors.GRN+"Looks like you're running Rasbian! Loading RPi specific modules!"+bcolors.ENDC)
    import RPi.GPIO as GPIO
    import pigpio
    import rotary_encoder

"""
All this class does is instantiate an instance of rotary_encoder
so that all other hueBerry functions can reference this instance
and check the pos variable. This avoids globals becuase the pos
variable is specific to the object, and cannot be changed via
other means.


Maybe I want it so that I have something like
rotary = hb_encoder.RotaryClass(debug = 1)
And then in every function I'll have it check to see if a state has changed by doing
pos,pushed = rotary.get_state()

So I guess when get_state() is called, it'll go and check if the debug variable was set
If the debug variable was set then it'll go and pull a value from the console
If the debug variable wasn't set then it'll just pull the pos value from the object scope variable
    It'll go and then immediately check if the button is being pushed
"""
class RotaryClass(object):
    def __init__(self,debug = 0,enc_plus = 16, enc_minus = 20,enc_button = 21,no_encoder = 0):
        #Set the encoder + and - pins and push switch pin
        self.enc_plus = enc_plus
        self.enc_minus = enc_minus
        self.enc_button = enc_button
        #Set the debug level
        self.debug = debug
        self.pos = 0
        self.pushed = 0
        self.no_encoder = no_encoder
        if (self.debug == 0):
            #Setup the rotary encoder module (lol idk what it does)
            self.pi = pigpio.pi()
            self.decoder = rotary_encoder.decoder(self.pi, self.enc_plus, self.enc_minus, self.callback)
            #Set the GPIO parameters for the push switch pin
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.enc_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def callback(self,way):
        #This function updates object scoped variables
        self.pos += way
        if (self.debug == 1):
            print("pos={}".format(self.pos))

    def get_state(self):
        #This function updates object scoped variables
        self.pushed = 0
        if self.no_encoder == 0:
            if (self.debug == 1):
                self.query_console()
            if (self.debug == 0):
                self.pushed = self.gpio_input()
        elif self.no_encoder == 1:
            self.query_3_buttons()
        return self.pos,self.pushed

    def gpio_input(self):
        if (not GPIO.input(self.enc_button)):
            #The button is pushed
            pushed = 1
        else:
            pushed = 0
        return pushed

    def query_console(self):
        #do a thing querying the console. it's fine if it stops everything
        #right now i just want something that works
        command = raw_input("Enter a command | Exit with: [q]\nScroll Left[,] Scroll Right[.] Button Press[/]\nThen send with [Enter]: ")
        #print command
        #if left:
        if(command == ','):
            self.callback(-1)
        #if right:
        if(command == '.'):
            self.callback(1)
        #if enter:
        if(command == '/'):
            self.pushed = 1
        #if q:
        if(command == 'q'):
            sys.exit()

    def query_3_buttons(self):
        if (not GPIO.input(self.undefinedvalue_down)):
            self.callback(-1)
        #if right:
        if (not GPIO.input(self.undefinedvalue_up)):
            self.callback(1)
        #if enter:
        if (not GPIO.input(self.undefinedvalue_pushed)):
            self.pushed = 1

    def wait_for_button_release(self):
        if (self.debug == 0):
            self.get_state()
            while(self.pushed):
                #just wait lol
                self.get_state()
                time.sleep(0.01)
        return


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
    test = hb_encoder.RotaryClass(debug = 1)
    test.callback(1)
    time.sleep(.5)
    test.callback(1)
    time.sleep(.5)
    test.callback(1)
    time.sleep(.5)
    test.callback(-1)
    print "testing button... please push the encoder or enter"
    pos,pushed = test.get_state()
    print "pos: "+str(pos)+" pushed: "+str(pushed)
