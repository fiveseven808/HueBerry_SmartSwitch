# created by @innocuoussoul (https://github.com/innocuoussoul/)

from authenticate import *

raw_input("Press the Link Button on your Bridge then Press Enter to continue...")
# fix this so you can accept a button push from your dimmer instead.

# this searches for the bridge on the network 
ip = search_for_bridge()

# this creates the api key
authenticate('testapp',ip)

# this creates your auth.json, set the path in authenticate.py
save_username()

