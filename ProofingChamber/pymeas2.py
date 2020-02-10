#!/usr/bin/python3
# -*- coding: utf-8 -*-
import time, sys, RPi.GPIO as GPIO

sensor = '/sys/bus/w1/devices/28-011453efb2aa/w1_slave'

def readTempSensor(sensorName) :    
    f = open(sensorName, 'r')
    lines = f.readlines()
    f.close()
    return lines

def readTempLines(sensorName) :
    lines = readTempSensor(sensorName)    
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = readTempSensor(sensorName)
    temperaturStr = lines[1].find('t=')    
    if temperaturStr != -1 :
        tempData = lines[1][temperaturStr+2:]
        tempCelsius = float(tempData) / 1000.0        
        # Rückgabe als Array - [0] tempCelsius => Celsius...
        return tempCelsius

currentTemp = float(readTempLines(sensor))
print("temp temperature=" + str(currentTemp) + " " + str(time.time_ns()) + "\n")
sys.exit(0)