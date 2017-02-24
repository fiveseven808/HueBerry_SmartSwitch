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

        1330
        0.40s Transition time now has no transition time (so it can be used with
        other programs that just turn on lights)
        upgrade_hb.py's updater now updates itself or at least tries to.

        1609
        bug fixes for the 0.40s transition time. Apparently the bridge now responds
        to on=false and other things. or maybe it always did... idk.

        1725
        Rearranged the clock thing... it now does stuff! :D
        Mash the button for 1.5 seconds and it will toggle all the lights in the house
        Not sure how useful this is for people with rooms they don't always use
        But it was a requested feature.

        1754
        Button routines optimized for console
        bug fixes

        2003
        changed house toggle from 3s to 1.5s

        2233
        added scene explorer function template. not yet linked
        also modified hb_display. gave the auto resize function an offset
        integrated the holding button thing to use that new thing instead of custom
        """
        #self.myrun("echo "+str(finalreadme)+" > release_notes.txt; sudo chown pi release_notes.txt")
        print(finalreadme)

if __name__ == "__main__":
    import sys
    import os
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
    wget_results = os.popen("sudo rm new_upgrade_hb.py; wget https://raw.githubusercontent.com/fiveseven808/HueBerry_SmartSwitch/dev/upgrade_hb.py --output-document=new_upgrade_hb.py -o upgrade.log; cat upgrade.log |  grep ERROR").read()
    if wget_results:
        print("Could not download the file for whatever reason")
        print("Returning to previous state")
        print("There are no changes or upgrades avaliable")
        #hb_display.display_2lines("Could not connect","to server :(",13)
        time.sleep(2)
        sys.exit()
    else:
        print("File Downloaded Successfully! Comparing...")
        #hb_display.display_2lines("Comparing","Versions...",15)
    #Change this to an upgrade only file. Smaller, easier and quicker to check if it just contains a version number and a changelog
    if os.path.isfile('./upgrade_hb.py') == False:
        #Make sure to make some noise if this is a much older version.
        diff_result = 1
    else:
        diff_result = os.popen("diff upgrade_hb.py new_upgrade_hb.py").read()
    #diff_result = os.popen("diff upgrade_hb.py upgrade_hb.py").read()
    if not diff_result:
        print("There are no changes or upgrades avaliable")
        #hb_display.display_2lines("You are","up to date! :)",15)
        time.sleep(2)
        sys.exit()
    else:
        print("It looks like there are changes avaliable. Installing...")
        decision_result = 1
        #Answering Yes automatically
        if (decision_result != 1):
            #hb_display.display_2lines("Canceling...","Returning...",15)
            os.popen("rm new_upgrade_hb.py")
            time.sleep(1)
            sys.exit()
        #hb_display.display_2lines("Upgrading!!!","Please wait...",15)
        import new_upgrade_hb
        #import upgrade_hb
        #upgrader = new_upgrade_hb.upgrader(simulate = 1)
        if diff_result == 1:
            #Legacy switch, currently does nothing...
            upgrader = new_upgrade_hb.upgrader(legacy = 1)
        else:
            upgrader = new_upgrade_hb.upgrader(console = debug_argument,mirror = mirror_mode,help = disp_help,simulate = simulate_arg)
    #Do a blind upgrade lol don't even check
    #upgrader.check_modules_exist()
    upgrader.download_all_modules()
    upgrader.display_exit_msg()
    upgrader.out_with_the_old()
