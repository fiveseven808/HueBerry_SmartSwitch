#!/usr/bin/env python
"""
Python upgrader for hueberry.
v001
//57
    Initial upgrade test. Everytime this gets updated, the hueberry should
    detect that an upgrade is avaliable, and follow the instructions here by
    wiping the files and redownloading them. Easiest way to get shit done right
    now without having to do anything complicated diffs on existing files.
"""
#import os
#import shutil
#import imp
import subprocess
#import shlex
import hb_display

class upgrader(object):
    def __init__(self,console=0,mirror = 0,help = 0):
        req_modules = ['hb_display','hb_encoder','hueberry']
        self.debug_argument = console
        self.mirror_mode = mirror
        self.help = help
        if (self.help == 1):
            self.print_usage()
            sys.exit()
        if(mirror_mode == 1):
            #If mirror mode, then console is implied, otherwise, it would be straight display
            hb_display = hb_display.display(console = 1,mirror = self.mirror_mode)
        else:
            #If mirror mode was not selected, then you can do whatever you want
            hb_display = hb_display.display(console = self.debug_argument,mirror = self.mirror_mode)

    def print_usage(self):
        usage = """
        How to run:
            sudo python ugprade_hb.py [-m] [-h,--help]

        -m          Turns on mirror mode. Outputs to the
                    display as well as the terminal.

        -h,--help   Displays this help text
        """
        print(usage)

    def myrun(self,cmd):
        """
        from http://blog.kagesenshi.org/2008/02/teeing-python-subprocesspopen-output.html
        """
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
        print(bcolors.BOLD+"Checking required modules. Please wait..."+bcolors.ENDC)
        hb_display.display_max_text("Checking required modules. \nPlease wait...")
        n2install = []
        #Go and check if things exist althouhg.... not really using it right now lol
        for x in self.req_modules:
            try:
                new_module = __import__(x)
                found = True
            except ImportError:
                print("    " + bcolors.YLO + str(x) + bcolors.ENDC + bcolors.RED + " module not found!"+bcolors.ENDC)
                n2install.append(x)
        print("\r")
        #n2install would be returned, but i don't really care about this right now...

    def download_all_modules(self):
        baremetal = 0
        #for x in n2install:
        #Just go and delete and re-download everything in self.req_modules LOL
        for x in self.req_modules:
            if x == 'hb_display':
                print("Installing " +str(x))
                hb_display.display_max_text("Installing " +str(x))
                self.myrun("rm "+str(x)".py; wget https://raw.githubusercontent.com/fiveseven808/HueBerry_SmartSwitch/dev/"+str(x)".py")")
                print("Done installing " +str(x)+"\n\n")
                hb_display.display_max_text("Done installing " +str(x)+"\n\n")
            if x == 'hb_encoder':
                print("Installing " +str(x))
                hb_display.display_max_text("Installing " +str(x))
                self.myrun("rm "+str(x)".py; wget https://raw.githubusercontent.com/fiveseven808/HueBerry_SmartSwitch/dev/"+str(x)".py")")
                print("Done installing " +str(x)+"\n\n")
                hb_display.display_max_text("Done installing " +str(x)+"\n\n")
            if x == 'hueberry':
                print("Installing " +str(x))
                hb_display.display_max_text("Installing " +str(x))
                self.myrun("rm "+str(x)".py; wget https://raw.githubusercontent.com/fiveseven808/HueBerry_SmartSwitch/dev/"+str(x)".py")
                print("Done installing " +str(x)+"\n\n")
                hb_display.display_max_text("Done installing " +str(x)+"\n\n")
        #print baremetal

    def display_exit_msg(self):
        finalreadme = """
        \rUpgrade level: v043-20170221-1527
        //57
            Initial upgrade test. Everytime this gets updated, the hueberry should
            detect that an upgrade is avaliable, and follow the instructions here by
            wiping the files and redownloading them. Easiest way to get shit done right
            now without having to do anything complicated diffs on existing files.
        """
        print(finalreadme)

if __name__ == "__main__":
    import upgrade_hb
    import sys
    debug_argument = 0
    mirror_mode = 0
    disp_help = 0
    for arg in sys.argv:
        if arg == '-d':
            debug_argument = 1
        if arg == '-m':
            mirror_mode = 1
        if arg in ("-h","--help"):
            disp_help = 1
    upgrader = upgrade_hb.upgrader(console = debug_argument,mirror = mirror_mode,help = disp_help)
    upgrader.check_modules_exist()
    upgrader.download_all_modules()
    upgrader.display_exit_msg()
