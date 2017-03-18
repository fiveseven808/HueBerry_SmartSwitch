# authentication code created by adamcharnock (https://github.com/adamcharnock)
# modified by @innocuoussoul
# modified again by fiveseven808 (https://github.com/fiveseven808)
# Requires a minimum of requests 2.4.3 module
# For WSL running Ubuntu 14, you must run 'sudo pip install requests==2.4.3'
from _socket import gethostname
import json
import os
import requests

class Authenticate(object):
    def __init__(self,authfile = None):
        self.USERNAME_SAVE_PATH = authfile or 'auth.json'
        self.api_key = ""
        self.bridge_ip = ""

    def parse_response(self, response):
        json = response.json()
        error = None
        try:
            error = json[0]['error']
            print error
        except (IndexError, KeyError):
            pass

        if error:
            print('ERROR')
            print(error['description'])
        #    return handle_error(error)
        else:
            return json


    def authenticate(self, app_name, bridge_host, client_name=None):
        client_name = client_name or gethostname()
        url = 'http://{}/api'.format(bridge_host)
        response = requests.post(url, json={
            'devicetype': '{}#{}'.format(app_name, client_name),
        })
        data = response.json()
        #json = parse_response(response)
        print('response:')
        print(data[0])
        if 'error' in data[0].keys():
            print('ERROR')
            print('ERROR:',data[0]['error']['description'])
        else:
            print('NO ERROR')
            self.save_creds(data[0]['success']['username'],bridge_host)

    def save_creds(self, username,ip):
        with open(os.path.expanduser(self.USERNAME_SAVE_PATH), 'a') as f:
            f.write(json.dumps({
                'philips-hue': {
                    'api_key': username,
                    'ip':ip,
                }
            }))
        print('Username saved')

    def search_for_bridge(self, timeout=3):
        """Searches for a bridge on the local network and returns the IP if it
        finds one."""
        all_bridges = []
        r = requests.get('http://www.meethue.com/api/nupnp', timeout=timeout)
        bridges = r.json()
        if len(bridges) > 0:
            return bridges[0]['internalipaddress']
        else:
            return None

    def search_for_all_bridges(self, debug = 0, timeout=3):
        """Searches for a bridge on the local network and returns the IP of all
        bridges that it finds"""
        all_bridges = []
        if debug == 0:
            r = requests.get('http://www.meethue.com/api/nupnp', timeout=timeout)
            bridges = r.json()
        else:
            r = os.popen("cat mb_bridge.json").read()
            bridges = json.loads(r)
        if len(bridges) > 0:
            all_bridges = []
            for each_entry in bridges:
                all_bridges.append(each_entry['internalipaddress'])
            return all_bridges
        else:
            return None

    def load_creds(self):
        try:
            with open(os.path.expanduser(self.USERNAME_SAVE_PATH), 'r') as f:
                contents = f.read()
        except IOError:
            return None
        #global self.api_key
        #global self.bridge_ip
        data = json.loads(contents)
        self.api_key = data['philips-hue']['api_key']
        self.bridge_ip = data['philips-hue']['ip']
        #print(self.api_key,self.bridge_ip)

if __name__ == "__main__":
    import authenticate
    import os
    import time
    import sys
    authenticate = authenticate.authenticate()
    #Search to see if an api key exists, if not, get it.
    if os.path.isfile('./auth.json') == False:
        print("Initial Setup: No Auth file found")
        msg = "Searching for hue Bridges..."
        print msg
        ip = authenticate.search_for_bridge()
        #ip="127.0.0.1"
        if not ip:
            msg = "No Bridges found. Quitting auth file creation."
            print(msg)
            sys.exit()
        elif len(ip) == 1:
            print("Attempting Link: Push Bridge button, then hit the enter key")
            raw_input()
            print("Pairing...")
            try:
                authenticate.authenticate('python module',ip)
            except:
                print("Something went horribly wrong, exiting...")
                sys.exit()
        elif len(ip) > 1:
            print("Attempting Link: Push EVERY Bridge button, then hit the enter key all within 30 seconds")
            raw_input()
            for each_ip in ip:
                #print each_ip
                print("Pairing... with " + str(each_ip))
                try:
                    authenticate.authenticate('python module',each_ip)
                except:
                    print("Something went horribly wrong when pairing with "+str(each_ip)+", exiting...")
                    sys.exit()
    #After a credential file exists
    authenticate.load_creds()
    api_key = authenticate.api_key
    bridge_ip = authenticate.bridge_ip
    api_url = 'http://%s/api/%s' % (bridge_ip,api_key)
    print("Link Established! Full key: \n"+str(api_url))
    print("Authorization file saved as: ./auth.json")
