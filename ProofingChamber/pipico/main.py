from machine import Pin
from time import sleep, ticks_ms, ticks_diff
from gpio_lcd import GpioLcd
from onewire import OneWire
from ds18x20 import DS18X20

keys = [['1', '2', '3', 'A'], ['4', '5', '6', 'B'], ['7', '8', '9', 'C'], ['*', '0', '#', 'D']]

rows = [2,3,4,5]
cols = [6,7,8,9]

row_pins = [Pin(pin_name, mode=Pin.OUT) for pin_name in rows]
col_pins = [Pin(pin_name, mode=Pin.IN, pull=Pin.PULL_DOWN) for pin_name in cols]

heating_pin=Pin(1, mode=Pin.OUT)

temp_pin=Pin(28)
temp_sensor = DS18X20(OneWire(temp_pin))
temp_source = None

targetTemp = float(26.0)
integralFactor = float(0.8)
cycleTime = float(40)
heatingTime=float(20)
skip = False

lcd = GpioLcd(rs_pin=Pin(14),
    enable_pin=Pin(15),
    d4_pin=Pin(10),
    d5_pin=Pin(11),
    d6_pin=Pin(12),
    d7_pin=Pin(13),
    num_lines=2, num_columns=16)

def init_keypad():
    for row in range(0,4):
        for col in range(0,4):
            row_pins[row].low()

def scan(row, col):
    row_pins[row].high()
    key = col_pins[col].value()
    row_pins[row].low()

    return key


def getKeyPressed():    
    for row in range(4):
        for col in range(4):
            key = scan(row, col)
            if key == 1:
                return keys[row][col]
    return ''

def init_lcd():
    lcd.clear()    
    lcd.blink_cursor_off()    
    lcd.backlight_on()
    
def init_sensor():
    global temp_source
    sensors = temp_sensor.scan()
    if len(sensors)!=1:
        exit(1)
    temp_source = sensors[0]
    
def get_temp():
    temp_sensor.convert_temp()
    sleep(.8)
    return temp_sensor.read_temp(temp_source)

def setLCD(str1, str2=""):
    init_lcd()
    lcd.move_to(0,0)
    lcd.putstr(str1[:16])
    lcd.move_to(0,1)
    lcd.putstr(str2[:16])
    lcd.hide_cursor()
    
def changeTargetPressed():
    global targetTemp
    setLCD("New Target:")    
    newTargetStr = ""
    digit = getKeyPressed()
    while digit != "#" and len(newTargetStr)<15:        
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
        while getKeyPressed()==digit:
            sleep(0)
        while getKeyPressed()==None:            
            sleep(0)
        digit = getKeyPressed()
    try:
        if(float(newTargetStr)>0.0):
            targetTemp = float(newTargetStr)
    except ValueError:
        print(newTargetStr)
        
def changeCyclePressed():
    global cycleTime
    setLCD("New Cycle:")    
    newCycleStr = ""
    digit = getKeyPressed()
    while digit != "#" and len(newCycleStr)<15:        
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
        while getKeyPressed()==digit:            
            time.sleep(0)
        while getKeyPressed()==None:            
            time.sleep(0)
        digit = getKeyPressed()
    try:
        if(float(newCycleStr)>0.0):
            cycleTime = float(newCycleStr)
    except ValueError:
        print(newCycleStr)
    

def overridePressed():    
    setLCD("Manual Mode  OFF","A:On B:Off #:Esc")
    digit = getKeyPressed()
    while digit != "#":
        if digit=="A":
            heating_pin.high()
            setLCD("Manual Mode   ON","A:On B:Off #:Esc")
        elif digit=="B":
            setLCD("Manual Mode  OFF","A:On B:Off #:Esc")
            heating_pin.low()
        while getKeyPressed()==digit:            
            time.sleep(0)
        while getKeyPressed()==None:            
            time.sleep(0)
        digit = getKeyPressed()
    GPIO.output(heatingPin, False)

def exitPressed():
    setLCD("Exit?","A:Yes B:No #:Esc")
    digit = getKeyPressed()
    cont = True
    while digit != "#" and cont:
        
        if digit=="A":
            lcd.clear()
            sys.exit()
        elif digit=="B":
            cont = False
        while getKeyPressed()==digit:            
            time.sleep(0)
        while getKeyPressed()==None:            
            time.sleep(0)
        digit = getKeyPressed()
        
def updateDisplay(temp):
    setLCD("M:{:5.2f} T:{:5.2f}".format(temp, targetTemp), "H:{:4.1f}s C:{:4.1f}s".format(heatingTime, cycleTime))
    
def waitForInput(waitTime):
    global skip
    start = ticks_ms()
    wait_ms = waitTime * 1000    
    while ticks_diff(ticks_ms(), start) < wait_ms and not skip:        
        digit = getKeyPressed()
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
            init_lcd()
            skip = True
            setLCD("...")
    
def init():
    init_keypad()
    init_lcd()
    init_sensor()
    
def loop():
    global heatingTime
    while True:        
        skip = False
        current_temp = get_temp()
        error = targetTemp - current_temp        
        heatingTime = heatingTime + (integralFactor * error)
        if heatingTime < 0 :
            heatingTime = 0
        if heatingTime > cycleTime :
            heatingTime = cycleTime
        coolingTime = cycleTime - heatingTime        
        updateDisplay(current_temp)
        if heatingTime > 0 :
            heating_pin.high()
            waitForInput(heatingTime)
        if coolingTime > 0 :
            heating_pin.low()
            waitForInput(coolingTime)
    
init()
loop()
