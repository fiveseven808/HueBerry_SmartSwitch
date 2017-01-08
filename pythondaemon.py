# process damon. 
#run this from home path (~) not from this folder. have rc.local start it and run it in the background. 
import os
import os.path
import time 
logfile = "/home/pi/pythondaemon.log"

current_time = time.strftime("%m / %d / %Y %-H:%M")
with open(logfile, "a") as myfile:
    myfile.write(current_time + " pythondaemon is starting up\n")
#print "should've written by now"

time.sleep(20)

while True:
    time.sleep(10)
    result = os.popen("ps ax | grep smartswitch").read()
    result_array = result.split('\n')
    #print (result_array)
    numofprocs = len(result_array)
    if (numofprocs < 4 ):
        #print("num of procs is greater! ")
        #os.popen("sudo /etc/rc.local")
        #os.popen("sudo shutdown -r now")
        os.popen("nice --10 python /home/pi/scripts/smartswitch/v028.py &")
        current_time = time.strftime("%m / %d / %Y %-H:%M")
        with open(logfile, "a") as myfile:
            myfile.write(current_time + " pythondaemon reset the program\n")

    #else:
    #    print("num of procs is less! ")
    #print numofprocs
