#!/usr/bin/env python3

import cgitb, cgi
cgitb.enable()
import lib.parse as parse
import lib.tools as tools
import os

def main(conditionsList, alarmDataDict):
    """Check if the conditions are met in the data provided and return a JSON construction of Trues and Falses alongside their unique condition ID"""
    # Find the time condition which has the earliest start hour
    lowestCondition = None
    for condition in conditionsList:
        if lowestCondition == None or condition['start'] < lowestCondition:
            lowestCondition = condition['start']
    datestamp = tools.unixToDate(float(lowestCondition))
    weather = parse.parseWeather(datestamp.year, datestamp.month, datestamp.day, datestamp.hour, str(alarmDataDict['lat']), str(alarmDataDict['long']))
    statuses = {}
    for weatherDay in weather:
        hourStatus = []
        precipStatus = False
        status = False
        testOffset = 0
        if float(weatherDay['precipIntensity']) != 0 and (weatherDay['precipType'] == 'rain' or weatherDay['precipType'] == 'hail'):
            if float(weatherDay['precipIntensity']) >= 10.16:
                if float(weatherDay['precipProbability']) >= 40/100 - testOffset:
                    status = True
                else:
                    status = False
            elif float(weatherDay['precipIntensity']) >= 2.54:
                if float(weatherDay['precipProbability']) >= 50/100 - testOffset:
                    status = True
                else:
                    status = False
            elif float(weatherDay['precipIntensity']) >= 0.4318:
                if float(weatherDay['precipProbability']) >= 60/100 - testOffset:
                    status = True
                else:
                    status = False
            elif float(weatherDay['precipIntensity']) >= 0.0508:
                if float(weatherDay['precipProbability']) >= 70/100 - testOffset:
                    status = True
                else:
                    status = False
        else:
            status = False
        precipStatus = status
        hourStatus.append(status)
        #####
        status = False
        testOffset = 0
        if float(weatherDay['precipIntensity']) != 0 and (weatherDay['precipType'] == 'snow' or weatherDay['precipType'] == 'sleet'):
            if float(weatherDay['precipIntensity']) >= 10.16:
                if float(weatherDay['precipProbability']) >= 30/100 - testOffset:
                    status = True
                else:
                    status = False
            elif float(weatherDay['precipIntensity']) >= 2.54:
                if float(weatherDay['precipProbability']) >= 40/100 - testOffset:
                    status = True
                else:
                    status = False
            elif float(weatherDay['precipIntensity']) >= 0.4318:
                if float(weatherDay['precipProbability']) >= 50/100 - testOffset:
                    status = True
                else:
                    status = False
            elif float(weatherDay['precipIntensity']) >= 0.0508:
                if float(weatherDay['precipProbability']) >= 60/100 - testOffset:
                    status = True
                else:
                    status = False
        else:
            status = False
        if status == True and precipStatus == False:
            precipStatus = True
        hourStatus.append(status)
        #####
        status = False
        if float(weatherDay['visibility']) <= 2:
            status = True
        else:
            status = False
        hourStatus.append(status)
        #####
        status = False
        if float(weatherDay['windSpeed']) >= 13.4112:
            status = True
        else:
            status = False
        hourStatus.append(status)
        hourStatus.append(precipStatus)
        #statuses[weatherDay['time'].split(' ')[1]] = hourStatus
        statuses[weatherDay['unixtime']] = hourStatus
    #print(statuses)
    returnJSONkey = []
    returnJSONvalue = []
    for condition in conditionsList:
        time = int(condition['start'])
        found = False
        while found == False and time < int(condition['end']):
            #print(time)
            if statuses[str(time)][int(condition['condid']) - 1]:
                found = True
            time += 3600
        returnJSONkey.append(condition['number'])
        returnJSONvalue.append(found)
        returnJSON = tools.jsonConstructor(returnJSONkey,returnJSONvalue,True)
    try:
        return returnJSON
    except:
        return ""


print("Content-Type: application/json;charset=utf-8")
#print("Content-Type: text/html;charset=utf-8")
print()


form = cgi.FieldStorage()
#print(os.environ["REQUEST_URI"])
#conditions, conditionsList = parse.parseURL("www.server.co.uk/?count=2&no1=1&condid1=1&start1=1438178400&end1=1438182000&no2=2&condid2=3&start2=1438178400&end2=1438185600")
conditionsList, alarmDataDict = parse.parseURL(os.environ["REQUEST_URI"])
if conditionsList == None and alarmDataDict == None:
    print()
else:
    json = main(conditionsList, alarmDataDict)
    print(json)
