#!/usr/bin/python
import hb_display
import sys

with open(FileName) as f:
  newText=f.read().replace('A', 'Orange')

with open(FileName, "w") as f:
  f.write(newText)

  
"""
What do I want this file to do? lol

well i bought a new light that i want to use to upgrade a normal light... 
but i dont want to go and change all of the scenes on my hueberries invidicually..

so i need to build a scene upgrader

what does this consist of? 
well, i have the scene files... 
i need to figure out how create a class that does the following:
    - This class will go and look for a specific string (i.e. a light) and replace it with a new string (i.e. new light) 
    - since the old light is now moved, there's no need to put it in the scene files it can just stay out
    
EXTRA FEATURES
    - well i've always wanted to do a thing that did a "lights ignore" bit or room ignore
        i.e. for my guest room, i dont want it to be controlled sometime... or all the time
        but i still want to use scene files...
        maybe this scene updater can have a kill guest room or something function
        i.e. i dont want group 4 lights in my scenes, so it'll go and identify all lights associated with group 4
        then delete them all from all of the avaliable scenes. 
        AND somehow save the preference and make it viewable. i.e. i look at what groups/lights are removed from scenes and then it'll
        tell me which ones are now removed. and then new scene generation will also ignore/remove these lights
        since scene generation is kind of a pain in the butt, maybe we'll just run this script/method afterwards 
        and then it'll cull the lights from the scene files?
        
        
"""

"""
planning: 
how is this code going to do this? 
class? 
library? 
just include some functions lol. 
"""
#we'll have like, something that'll be like
def hb_SceneUpgrader(old_light, new_light, scene_dir)
    """
    Start opening up the files in scenedir one by one 
    for each scene in scene_dir 
        display out and show status? 
        open the file for reading and writing
        display out and show status? 
        use the replace function to replace old_light with new_light
        close the file 
        display out and show status? 
    """
    return status

#and we'll also have something like this
def hb_SetIgnore(light_or_group, number_to_ignore, scene_number)
    """
    if scene_number == 0
        run though and ignore all scenes
    else 
        only run through the scene_number scene
    if light_or_group == "l"
       ignore a single light in number_to_ignore
    if light_or_group == "g"
        expect that number_to_ignore is an array (since it'd be too hard to have this call a function to figure out whats in that group)
        handle and cycle through the array? (although maybe this can also handle the above function... so maybe above is not needed?) 
    """
    return status