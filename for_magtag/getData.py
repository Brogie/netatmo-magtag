from secrets import secrets
from station import stationId
import time
import adafruit_requests
import ssl
import wifi
import socketpool

def connect(tries = 10):
    tries = 10
    for i in range(tries):
        try:
            print('Connecting Wifi')
            wifi.radio.connect(secrets["ssid"], secrets["password"])
            pool = socketpool.SocketPool(wifi.radio)
            requests = adafruit_requests.Session(pool, ssl.create_default_context())
            print('Connected')
        except:
            if i < tries - 1: # i is zero indexed
                print('[Connection failure] tries remaining ', tries)
                tries -= 1
                time.sleep(10)
                continue
            else:
                raise
        break
    return requests
    

def get_access_token(requests):
    URL = 'https://api.netatmo.com/oauth2/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'client_id' : secrets['client_id'],
        'client_secret' : secrets['client_secret'],
        'grant_type' : 'password',
        'username' : secrets['netatmo_username'],
        'password' : secrets['netatmo_password'],
        'scope' : 'read_station',
    }

    resp = requests.post(URL, headers=headers, data = data)
    json_data = resp.json()

    return json_data['access_token']


def get_station_data(access_token, requests):
    URL = 'https://api.netatmo.com/api/getstationsdata?device_id='+ stationId + '&get_favorites=false'
    headers = {
        'Authorization' : "Bearer " + access_token
    }

    resp = requests.get(URL, headers=headers)
    json_data = resp.json()
    
    return json_data

def get_graph_data_for_module(module, dataType, unix_time, access_token, requests):
    URL = 'https://api.netatmo.com/api/getmeasure?device_id='+ stationId + '&module_id=' + module + '&scale=30min&type=' + dataType + '&date_begin=' + str(unix_time - 86400) + '&limit=48&real_time=false&optimize=true'
    headers = {
        'Authorization' : "Bearer " + access_token
    }

    resp = requests.get(URL, headers=headers)
    json_data = resp.json()

    min = 10000
    max = -10000
    flat_list = []

    for i in range(len(json_data['body'])):
        for item in json_data['body'][i]['value']:
            if item[0] < min:
                min = item[0]
            elif item[0] > max:
                max = item[0]
            flat_list.append(item[0])

    return flat_list, min, max

def extract_dashboard_data(stationData):
    extractedDashboards = {}
    extractedDashboards[stationData['body']['devices'][0]['_id']] = stationData['body']['devices'][0]['dashboard_data']

    for i in range(len(stationData['body']['devices'][0]['modules'])):
        extractedDashboards[stationData['body']['devices'][0]['modules'][i]['_id']] = stationData['body']['devices'][0]['modules'][i]['dashboard_data']


    return extractedDashboards
