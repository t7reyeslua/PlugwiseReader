#!/usr/bin/python

import datetime
import time
import requests
import xml.etree.ElementTree as ET
from time import sleep
import pprint as pp

#Credentials for accessing stretch
username = 'smile'
password = 'pqszkhpp' #Change to corresponding value
url = 'http://<smile-ip>/core/modules'

#Post to local database
urlphp = 'http://<server-ip>/insert2db_smile.php'

#Post to visualize with Emoncms
api_local = '876e41a0395c055ceff7e0a259a092ff' #Change to corresponding value
emoncms_local_url  = 'http://<server-ip>/emoncms/input/post.json?'


def postToLocalDB(name, timestamp, power, directionality, unit, tariff_indicator, interval, service_type):    
    print 'Posting to local db...'
    payload = {
    'name': name, 
    'timestamp': timestamp, 
    'power': power, 
    'directionality': directionality, 
    'unit': unit, 
    'tariff_indicator': tariff_indicator, 
    'interval': interval,
    'service_type':service_type}
    r1 = requests.post(urlphp, data=payload)
    print r1 
    
def postToEmoncms(name, epoch, power):    
    print 'Posting to local emoncms...'                    
    payload2 = 'time=' + str(epoch) + "&node=" + name + "&csv=" + power + "&apikey=" + api_local
    r2 = requests.post(emoncms_local_url + payload2)
    print r2.url

def requestNewDataFromSmile(x):
    i = datetime.datetime.now()
    r = requests.get(url, auth=(username, password), stream=True)
    i2 = datetime.datetime.now()
    
    print x, i.isoformat(), str((i2-i))
    return r

def parseService(service, service_type):
    results = {}
    for measurement in service:
        attr = measurement.attrib
        attr['power'] = measurement.text
        
        key = attr['directionality']
        if service_type in ['interval', 'cumulative']:        
            key += '/' + attr['tariff_indicator']
            
        results[key] = attr
    return results

def compare_dictionaries(d1, d2):
    unmatched_item = set(d1.items()) ^ set(d2.items())
    n = len(unmatched_item)
    
    if n == 0:
        return False
    else:
        return True
    
def checkIfNewResults(readings, new_readings):
    results = {}    
    for service_type in readings:
        results[service_type] = {}
        for measurement in readings[service_type]:
            changed = compare_dictionaries(readings[service_type][measurement], new_readings[service_type][measurement])
            results[service_type][measurement] = (changed, new_readings[service_type][measurement])
    return results

def findMeterIndex(services, service_type):    
    index = 0
    for i in range(0,3):
        if service_type in services[i].tag:
            index = i
    return index
    
def parseXML(r):
    root = ET.fromstring(r.content)
    services = root[0][7]      
    
    index_interval   = findMeterIndex(services, 'interval')
    index_cumulative = findMeterIndex(services, 'cumulative')
    index_point      = findMeterIndex(services, 'point')
    
    interval   = parseService(list(services[index_interval]), 'interval')
    cumulative = parseService(list(services[index_cumulative]), 'cumulative') 
    point      = parseService(list(services[index_point]), 'point')
    
    readings   = {'cumulative': cumulative, 'interval': interval, 'point': point}
        
    return readings   

def save_to_db(service_type, values):     
    log_date = values['log_date']
    epoch = int(time.mktime(time.strptime(log_date, '%Y-%m-%dT%H:%M:%S+02:00')))
    unit = values['unit']
    directionality = values['directionality']
    power = values['power']
    
    tariff_indicator = ''
    interval  = ''
    if service_type is not 'point':
        tariff_indicator = values['tariff_indicator']
        if service_type is 'interval':
            interval = values['interval']
                         
    postToLocalDB(username, log_date , power, directionality, unit, tariff_indicator, interval, service_type)
    if service_type is 'point':
        if 'consumed' in directionality:
            postToEmoncms(username, epoch    , power)

def save_readings(readings):
    
    for service_type in readings:
        for measurement in readings[service_type]:
            changed = readings[service_type][measurement][0]
            if changed:
                print service_type, '===================='
                pp.pprint(readings[service_type][measurement][1])
                save_to_db(service_type, readings[service_type][measurement][1])

def main():
    print ('Starting script to read Smile P1...')
    x = 0
    readings = {}
    while True:
        try:
            x = x + 1
            r = requestNewDataFromSmile(x)
            
            new_readings = parseXML(r)
            
            changed_readings = checkIfNewResults(readings, new_readings)
            save_readings(changed_readings)
            print '========================================================='
            
            readings = new_readings
            sleep(5)
        except Exception as e:
            print "Parse error", e


if __name__ == '__main__':
    main()
