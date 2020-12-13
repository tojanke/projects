#!/usr/bin/python3
# -*- coding: utf-8 -*-
import time, sys, RPi.GPIO as GPIO
from RPLCD.gpio import CharLCD
from keypad import keypad
 
GPIO.setwarnings(False)

lcd = CharLCD(pin_rs=26, pin_e=19, pins_data=[13, 6, 5, 11],numbering_mode=GPIO.BCM,cols=16, rows=2)
lcd.cursor_mode = 'hide'

kp = keypad(columnCount = 4)

heatingPin=17

GPIO.setmode(GPIO.BCM)
GPIO.setup(heatingPin, GPIO.OUT)

sensor = '/sys/bus/w1/devices/28-011453efb2aa/w1_slave'
targetTemp = float(26.0)
integralFactor = float(0.8)
cycleTime = float(10)
skip = False

def initLCD():
    lcd = CharLCD(pin_rs=26, pin_e=19, pins_data=[13, 6, 5, 11],numbering_mode=GPIO.BCM,cols=16, rows=2)
    lcd.cursor_mode = 'hide'

def setLCD(str1, str2=""):
    lcd.clear()
    lcd.write_string(str1[:16])
    lcd.cursor_pos = (1,0)
    lcd.write_string(str2[:16])
    lcd.cursor_mode = 'hide'

def changeTargetPressed():
    global targetTemp
    setLCD("New Target:")    
    newTargetStr = ""
    digit = kp.getKey()
    while digit != "#" and len(newTargetStr)<15:
        print("L")
        if digit in [1,2,3,4,5,6,7,8,9,0]:
            newTargetStr = newTargetStr + str(digit)
            setLCD("New Target:", newTargetStr)
        elif digit == "*":            
            newTargetStr += '.'
            setLCD("New Target:", newTargetStr)
        elif digit=="D":
            if len(newTargetStr)>0:
              newTargetStr = newTargetStr[:len(newTargetStr)-1]              
              setLCD("New Target:", newTargetStr)
        while kp.getKey()!=None:            
            time.sleep(0)
        while kp.getKey()==None:            
            time.sleep(0)
        digit = kp.getKey()
    try:
        if(float(newTargetStr)>0.0):
            targetTemp = float(newTargetStr)
    except ValueError:
        print(newTargetStr)

def changeCyclePressed():
    global cycleTime
    setLCD("New Cycle:")    
    newCycleStr = ""
    digit = kp.getKey()
    while digit != "#" and len(newCycleStr)<15:
        print("L")
        if digit in [1,2,3,4,5,6,7,8,9,0]:
            newCycleStr = newCycleStr + str(digit)
            setLCD("New Cycle:", newCycleStr)
        elif digit == "*":            
            newCycleStr += '.'
            setLCD("New Cycle:", newCycleStr)
        elif digit=="D":
            if len(newCycleStr)>0:
              newCycleStr = newCycleStr[:len(newCycleStr)-1]              
              setLCD("New Cycle:", newCycleStr)
        while kp.getKey()!=None:            
            time.sleep(0)
        while kp.getKey()==None:            
            time.sleep(0)
        digit = kp.getKey()
    try:
        if(float(newCycleStr)>0.0):
            cycleTime = float(newCycleStr)
    except ValueError:
        print(newCycleStr)
    

def overridePressed():
    GPIO.output(heatingPin, False)
    setLCD("Manual Mode  OFF","A:On B:Off #:Esc")
    digit = kp.getKey()
    while digit != "#":
        if digit=="A":
            GPIO.output(heatingPin, True)
            setLCD("Manual Mode   ON","A:On B:Off #:Esc")
        elif digit=="B":
            setLCD("Manual Mode  OFF","A:On B:Off #:Esc")
            GPIO.output(heatingPin, False)
        while kp.getKey()!=None:            
            time.sleep(0)
        while kp.getKey()==None:            
            time.sleep(0)
        digit = kp.getKey()
    GPIO.output(heatingPin, False)

def exitPressed():
    setLCD("Exit?","A:Yes B:No #:Esc")
    digit = kp.getKey()
    cont = True
    while digit != "#" and cont:
        
        if digit=="A":
            lcd.clear()
            sys.exit()
        elif digit=="B":
            cont = False
        while kp.getKey()!=None:            
            time.sleep(0)
        while kp.getKey()==None:            
            time.sleep(0)
        digit = kp.getKey()


def readHeatingTime() :
    with open("/code/heating.temp", "r") as heatingFile: 
        return float(heatingFile.read())    
    
def writeHeatingTime(heating) :
    with open("/code/heating.temp", "w") as heatingFile: 
        heatingFile.write(str(heating))    

def updateDisplay(temp, heating):
    setLCD("M:{:5.2f} T:{:5.2f}".format(temp, targetTemp), "H:{:4.1f}s C:{:4.1f}s".format(heating, cycleTime))

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

def waitForInput(waitTime):
    global skip
    stopTime = time.time() + waitTime
    while time.time() < stopTime and not skip:
        digit = kp.getKey()
        if digit=="A":
            changeTargetPressed()
            skip = True
            setLCD("...")
        elif digit=="B":            
            changeCyclePressed()
            skip = True
            setLCD("...")
        elif digit=="C":
            overridePressed()        
            skip = True
            setLCD("...")
        elif digit=="D":
            exitPressed()            
            setLCD("...")
        elif digit=="*":
            initLCD()
            skip = True
            setLCD("...")

try:
    while True :
        skip = False
        currentTemp = float(readTempLines(sensor))
        error = targetTemp - currentTemp
        heatingTime = readHeatingTime()
        heatingTime = heatingTime + (integralFactor * error)
        if heatingTime < 0 :
            heatingTime = 0
        if heatingTime > cycleTime :
            heatingTime = cycleTime
        coolingTime = cycleTime - heatingTime
        writeHeatingTime(heatingTime)        
        updateDisplay(currentTemp, heatingTime)
        if heatingTime > 0 :
            GPIO.output(heatingPin, True)            
            waitForInput(heatingTime)            
        if coolingTime > 0 :
            GPIO.output(heatingPin, False)            
            waitForInput(coolingTime)
except KeyboardInterrupt:    
    print('Temperaturmessung wird beendet')
except Exception as e:
    print(str(e))
    sys.exit(1)
finally:
    GPIO.cleanup()
    sys.exit(0)
