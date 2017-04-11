import pickle
import os

# -----------------------------------------------------------
# Class for all settings that should be saved on restart
# To add more settings, add them as local variables (__ before the name)
# Then create methods to change the setting, and to read the setting
# See the examples ToggleTimeFormat and GetTimeFormat.
# Make sure that you call self.Save() once you have changed a setting
# ----------------------------------------------------------
"""
//57: To-do
    - Setting for night mode start and stop time (outline font)
    - Setting for return to clock, or return to previous selection (for main menu only)
    - Screen saver options
        - date and time move in random positions on the screen?
        - Turn off display after 5 minutes of inactivity? adjustable minutes of inactivity?
"""
class Settings(object):

    __filename = "settings.p"

    # Settings-variables that are saved to the file
    __time_format = True
    # 0:do nothing, 1:turn all lights on, 2:turn all lights off, 3:toggle all lights
    __screen_blanking = False

    __quick_press_dict = {  'action': 1,
                            'mode': "g",
                            'number':0,
                            'file_name': None}

    __long_press_dict = {   'action': 1,
                            'mode': "g",
                            'number':0,
                            'file_name': None}
    __demo_state = False
    __ct_for_color_lights = False


    # Constructor. Loads the previosu version of the object, if there is any
    def __init__(self):
        self.Load()

    # Saves the settings to a file
    def Save(self):
        f = open(self.__filename,'wb')
        pickle.dump(self.__dict__,f,2)
        f.close()

    # Loads the object if it exists
    def Load(self):
        if os.path.isfile(self.__filename):
            f = open(self.__filename,'rb')
            tmp_dict = pickle.load(f)
            f.close()
            self.__dict__.update(tmp_dict)

    # Changes the time format and saves it to the file.
    def ToggleTimeFormat(self):
        self.__time_format = not self.__time_format
        self.Save()

    def toggle_screen_blanking(self):
        self.__screen_blanking = not self.__screen_blanking
        self.Save()

    # Gets the time format
    def GetTimeFormat(self):
        return self.__time_format

    def get_screen_blanking(self):
        return self.__screen_blanking

    def set_quick_press_action(self, action, mode = 0, number = 0, file_name = None):
        if action < 0:
            return
        self.__quick_press_dict ={  'action': action,
                                    'mode': mode,
                                    'number':number,
                                    'file_name': file_name}
        self.Save()

    def get_quick_press_action_dict(self):
        return self.__quick_press_dict

    def get_quick_press_action_string(self):
        return self.__get_quick_action_string(self.__quick_press_dict)

    def set_long_press_action(self, action, mode = 0, number = 0, file_name = None):
        if action < 0:
            return
        self.__long_press_dict ={   'action': action,
                                    'mode': mode,
                                    'number':number,
                                    'file_name': file_name}
        self.Save()

    def get_long_press_action_dict(self):
        return self.__long_press_dict

    def get_long_press_action_string(self):
        return self.__get_quick_action_string(self.__long_press_dict)

    def __get_quick_action_string(self, press_dict):
        if press_dict["action"] == "set_group_or_light":
            return "Toggle "+str(press_dict["mode"])+" " +str(press_dict["number"])
        if press_dict["action"] == "set_quick_scene":
            return "Running Scene: "+str(press_dict["number"])
        if press_dict["action"] == 0:
            return "Do nothing"
        elif press_dict["action"] == 1:
            return "Turn all on"
        elif press_dict["action"] == 2:
            return "Turn all off"
        elif press_dict["action"] == 3:
            return "Toggle all"
        else:
            return "False value"

    def toggle_demo_state(self):
        self.__demo_state = not self.__demo_state
        self.Save()

    def get_demo_state(self):
        return self.__demo_state

    def ct_for_color_lights_actions(self,action):
        if action == 'toggle':
            self.__ct_for_color_lights = not self.__ct_for_color_lights
            self.Save()
        if action == 'whole_group':
            self.__ct_for_color_lights = action
            self.Save()
        if action == 'get':
            return self.__ct_for_color_lights



# For testing
if __name__ == "__main__":
    import hb_settings

    print("Running hb_settings module self test...")
    settings = hb_settings.Settings()
    print("Object initialized")
    print(settings.GetTimeFormat())
    settings.ToggleTimeFormat()
    print(settings.GetTimeFormat())
