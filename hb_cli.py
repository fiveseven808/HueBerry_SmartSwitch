"""
HueBerry CLI

The purpose of this file/module is to provide an external API 
or command line interface with the hueberry commands.

Goals:
    Scenes
        Run/execute them
        Modiy them
        Create them
        Delete them
        Sync them? 
        Update them? 
        
"""
import hueberry

bridge_present = 0

authenticate = hueberry.authenticate.Authenticate()
authenticate.load_creds()
api_key = authenticate.api_key
bridge_ip = authenticate.bridge_ip
api_url = 'http://%s/api/%s' % (bridge_ip,api_key)

#Load the Hue API module so that the hueberry can control hue lights lol
hueapi = hueberry.hb_hue.HueAPI()
#Load the settings-module
settings = hueberry.hb_settings.Settings()

print api_url
