/*
  OLED Menu System
  
  Created by Dean, 10th October 2013.
  
  Menu Library from http://jonblack.org/
  OLED Library from Adafruit
*/

#include <MenuSystem.h>
#include <Wire.h>
#include <SPI.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306h.h>

//DEFINES
#define OLED_DC 8
#define OLED_CS 10
#define OLED_CLK 13
#define OLED_MOSI 11
#define OLED_RESET 7
Adafruit_SSD1306h display(OLED_MOSI, OLED_CLK, OLED_DC, OLED_RESET, OLED_CS);

// Menu variables
MenuSystem ms;
Menu mm("");
Menu mu1("Display");
MenuItem mu1_mi1("Display1");
MenuItem mu1_mi2("Display2");
MenuItem mu1_mi3("Display3");
Menu mu2("Settings");
MenuItem mu2_mi1("Settings1");
MenuItem mu2_mi2("Settings2");
MenuItem mu2_mi3("Settings3");

// Example variables
const int UpBtn = 5;       // the number of the pushbutton pin
const int DownBtn = 4;     // the number of the pushbutton pin
const int SelectBtn = 3;   // the number of the pushbutton pin
const int BackBtn = 2;     // the number of the pushbutton pin
int UpButtonState = 0;     // variable for reading the pushbutton status
int DownButtonState = 0;   // variable for reading the pushbutton status
int SelectButtonState = 0; // variable for reading the pushbutton status
int BackButtonState = 0;   // variable for reading the pushbutton status
bool bRanCallback = false;
bool bForward = true;
int line = 10;             // variable for setting display line

// Menu callback function
// In this example all menu items use the same callback.

void on_display1_selected(MenuItem* p_menu_item)
{
  //Serial.println("DISPLAY1 Selected");
  display.setCursor(0,55);
  display.print("DISPLAY1 Selected");
  bRanCallback = true;
  bForward = true;
}
void on_display2_selected(MenuItem* p_menu_item)
{
  //Serial.println("DISPLAY2 Selected");
  display.setCursor(0,55);
  display.print("DISPLAY2 Selected");
  //bRanCallback = false;
  bForward = true;
}
void on_display3_selected(MenuItem* p_menu_item)
{
  //Serial.println("DISPLAY3 Selected");
  display.setCursor(0,55);
  display.print("DISPLAY3 Selected");
  bRanCallback = false;
  bForward = true;
}

void on_settings1_selected(MenuItem* p_menu_item)
{
  //Serial.println("SETTINGS1 Selected");
  display.setCursor(0,55);
  display.print("SETTINGS1 Selected");
  bRanCallback = true;
  bForward = true;
}
void on_settings2_selected(MenuItem* p_menu_item)
{
  //Serial.println("SETTINGS2 Selected");
  display.setCursor(0,55);
  display.print("SETTINGS2 Selected");
  bRanCallback = false;
  bForward = true;
}
void on_settings3_selected(MenuItem* p_menu_item)
{
  //Serial.println("SETTINGS3 Selected");
  display.setCursor(0,55);
  display.print("SETTINGS3 Selected");
  //bRanCallback = false;
  bForward = true;
}

// Standard arduino functions

void setup()
{
  Serial.begin(9600);
  
// by default, we'll generate the high voltage from the 3.3v line internally! (neat!)
  display.begin(SSD1306h_SWITCHCAPVCC);
  
    // initialize the pushbutton pin as an input:
  pinMode(UpBtn, INPUT); 
    // initialize the pushbutton pin as an input:
  pinMode(DownBtn, INPUT); 
      // initialize the pushbutton pin as an input:
  pinMode(SelectBtn, INPUT); 
      // initialize the pushbutton pin as an input:
  pinMode(BackBtn, INPUT); 
  
  display.display(); 		// show splashscreen
  delay(2000);
  display.clearDisplay();   // clears the screen and buffer
  
// Menu setup
  mm.add_menu(&mu1);
  mu1.add_item(&mu1_mi1, &on_display1_selected);
  mu1.add_item(&mu1_mi2, &on_display2_selected);
  mu1.add_item(&mu1_mi3, &on_display3_selected);
  mm.add_menu(&mu2);
  mu2.add_item(&mu2_mi1, &on_settings1_selected);
  mu2.add_item(&mu2_mi2, &on_settings2_selected);
  mu2.add_item(&mu2_mi3, &on_settings3_selected);
  ms.set_root_menu(&mm);
}

void loop()
{
//OLED set up
  display.display(); 		
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(WHITE);
  line=10; //line variable reset
  //Serial.println("");
  
  
// Display Title
  display.setCursor(0,0);
  display.println("MENU");
  
// Display the menu
  Menu const* cp_menu = ms.get_current_menu();
  MenuComponent const* cp_menu_sel = cp_menu->get_selected();
  for (int i = 0; i < cp_menu->get_num_menu_components(); ++i)
  {
    MenuComponent const* cp_m_comp = cp_menu->get_menu_component(i);
    //Serial.print(cp_m_comp->get_name());
    display.setCursor(30,line);
    display.print(cp_m_comp->get_name());
    
    if (cp_menu_sel == cp_m_comp){
      //Serial.print("<<< ");
      display.setCursor(0,line);
      display.print(">>> ");
    }
    line=line+10;
    //Serial.println("");
  } 
 
// read the state of the pushbutton value:
  UpButtonState = digitalRead(UpBtn);
  if (UpButtonState == HIGH) {    
    ms.prev(); 
  } 
  
  DownButtonState = digitalRead(DownBtn);
  if (DownButtonState == HIGH) {   
    ms.next();  
  } 

  SelectButtonState = digitalRead(SelectBtn);
  if (SelectButtonState == HIGH) {   
    ms.select();  
  } 
  
  BackButtonState = digitalRead(BackBtn);
  if (BackButtonState == HIGH) {   
    ms.back();  
  } 
 
  
// Wait for two seconds so the output is viewable
  delay(500);
}