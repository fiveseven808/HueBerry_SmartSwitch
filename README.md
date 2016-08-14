HueBerry: DimmerDial
=============
## Smart dial for the Philips Hue lighting system 

[![Learn About the hueBerry!](http://i.imgur.com/zl9XxJq.jpg)](https://youtu.be/YTvbsL82ZcM?t=1m3s "hueBerry is awesome!")

### Summary: Updated 8/13/2016
You can build a dedicated device with a Raspberry Pi to QUICKLY change between scenes and control your lights!!! 

##### Program is currently in pre-alpha
##### No instructions at the moment. 

### Bonus:

>  * Clock! Dims (ish) during night time
>  * It works! 
>  * Groups and individual Lights work now! 
>  * Pulls information from the hub!


**Instructions as of 8/6/16**  
**Requirements:**

  * Raspberry Pi (I used a Zero)
  * Adafruit_SSD1306 library
  * pigpio library
  * SSD1306 compatible display (128x64 resolution)
  * Rotary encoder switch thing 
  * Full BOM located [here](https://docs.google.com/spreadsheets/d/18q5wE9IcbJ1D823ktt4ZN7Fp1JHZutR4hCld2env4vI/edit?usp=sharing)
	
**Instructions:**

  1. None at the moment... 
  2. Whatever the latest v00*.py probably works.
  3. You're gonna have to dig into the code and replacce with your bridge IP and API key. (If you have to ask what this is, the project isn't ready for you yet). 
		
		  	 
**Wishlist:**

  * Gotta clean up repo and get rid of my "training" files
  * More refined menu system programming
  * Ability to control things other than just brightness, hue, sat, CT, etc...
  * INI based configuration 
  * Auto hub detection
  * Hub Pairing (Store API key in INI?) 
  * Timeout to clock
  * Disable clock via settings
  * PIR integration?
  * Lower power consumption (stop refreshing display so often and polling button)
    * Can't do much regarding this though... 0.7w is about as low as it goes... unless you power it off... 
  * Battery state support and icon (low power indicator and graceful shutdown too)
    * Coming soon 
  * C rewrite to make use of faster display interface
    * Not really necessary anymore? 
  * Wifi detection and selection as well as password selection and clear settings
    * Gonna try a WPS implementation 
	
	
**License:** 

[Creative Commons Attribution-NonCommercial 4.0 International ](https://creativecommons.org/licenses/by-nc/4.0/)  

This is a pre-alpha program. Don't blame me for anything and you may not use this against me... although you probably could... 