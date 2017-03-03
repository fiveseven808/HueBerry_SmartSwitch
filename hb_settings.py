import pickle
import os

class Settings(object):

    __time_format = True
    __filename = "settings.p"

    def __init__(self):
        self.Load()

    def Save(self):
        f = open(self.__filename,'wb')
        pickle.dump(self.__dict__,f,2)
        f.close()

    def Load(self):
        if os.path.isfile(self.__filename):
            f = open(self.__filename,'rb')
            tmp_dict = pickle.load(f)
            f.close()
            self.__dict__.update(tmp_dict)

    def ToggleTimeFormat(self):
        self.__time_format = not self.__time_format
        self.Save()

    def GetTimeFormat(self):
        return self.__time_format

if __name__ == "__main__":
    import hb_settings

    print("Running hb_settings module self test...")
    settings = hb_settings.Settings()
    print("Object initialized")
    print(settings.GetTimeFormat())
    settings.ToggleTimeFormat()
    print(settings.GetTimeFormat())
