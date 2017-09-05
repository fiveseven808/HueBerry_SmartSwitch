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

class Upgrader(object):
    def __init__(self,console=0,mirror = 0,help = 0,simulate = 0,legacy = 0, branch = "dev"):
        self.req_modules = ['hb_display',
                            'hb_encoder',
                            'hb_hue',
                            'hb_settings',
                            'hb_menu',
                            #'hbplugin'
                            'hb_morse',
                            'hueberry',
                            'console_colors',
                            'hb_sceneUpdater',
                            'everything_else',
                            'authenticate']
        self.everything_else = ['r2hb',
                                'tom-thumb.psf',
                                'splashscreen.py']
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
            if x == 'console_colors':
                self.download_hb_module(x)
            if x == 'authenticate':
                self.download_hb_module(x)
            if x == 'hb_hue':
                self.download_hb_module(x)
            if x == 'hb_settings':
                self.download_hb_module(x)
            if x == 'hb_menu':
                self.download_hb_module(x)
            if x == 'hb_morse':
                self.download_hb_module(x)
            if x == 'hb_sceneUpdater':
                self.download_hb_module(x)
        for x in self.everything_else:
                self.download_everything_else(x)
        #print baremetal

    def download_hb_module(self,module):
        x = module
        print("Installing " +str(x))
        self.hb_display.display_max_text("Installing " +str(x))
        self.myrun("rm "+str(x)+".py; wget https://raw.githubusercontent.com/fiveseven808/HueBerry_SmartSwitch/"+str(self.branch)+"/"+str(x)+".py")
        print("Done installing " +str(x)+"\n")
        self.hb_display.display_max_text("Done installing " +str(x)+" library\n\n")

    def download_everything_else(self,individual_file):
        x = individual_file
        print("Installing " +str(x))
        self.hb_display.display_max_text("Installing " +str(x))
        self.myrun("rm "+str(x)+"; wget https://raw.githubusercontent.com/fiveseven808/HueBerry_SmartSwitch/"+str(self.branch)+"/"+str(x))
        print("Done installing " +str(x)+"\n")
        self.hb_display.display_max_text("Done installing " +str(x)+" file\n\n")

    def out_with_the_old(self):
        self.myrun("sudo mv upgrade_hb.py upgrade_hb_old.py")
        self.myrun("sudo mv new_upgrade_hb.py upgrade_hb.py")
        self.myrun("sudo chown pi upgrade_hb.py")
        self.myrun("sudo chown pi upgrade_hb_old.py")
        self.myrun("sudo chmod +x r2hb")
        for x in self.req_modules:
            self.hb_display.display_max_text("Updating Permissions for: "+str(x))
            self.myrun("sudo chown pi "+str(x)+".py")
        for x in self.everything_else:
            self.hb_display.display_max_text("Updating Permissions for: "+str(x))
            self.myrun("sudo chown pi "+str(x))
        #self.hb_display.display_2lines("Upgrade Finished!","Rebooting...",13)


    def display_exit_msg(self):
        # Instead of dumping out some text to the screen
        # Maybe I should download a change.log or something
        # Then I could just cat that onto the screen, and there'd be a
        # local copy for whomever to look at later....
        finalreadme = """
    \rUpgrade level: v051-0905.57.a
        2017-09-05 //57
        * I really want to update the master branch... So this is some simple modifications to undo the dev features
        - Scene upgrader removed and placeholder in place right now
        + Added WPBack's 3d printable model of the hueBerry case!!!
        + Want to push to master! 
        
        2017-08-26 //57
        + Added hb_sceneUpdater module. Not really integrated yet..
        * DEV RELEASE ONLY. DO NOT UPDATE THIS. 
        
        2017-04-30 //57
        + Fixed a bug preventing scenes from being created
        """
        #self.myrun("echo "+str(finalreadme)+" > release_notes.txt; sudo chown pi release_notes.txt")
        print(finalreadme)
        return finalreadme

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
            upgrader = new_upgrade_hb.Upgrader(legacy = 1)
        else:
            upgrader = new_upgrade_hb.Upgrader(console = debug_argument,mirror = mirror_mode,help = disp_help,simulate = simulate_arg)
    #Do a blind upgrade lol don't even check
    #upgrader.check_modules_exist()
    upgrader.download_all_modules()
    upgrader.display_exit_msg()
    upgrader.out_with_the_old()
