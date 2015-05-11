#!/usr/bin/python

import datetime
import time
import requests
import xml.etree.ElementTree as ET
from time import sleep

#Credentials for accessing stretch
username = 'stretch'
password = 'ppwkcdzz' #Change to corresponding value
url = 'http://<stretch-ip>/minirest/appliances'

#Post to local database
urlphp = 'http://<server-ip>/insert2db.php'

#Post to visualize with Emoncms
api_local = '876e41a0395c055ceff7e0a259a092ff' #Change to corresponding value
emoncms_local_url  = 'http://<server-ip>/emoncms/input/post.json?'


def checkIfNewValue(appliance, appliances_list_last):
    new_values = True
    #Check if the appliance was read in the last reading
    if (appliance[1].get('name') in appliances_list_last):
        if (appliance[1].get('last_known_measurement') == appliances_list_last.get(appliance[1].get('name')).get('last_known_measurement')):
            new_values = False
            print appliance[1].get('name'), 'SAME VALUE AS PREVIOUS ONE', appliance[1].get('last_known_measurement')
    if new_values:
        print appliance
        
    return new_values

def postToLocalDB(appliance):    
    print 'Posting to local db...'
    payload = {'name': appliance[1].get('name'), 'timestamp': appliance[1].get('last_known_measurement'), 'power': appliance[1].get('current_power_usage')}
    r1 = requests.post(urlphp, data=payload)
    print r1 
    
def postToEmoncms(appliance):    
    print 'Posting to local emoncms...'                    
    epoch = int(time.mktime(time.strptime(appliance[1].get('last_known_measurement'), '%Y-%m-%dT%H:%M:%S+01:00')))
    payload2 = 'time=' + str(epoch) + "&node=" + appliance[1].get('name') + "&csv=" + appliance[1].get('current_power_usage') + "&apikey=" + api_local
    r2 = requests.post(emoncms_local_url + payload2)
    print r2.url

def requestNewDataFromStretch(x):
    i = datetime.datetime.now()
    r = requests.get(url, auth=(username, password), stream=True)
    i2 = datetime.datetime.now()
    
    print x, i.isoformat(), str((i2-i))
    return r
    
def buildAppliancesList(r):
    root = ET.fromstring(r.content)
    appliances = list(root)
    appliances_list = {}
        
    for appliance in appliances:
        appliance_info = {}
        appliance_info['name'] = appliance[0].text
        appliance_info['last_seen_date'] = appliance[4].text
        appliance_info['last_known_measurement'] = appliance[8].text
        appliance_info['power_state'] = appliance[5].text
        appliance_info['current_power_usage'] = appliance[6].text
        appliances_list[appliance[0].text] = appliance_info
        
    return appliances_list

def main():
    appliances_list_last = []    
    x = 0
    while True:
        try:
            x = x + 1
            r = requestNewDataFromStretch(x)
            appliances_list = buildAppliancesList(r)
            
            for appliance in appliances_list.items():
                new_values = checkIfNewValue(appliance, appliances_list_last)            
                if new_values:
                    postToLocalDB(appliance)
                    postToEmoncms(appliance)
    
            appliances_list_last = appliances_list
            print '========================================================='
            sleep(5)
        except Exception as e:
            print "Parse error", e

if __name__ == '__main__':
    main()
