#!/bin/python

import subprocess
import os
from contextlib import contextmanager
import time

simulate = 0

@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)

def myrun(cmd):
    """
    from http://blog.kagesenshi.org/2008/02/teeing-python-subprocesspopen-output.html
    """
    if (simulate == 1):
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

myrun("sudo apt-get remove python-pil -y")
#myrun("sudo apt-get remove ")
myrun("yes | sudo -H pip install --upgrade psutil")
myrun("yes | sudo -H pip install --upgrade pillow")

myrun("sudo usermod -a -G i2c,spi,gpio pi")
myrun("sudo apt-get install python-dev python-pip libfreetype6-dev libjpeg-dev -y")
myrun("yes | sudo -H pip install --upgrade pip")
myrun("sudo apt-get purge python-pip -y")

myrun("runuser -l pi -c 'git clone https://github.com/rm-hull/luma.examples.git'")
with cd("luma.examples/"):
    myrun("sudo -H pip install -e .")
