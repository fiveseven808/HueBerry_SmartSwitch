import pickle
import os

# -----------------------------------------------------------
# Class for all settings that should be saved on restart
# To add more settings, add them as local variables (__ before the name)
# Then create methods to change the setting, and to read the setting
# See the examples ToggleTimeFormat and GetTimeFormat.
# Make sure that you call self.Save() once you have changed a setting
# ----------------------------------------------------------

class Settings(object):

    __filename = "settings.p"

    # Settings-variables that are saved to the file
    __time_format = True
    # 0:do nothing, 1:turn all lights on, 2:turn all lights off, 3:toggle all lights
    # Should be able to select a specific scene, later project
    __quick_press_action = 1
    __long_press_action = 2

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

    def SetQuickPressAction(self, action):
        if action >= 0 and action <= 3:
            self.__quick_press_action = action
            self.Save()

    def GetQuickPressAction(self):
        return self.__quick_press_action

    def __getQuickActionString(self, action):
        if action == 0:
            return "Do nothing"
        elif action == 1:
            return "Turn all on"
        elif action == 2:
            return "Turn all off"
        elif action == 3:
            return "Toggle all"
        else:
            return "False value"

    def GetQuickPressActionString(self):
        return self.__getQuickActionString(self.__quick_press_action)

    def SetLongPressAction(self, action):
        if action >= 0 and action <= 3:
            self.__long_press_action = action
            self.Save()

    def GetLongPressAction(self):
        return self.__long_press_action

    def GetLongPressActionString(self):
        return self.__getQuickActionString(self.__long_press_action)

# For testing
if __name__ == "__main__":
    import hb_settings

    print("Running hb_settings module self test...")
    settings = hb_settings.Settings()
    print("Object initialized")
    print(settings.GetTimeFormat())
    settings.ToggleTimeFormat()
    print(settings.GetTimeFormat())
