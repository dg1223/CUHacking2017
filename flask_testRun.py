#import indicoio
import time
import os
import json
import urllib2
import flask
from natsort import natsorted
from pandas import DataFrame
#print "Access-Control-Allow-Origin: *"
##indicoio.config.api_key = '8a1ce26c054d3985644f63074b015980'

from flask import Flask
app = Flask(__name__)

@app.route("/data/")
def callBackend():
    defective = detectDefectiveDevices(allInfo)
    #info = fetch_and_extract(rows, allInfo)
    #completeStr = info[0]
    
    #for i in range(len(info)):
    #    completeStr = completeStr + info[i]
    resp = flask.jsonify({"text":defective})
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

destination = "C:/Users/Shamir Alavi/Desktop/CUHacking2017/Codes/"
name = 'rawData'
fileformat = '.csv'
mainURL = 'http://cuhackathon-challenge.martellotech.com/devices/'
rows = ["description", "name", "alarms" , "connected", "dhcpClients", "volume", "source", "channel",
            "firmware", "queue", "digits", "inUse", "setTemperature", "actualTemperature", "setting", "alarm_status",
            "lastSeen", "uptime", "is_on", "is_connected", "paired_device", "wifi_strength", "paperJam", "inkStock",
            "battery", "voiceQuality", "bagelMode", "isToasting", "oodl", "patch", "qa_passed", "is_streaming", "media_type",
            "paperStock", "motionDetected", "bytesReceived", "bytesSent", "macAddress", "packetLossRate", "packetsLost"] # "alarms_description", "alarms_severity", "alarms_title"
allInfo = []
allInfo.append(rows)

def detectDefectiveDevices(listOfDevices):
    packetLost = []
    packetLossThreshold = 50000
    for i in range(len(listOfDevices)):
        packetLost.append(listOfDevices[i][-1])
    
    checkDevice = []
    for i in range(len(packetLost)):
        if (packetLost[i] > packetLossThreshold):
            checkDevice.append(listOfDevices[i][0])
    
    checkDevStr = ''
    for i in range(len(checkDevice) - 1):
        index = i+1
        checkDevStr = checkDevStr + str(checkDevice[index]) + ' || '
        
    return checkDevStr
    
def fetchDeviceList(url):    
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    the_page = response.read()
    jsonString = json.loads(the_page)
    
    return jsonString
    
def fetchDeviceData(jsonList, url, storage):    
    for i in range(len(jsonList)):
        deviceURL = url + str(i) + '/'
        storage.append(fetchDeviceList(deviceURL))

def fetch_and_extract(headers, storage):
    deviceListObject = fetchDeviceList(mainURL)
    sortedList = natsorted(deviceListObject.values())
    rawData = []
    
    i = 0
    while(i < 1):
        fetchDeviceData(sortedList, mainURL, rawData)
        i += 1 
    
    # Write CSV Header, If you dont need that, remove this line
    
    
    information = ["NA"] * len(headers)
    
    for device in range(len(rawData)):
        for i in range(len(rawData[device].keys())):
            key = rawData[device].keys()[i]
            if (key != 'interfaces'):
                try:
                    information[rows.index(key)] = rawData[device][key]
                except IndexError:
                    pass
            else:
                try:
                    for j in range(5):
                        index = j - 5
                        information[index] = rawData[device]['interfaces'][0][rows[index]]
                except IndexError:
                    pass
    
        storage.append(information)
        #callableInfo = information
        information = ["NA"] * len(rows)
        
    #return callableInfo
    
fetch_and_extract(rows, allInfo)

#if __name__ == "__main__":
#    app.run(debug = True)

#for i in range(250):
#    fetch_and_extract(rows, allInfo)
#    time.sleep(60)

    
#pandasData = DataFrame(allInfo)
#pandasData.to_csv(destination + name + fileformat, header = False, index = False)
