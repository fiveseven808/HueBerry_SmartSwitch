import authenticate
import os

if os.path.isfile('./auth.json') == False:
    raw_input("Press the Link Button on your Bridge then Press Enter to continue...")
    # fix this so you can accept a button push from your dimmer instead.
    ip = authenticate.search_for_bridge()
    authenticate.authenticate('testapp',ip)
else:
    authenticate.load_creds()
    print(authenticate.api_key)
    print(authenticate.bridge_ip)
