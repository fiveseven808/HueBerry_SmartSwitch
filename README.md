HueBerry: Smart Switch
=============
## IoT Smart Switch for the Philips Hue lighting system

[![Learn About the hueBerry!](http://i.imgur.com/zl9XxJq.jpg)](https://youtu.be/YTvbsL82ZcM?t=1m3s "hueBerry is awesome!")

###### Video updated 8/13/2016 *(Outdated)*

## [Discord Channel here!](https://discord.gg/YxUusf8)

## Summary: Updated 2/7/2017
The hueBerry is a dedicated device based on a Raspberry Pi Zero to QUICKLY record and change between Whole house scene! Want to transition your entire home to "bed time" over 30 seconds? now you can! Want in instantaneous "emergency" mode? Now you can do that with ease! It also lets you to control the color temperature and Hue and saturation of individual groups through a quick and friendly interface! No fumbling with a phone or table or PC, just spin and click and spin!
##### Program is currently in open beta


### Features: Updated 9/05/2017

>  * [3D Printable Case!!! Courtsey of Daniel Back](https://www.thingiverse.com/thing:2180872)
>  * Clock! Dims (slightly) during night time (currently hard coded to 9pm)
>  * Control whole Groups and individual Lights!
>  * Control Color temperature and Hue and Saturation of lights OR groups! (for that precise control!)
>  * Assign quick actions to conveniently toggle your lights or set your favorite scene! 
>  * Flashlight mode lol
>  * Create then save whole house scenes with the push of a button! Replay and edit them just as easily!
>  * Adjust the transition time of the whole house scenes between Instant and 30 seconds!

### Technical Features: 

>  * Main menu times out to clock after 30 seconds (customization coming soon)
>  * Automatic Bridge detection and pairing initiation
>  * Scan and Connect to WiFi via WPS!
>  * Settings menu allowing Pi resets, shutdown, and Device and bridge info
>  * One command line install for super easy setup! (beta)
>  * OTA software upgrades!
>  * Unicode support! (beta)
>  * **Undocumented features**
>   * Non WPS WiFi APs added by a text file in the /boot partition
>   * Firmware upgrade possible via placing a special file in the /boot partition
>   * Console and Console Mirroring mode available (for remote debugging/control)


**Requirements:**

  * Optional: [3D Printable Case!!! Courtsey of Daniel Back](https://www.thingiverse.com/thing:2180872)
  * Raspberry Pi (a Zero W is suggested for size reasons)
  * Adafruit_SSD1306 library
  * pigpio library
  * SSD1306 compatible display (128x64 resolution)
  * Rotary encoder with momentary switch
  * Full BOM located [here](https://docs.google.com/spreadsheets/d/18q5wE9IcbJ1D823ktt4ZN7Fp1JHZutR4hCld2env4vI/edit?usp=sharing)

## Instructions as of 2/7/17

  * [Detailed instructions for developers available here!](https://github.com/fiveseven808/HueBerry_SmartSwitch/blob/dev/Dev_setup.md)


**Wishlist:**

  * Gotta clean up repo and get rid of my "training" files
  * More refined menu system programming
    * 2/7 update: Menu code is semi dynamic. Need to make every menu like this. Separate class?
  * Timeout to clock
    * 1/29/17 Needs to be configurable. Affect all menus? (not just main tree)
  * Disable clock via settings
  * Implement Guest mode
    * Guest mode will lock the hueBerry to one group or light allowing for ease of use, without "accidentally" affecting the rest of the house
  * PIR integration?
  * IR remote integration?
    * Push buttons on a universal remote to change scenes!
  * Lower power consumption
    * Move to ESP8266 architecture?
  * Battery state support and icon (low power indicator and graceful shutdown too)
    * Need to design
  * Bugs to squash:
    * Currently need to re-pair with bridge if bridge IP changes...
    * If API key doesn't work on boot, self troubleshoot and see if communication to bridge is bad or API key is bad?
	* Does not complain if bridge does not exist on boot
  * Multiple bridge support (looks like the N-UPnP discovery method supports it)
    * Whole house scenes spanning multiple bridges (for those lucky enough to have that problem lol)
  * This project will be shortly branched into a general toolkit and IoT menu platform for Raspberry Pi Zeros (although all Pis can make use of it)
    * The plan involves creating a custom distribution with all of the required files preloaded so that you can get a pi connected to WiFi with just a screen and a rotary encoder. No HDMI tv or USB widget fussing around necessary!
    * This is particularly useful if you find yourself in a situation where you don't have a computer to get started, but you own a smartphone and have an SSH or VNC app on it!



**License:**

[Creative Commons Attribution-NonCommercial 4.0 International ](https://creativecommons.org/licenses/by-nc/4.0/)  
This is an open source beta program supplied with no guarantee.

**Donations:**

If this project has been useful to you, I'd appreciate it if you would buy me a drink! :D

[![](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=7V4SEHWVDNQL6)
