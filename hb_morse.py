import time
import os
import sys


"""
hueBerry Morse Code generator / ip2morse

What this module does is that it can take control of a Pi Zero's LED and send morse code out of it
When the module exists (if run as self), the LED should resume normal operation

Arguments:
    -c          Send the morse code output to console instead of led for easy viewing/debugging

    -d          Use the IP of 127.0.0.1 to test the system in case ifconfig wlan0 is unavailable
                (-d overrides -i)

    -i          Send your own text through the module!

    -m          Mirror morse code of the LED in the console (implies -c)


Usage:
    import hb_morse.py
    hb_morse.i2pmorse(mirror = 1)
"""
DIT = 0.1                   # Short Mark: Single Time Unit
DAH = DIT * 3               # Longer Mark
INTER_ELEMENT_GAP = DIT     # Between Characters
SHORT_GAP = DAH             # Between Letters
MEDIUM_GAP = DIT * 7        # Between Words

def print_no_newline(string):
    sys.stdout.write(string)
    sys.stdout.flush()

def save_and_kill_triggers():
    triggers = os.popen("cat /sys/class/leds/led0/trigger").read()
    os.popen("echo none | sudo tee /sys/class/leds/led0/trigger").read()
    return triggers

def resume_triggers(triggers):
    os.popen("echo " + triggers + " | sudo tee /sys/class/leds/led0/trigger").read()

def led_off():
    os.popen("echo 1 | sudo tee /sys/class/leds/led0/brightness").read() #turn led off

def led_on():
    os.popen("echo 0 | sudo tee /sys/class/leds/led0/brightness").read() #turn led on

CODE = {'\n': ' ',
        ' ': ' ',
        "'": '.----.',
        '(': '-.--.-',
        ')': '-.--.-',
        ',': '--..--',
        '-': '-....-',
        '.': '.-.-.-',
        '?': '..--..',
        '/': '-..-.',
        '@': '.--.-.',
        '0': '-----',
        '1': '.----',
        '2': '..---',
        '3': '...--',
        '4': '....-',
        '5': '.....',
        '6': '-....',
        '7': '--...',
        '8': '---..',
        '9': '----.',
        ':': '---...',
        ';': '-.-.-.',
        '?': '..--..',
        'A': '.-',
        'B': '-...',
        'C': '-.-.',
        'D': '-..',
        'E': '.',
        'F': '..-.',
        'G': '--.',
        'H': '....',
        'I': '..',
        'J': '.---',
        'K': '-.-',
        'L': '.-..',
        'M': '--',
        'N': '-.',
        'O': '---',
        'P': '.--.',
        'Q': '--.-',
        'R': '.-.',
        'S': '...',
        'T': '-',
        'U': '..-',
        'V': '...-',
        'W': '.--',
        'X': '-..-',
        'Y': '-.--',
        'Z': '--..',
        '_': '..--.-'}


def dot(console_var = 0, mirror = 0):
    if console_var == 0 or mirror == 1:
        led_on()
        time.sleep(DIT)
        led_off()
    if console_var == 1 or mirror == 1:
        print_no_newline(".")
        time.sleep(DIT)
    time.sleep(INTER_ELEMENT_GAP)

def dash(console_var = 0, mirror = 0):
    if console_var == 0 or mirror == 1:
        led_on()
        time.sleep(DAH)
        led_off()
    if console_var == 1 or mirror == 1:
        print_no_newline("-")
        time.sleep(DAH)
    time.sleep(INTER_ELEMENT_GAP)

def ip2morse(console_var = 0, mirror = 0):
    if console_var == 0 or mirror == 1:
        # Turn LED off for a second so yo know it'll start sending info
        led_off()
        time.sleep(1)
    #get wifi ip address
    ipaddress = os.popen("ifconfig wlan0 | grep 'inet addr' | awk -F: '{print $2}' | awk '{print $1}'").read()
    print ipaddress
    while True:
        send2morse(console_var,ipaddress, mirror)

def input2morse(console_var = 0, input = None, mirror = 0):
    while True:
        if input == None:
            input = raw_input('What would you like to send? ')
        send2morse(console_var, input, mirror)

def send2morse(console_var, input, mirror = 0):
        for letter in input:
                for symbol in CODE[letter.upper()]:
                    if symbol == '-':
                        dash(console_var, mirror)
                    elif symbol == '.':
                        dot(console_var, mirror)
                    else:
                        time.sleep(MEDIUM_GAP)
                if console_var == 1 or mirror == 1:
                    print_no_newline(" ")
                time.sleep(DAH)
        print_no_newline(" ")
        time.sleep(DAH*2)


if __name__ == "__main__":
    global CONSOLE
    global PRESET
    CONSOLE = 0
    PRESET = 0
    INPUT = 0
    MIRROR = 0
    for arg in sys.argv:
        if arg == '-c':
            CONSOLE = 1
        if arg == '-d':
            PRESET = "127.0.0.1"
        if arg == '-i':
            INPUT = 1
        if arg == '-m':
            MIRROR = 1
    if not os.geteuid() == 0 and CONSOLE == 0:
        sys.exit('Script must be run as root for LED functionality')
    import hb_morse
    print("Running... Ctrl + C to quit!")
    try:
        if CONSOLE == 0:
            triggers = hb_morse.save_and_kill_triggers()
        if PRESET != 0:
            hb_morse.input2morse(CONSOLE, PRESET, MIRROR)
        elif INPUT == 0:
            hb_morse.ip2morse(CONSOLE, MIRROR)
        elif INPUT == 1:
            hb_morse.input2morse(console_var = CONSOLE, mirror = MIRROR)
    except(KeyboardInterrupt,SystemExit):
        if CONSOLE == 0:
            print("\nReturning control of LED...")
            print triggers
            hb_morse.resume_triggers(triggers)
        print("\nExiting Gracefully")
