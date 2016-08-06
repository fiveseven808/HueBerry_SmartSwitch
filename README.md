HueBerry: DimmerDial
=============
## Smart dial for the Philips Hue lighting system 


### Summary: Updated 8/6/2016
You can build a dedicated device with a Raspberry Pi to QUICKLY change between scenes and control your lights!!! 

##### Program is currently in pre-alpha
##### No instructions at the moment. 

### Bonus:

>  * Clock! Dims (ish) during night time
>  * It works! 


**Instructions as of 8/6/16**  
**Requirements:**

  * Raspberry Pi (I used a Zero)
  * Adafruit_SSD1306 library
  * pigpio library
  * SSD1306 compatible display (128x64 resolution)
  * Rotary encoder switch thing 
	
**Instructions:**

  1. None at the moment... 
  2. Currently v002.py works.
		
		  	 
**Wishlist:**

  * Gotta clean up repo and get rid of my "training" files
  * Better menu system
  * Ability to control individual lights and their brightness, hue, sat, CT, etc...
  * Ability to control groups of lights and their brightness, hue, sat, CT, etc... 
  * INI based configuration 
  * Auto hub detection
  * Hub Pairing (Store API key in INI?) 
  * Timeout to clock
  * Disable clock via INI
  * PIR integration
  * Lower power consumption (stop refreshing display so often and polling button)
  * Battery state support and icon (low power indicator and graceful shutdown too)
  * C rewrite to make use of faster display interface
  * Python SSD1306 driver optimization to try and speed things up
	
	
**License:** 

[Creative Commons Attribution-NonCommercial 4.0 International ](https://creativecommons.org/licenses/by-nc/4.0/)  

This is a pre-alpha program. Don't blame me for anything and you may not use this against me... although you probably could... 