#!/usr/bin/env python
"""
Python upgrader for hueberry.
Readme for current version is in display_exit_msg()
"""
#import os
#import shutil
#import imp
import subprocess
#import shlex
import hb_display
import time
import sys

class upgrader(object):
    def __init__(self,console=0,mirror = 0,help = 0,simulate = 0,legacy = 0, branch = "dev"):
        self.req_modules = ['hb_display','hb_encoder','hueberry']
        self.debug_argument = console
        self.mirror_mode = mirror
        self.help = help
        self.simulate = simulate
        self.legacy = legacy
        self.branch = branch
        if (self.help == 1):
            self.print_usage()
            sys.exit()
        if(self.mirror_mode == 1):
            #If mirror mode, then console is implied, otherwise, it would be straight display
            self.hb_display = hb_display.display(console = 1,mirror = self.mirror_mode)
        else:
            #If mirror mode was not selected, then you can do whatever you want
            self.hb_display = hb_display.display(console = self.debug_argument,mirror = self.mirror_mode)

    def print_usage(self):
        usage = """
        How to run:
            sudo python ugprade_hb.py [-m] [-s] [-h,--help]

        -m          Turns on mirror mode. Outputs to the
                    display as well as the terminal.

        -s          Simulates the upgrade without actually
                    downloading and overwriting files

        -h,--help   Displays this help text
        """
        print(usage)

    def myrun(self,cmd):
        """
        from http://blog.kagesenshi.org/2008/02/teeing-python-subprocesspopen-output.html
        """
        if (self.simulate == 1):
            print("Simulating command: "+cmd)
            time.sleep(1)
            return
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout = []
        while True:
            line = p.stdout.readline()
            stdout.append(line)
            print line,
            if line == '' and p.poll() != None:
                break
        return ''.join(stdout)


    class bcolors:
        PRPL = '\033[95m'
        BLU = '\033[94m'
        GRN = '\033[92m'
        YLO = '\033[93m'
        RED = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'

    def check_modules_exist(self):
        print(self.bcolors.BOLD+"Checking required modules. Please wait..."+self.bcolors.ENDC)
        self.hb_display.display_max_text("Checking required modules. \nPlease wait...")
        n2install = []
        #Go and check if things exist althouhg.... not really using it right now lol
        for x in self.req_modules:
            try:
                new_module = __import__(x)
                found = True
            except ImportError:
                print("    " + self.bcolors.YLO + str(x) + self.bcolors.ENDC + self.bcolors.RED + " module not found!"+self.bcolors.ENDC)
                n2install.append(x)
        print("\r")
        #n2install would be returned, but i don't really care about this right now...

    def download_all_modules(self):
        baremetal = 0
        #for x in n2install:
        #Just go and delete and re-download everything in self.req_modules LOL
        for x in self.req_modules:
            if x == 'hb_display':
                self.download_hb_module(x)
            if x == 'hb_encoder':
                self.download_hb_module(x)
            if x == 'hueberry':
                self.download_hb_module(x)
        #print baremetal

    def download_hb_module(self,module):
        x = module
        print("Installing " +str(x))
        self.hb_display.display_max_text("Installing " +str(x))
        self.myrun("rm "+str(x)+".py; wget https://raw.githubusercontent.com/fiveseven808/HueBerry_SmartSwitch/"+str(self.branch)+"/"+str(x)+".py")
        print("Done installing " +str(x)+"\n")
        self.hb_display.display_max_text("Done installing " +str(x)+" library\n\n")

    def out_with_the_old(self):
        self.myrun("sudo mv upgrade_hb.py upgrade_hb_old.py")
        self.myrun("sudo mv new_upgrade_hb.py upgrade_hb.py")
        self.myrun("sudo chown pi upgrade_hb.py")
        self.myrun("sudo chown pi upgrade_hb_old.py")
        for x in self.req_modules:
            self.hb_display.display_max_text("Updating Permissions for: "+str(x))
            self.myrun("sudo chown pi "+str(x)+".py")
        #self.hb_display.display_2lines("Upgrade Finished!","Rebooting...",13)


    def display_exit_msg(self):
        # Instead of dumping out some text to the screen
        # Maybe I should download a change.log or something
        # Then I could just cat that onto the screen, and there'd be a
        # local copy for whomever to look at later.... 
        finalreadme = """
    \rUpgrade level: v044-20170222-1233
    //57
        20170222-1158
        Added Unicode Support
            Scenes now are generated properly with unicode light names
        Unicode Display support currently untested

        20170222-1233
        Final Readme is now easier to read
        """
        #self.myrun("echo "+str(finalreadme)+" > release_notes.txt; sudo chown pi release_notes.txt")
        print(finalreadme)

if __name__ == "__main__":
    import upgrade_hb
    import sys
    debug_argument = 0
    mirror_mode = 0
    simulate_arg = 0
    disp_help = 0
    for arg in sys.argv:
        if arg == '-d':
            debug_argument = 1
        if arg == '-m':
            mirror_mode = 1
        if arg == '-s':
            simulate_arg = 1
        if arg in ("-h","--help"):
            disp_help = 1
    upgrader = upgrade_hb.upgrader(console = debug_argument,mirror = mirror_mode,help = disp_help,simulate = simulate_arg)
    #Do a blind upgrade lol don't even check
    #upgrader.check_modules_exist()
    upgrader.download_all_modules()
    upgrader.display_exit_msg()
    upgrader.out_with_the_old()
