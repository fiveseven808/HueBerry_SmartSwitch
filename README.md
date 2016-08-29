HueBerry: DimmerDial
=============
## Smart dial for the Philips Hue lighting system 

[![Learn About the hueBerry!](http://i.imgur.com/zl9XxJq.jpg)](https://youtu.be/YTvbsL82ZcM?t=1m3s "hueBerry is awesome!")

###### Video updated 8/13/2016 *(Outdated)* 


## Summary: Updated 8/15/2016
You can build a dedicated device with a Raspberry Pi to QUICKLY change between scenes (Whole house scenes supported) and control all of your lights!!! No fumbling with a phone or table or PC, just spin and click like "back in da hanabada days"! 

##### Program is currently in beta as of v012
#### No real instructions at the moment... But feel free to ask questions! 

### Bonus: Updated 8/29/2016

>  * Clock! Dims (ish) during night time
>  * Main menu times out to clock after 30 seconds (customizable in script)
>  * Control Groups and individual Lights! 
>  * Pulls information from the bridge!
>  * Automatic Bridge detection and pairing initiation (if not done before)
>  * Storage of API key and bridge IP in JSON
>  * Flashlight mode because why the hell not
>  * Scan and Connect to WiFi via WPS! 
>  * Change the color temperature of a group by holding down the button on the light! 
>  * Change Hue and Saturation of the light or groups of lights!



### Instructions as of 8/15/16  
**Requirements:**

  * Raspberry Pi (I used a Zero)
  * Adafruit_SSD1306 library
  * pigpio library
  * SSD1306 compatible display (128x64 resolution)
  * Rotary encoder switch thing 
  * Full BOM located [here](https://docs.google.com/spreadsheets/d/18q5wE9IcbJ1D823ktt4ZN7Fp1JHZutR4hCld2env4vI/edit?usp=sharing)
	
**Instructions:**

  1. None at the moment... 
  2. Run pigpiod via "sudo pigpiod"
  3. Run whatever the latest v00*.py is. Should work.
  4. Follow instructions on the screen to pair your hueBerry and bridge
  5. ???
  6. Profit!!!
		
		  	 
**Wishlist:**

  * Gotta clean up repo and get rid of my "training" files
  * More refined menu system programming
    * 8/15 update: getting there slowly...
	* 8/29 update: 
  * INI based configuration?
  * Timeout to clock
	* 8/29 works only for main menu at the moment
  * Disable clock via settings
  * PIR integration?
  * Lower power consumption (stop refreshing display so often and polling button)
    * Can't do much regarding this though... 0.7w is about as low as it goes... unless you power it off...
	* 8/29 update: reworked menu system now lowers power consumption... but pi still sucks power... 
  * Battery state support and icon (low power indicator and graceful shutdown too)
    * Coming soon  
  * Bugs to squash:
	* Currently need to re-pair with bridge if bridge IP changes... 
	
	
**License:** 

[Creative Commons Attribution-NonCommercial 4.0 International ](https://creativecommons.org/licenses/by-nc/4.0/)  

This is a pre-alpha program. Don't blame me for anything and you may not use this against me... although you probably could... 