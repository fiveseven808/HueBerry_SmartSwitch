import pickle
import os

class Settings(object):

    __filename = "settings.p"

    # Settings-variables that are saved to the file
    __time_format = True

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

    # Changes the time format
    def ToggleTimeFormat(self):
        self.__time_format = not self.__time_format
        self.Save()

    # Gets the time format
    def GetTimeFormat(self):
        return self.__time_format

# For testing
if __name__ == "__main__":
    import hb_settings

    print("Running hb_settings module self test...")
    settings = hb_settings.Settings()
    print("Object initialized")
    print(settings.GetTimeFormat())
    settings.ToggleTimeFormat()
    print(settings.GetTimeFormat())
