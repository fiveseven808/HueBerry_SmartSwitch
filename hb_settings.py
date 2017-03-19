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
    - Rewrite scene selection and string return to be flexible.
      I want to return the name of the scene selected or the group being controlled
      Also the group or light being controlled... 
"""
class Settings(object):

    __filename = "settings.p"

    # Settings-variables that are saved to the file
    __time_format = True
    # 0:do nothing, 1:turn all lights on, 2:turn all lights off, 3:toggle all lights
    # Should be able to select a specific scene, later project
    __quick_press_action = 1
    __quick_press_mode = "g"
    __quick_press_number = 0
    __quick_press_selected_file = None

    __long_press_action = 2
    __long_press_mode = "g"
    __long_press_number = 0
    __long_press_selected_file = None


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

    # Gets the time format
    def GetTimeFormat(self):
        return self.__time_format

    def SetQuickPressAction(self, action, mode = 0, number = 0 ):
        if action >= 0 and action <= 3:
            pass # set action number is implicit
        elif action == "set_group_or_light":
            self.__quick_press_mode = mode
            self.__quick_press_number = number
        elif action == "set_quick_scene":
            self.__quick_press_selected_file = number
        else:
            return
        self.__quick_press_action = action
        self.Save()

    def GetQuickPressAction(self):
        return self.__quick_press_action

    def get_quick_press_action_SGoL(self):
        return self.__quick_press_mode, self.__quick_press_number

    def get_quick_press_action_SQS(self):
        return self.__quick_press_selected_file

    def __getQuickActionString(self, action, type = 0):
        if action == 0:
            return "Do nothing"
        elif action == 1:
            return "Turn all on"
        elif action == 2:
            return "Turn all off"
        elif action == 3:
            return "Toggle all"
        elif action == "set_group_or_light":
            return "Toggle a group or light"
        elif action == "set_quick_scene":
            return "Running a Scene"
        else:
            return "False value"

    def GetQuickPressActionString(self):
        return self.__getQuickActionString(self.__quick_press_action, type = "quickpress")

    def SetLongPressAction(self, action, mode = 0, number = 0 ):
        if action >= 0 and action <= 3:
            pass # set action number is implicit
        elif action == "set_group_or_light":
            self.__long_press_mode = mode
            self.__long_press_number = number
        elif action == "set_quick_scene":
            self.__long_press_selected_file = number
        else:
            return
        self.__long_press_action = action
        self.Save()

    def GetLongPressAction(self):
        return self.__long_press_action

    def get_long_press_action_SGoL(self):
        return self.__long_press_mode, self.__long_press_number

    def get_long_press_action_SQS(self):
        return self.__long_press_selected_file

    def GetLongPressActionString(self):
        return self.__getQuickActionString(self.__long_press_action, type = "longpress")

# For testing
if __name__ == "__main__":
    import hb_settings

    print("Running hb_settings module self test...")
    settings = hb_settings.Settings()
    print("Object initialized")
    print(settings.GetTimeFormat())
    settings.ToggleTimeFormat()
    print(settings.GetTimeFormat())
