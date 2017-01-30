HueBerry: DimmerDial
=============
## Smart dial for the Philips Hue lighting system 

[![Learn About the hueBerry!](http://i.imgur.com/zl9XxJq.jpg)](https://youtu.be/YTvbsL82ZcM?t=1m3s "hueBerry is awesome!")

###### Video updated 8/13/2016 *(Outdated)* 


## Summary: Updated 1/29/2017
The hueBerry is a dedicated device based on a Raspberry Pi Zero to QUICKLY record and change between Whole house scene! It also easily enables you to control the color temperature and Hue and saturation of a group control all of your lights!!! No fumbling with a phone or table or PC, just spin and click and spin like "back in da hanabada days"! 

##### Program is currently in open beta
#### No real instructions at the moment... But feel free to ask questions! 

### Features: Updated 1/29/2017

>  * Clock! Dims (ish) during night time (currently hard coded to 9pm) 
>  * Main menu times out to clock after 30 seconds (customization coming soon)
>  * Control Groups and individual Lights! 
>  * Control Color temperature and Hue and Saturation of lights OR groups! 
>  * Automatic Bridge detection and pairing initiation (if not done before)
>  * Settings menu allowing resets, shutdown, and Device and bridge info
>  * Flashlight mode because why the hell not
>  * Scan and Connect to WiFi via WPS! 
>  * Create then save whole house scenes with the push of a button! Replay them back just as easily!
>  * **Undocumented features**
>   * Non WPS WiFi APs added by a text file in the /boot partition
>   * Firmware upgrade possible via placing a special file in the /boot partition


### Instructions as of 1/29/17  
**Requirements:**

  * Raspberry Pi (I used a Zero)
  * Adafruit_SSD1306 library
  * pigpio library
  * SSD1306 compatible display (128x64 resolution)
  * Rotary encoder switch thing 
  * Full BOM located [here](https://docs.google.com/spreadsheets/d/18q5wE9IcbJ1D823ktt4ZN7Fp1JHZutR4hCld2env4vI/edit?usp=sharing)
	
**Instructions:**

  * Detailed instructions for developers available [here!](https://github.com/fiveseven808/HueBerry_SmartSwitch/blob/dev/Dev_setup.md)
		
		  	 
**Wishlist:**

  * Gotta clean up repo and get rid of my "training" files
  * More refined menu system programming
    * 1/29 update: Should use the dynamic light or group menus to influence main menu code
  * Timeout to clock
    * 1/29/17 Needs to be configurable. Affect all menus? (not just main tree) 
  * Disable clock via settings
  * Implement Guest mode
    * Guest mode will lock the hueBerry to one group or light allowing for ease of use, without "accidentally" affecting the rest of the house
  * PIR integration?
  * IR remote integration? 
  * Lower power consumption
    * Move to ESP8266 architecture?
  * Battery state support and icon (low power indicator and graceful shutdown too)
    * Need to design
  * Bugs to squash:
    * Currently need to re-pair with bridge if bridge IP changes... 
    * If API key doesn't work on boot, self troubleshoot and see if communication to bridge is bad or API key is bad? 
  * Dynamically extend main menu with custom scenes 
	
	
**License:** 

[Creative Commons Attribution-NonCommercial 4.0 International ](https://creativecommons.org/licenses/by-nc/4.0/)  
This is an open source beta program supplied with no guarantee.