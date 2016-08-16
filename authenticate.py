# authentication code created by adamcharnock (https://github.com/adamcharnock)
# modified by @innocuoussoul
from _socket import gethostname
import json
import os
import requests

USERNAME_SAVE_PATH = 'auth.json'
api_key = ""
bridge_ip = ""
def parse_response(response):
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


def authenticate(app_name, bridge_host, client_name=None):
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
        save_creds(data[0]['success']['username'],bridge_host)


def save_creds(username,ip):
    with open(os.path.expanduser(USERNAME_SAVE_PATH), 'w') as f:
        f.write(json.dumps({
            'philips-hue': {
                'api_key': username,
                'ip':ip,
            }
        }))
    print('Username saved')
def search_for_bridge(timeout=3):
    """Searches for a bridge on the local network and returns the IP if it
    finds one."""
    r = requests.get('http://www.meethue.com/api/nupnp', timeout=timeout)
    bridges = r.json()
    if len(bridges) > 0:
        return bridges[0]['internalipaddress']
    else:
        return None

def load_creds():
    try:
        with open(os.path.expanduser(USERNAME_SAVE_PATH), 'r') as f:
            contents = f.read()
    except IOError:
        return None
    global api_key
    global bridge_ip
    data = json.loads(contents)
    api_key = data['philips-hue']['api_key']
    bridge_ip = data['philips-hue']['ip']
    #print(api_key,bridge_ip)
