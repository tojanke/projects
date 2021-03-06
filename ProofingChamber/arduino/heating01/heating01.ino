
#include <OneWire.h>
#include <DallasTemperature.h>

// Sensor input pin
#define DATA_PIN 3
// How many bits to use for temperature values: 9, 10, 11 or 12
#define SENSOR_RESOLUTION 11
// Index of sensors connected to data pin, default: 0
#define SENSOR_INDEX 0

OneWire oneWire(DATA_PIN);
DallasTemperature sensors(&oneWire);
DeviceAddress sensorDeviceAddress;

float targetTemp = 26.0;
float integralFactor;
long cycleTime = 10000;
long heatingTime;

void pulse(int dur){
  digitalWrite(1, HIGH);  
  delay(dur*80);
  digitalWrite(1, LOW);  
  delay(dur*80);
}

void beep(int dur){  
    tone(2,440);
    delay(dur*80);
    noTone(2);
    delay(dur*80);
}

void debugOut(float data){
  float out = data;
  while(out >= 10){
    pulse(4);
    out = out - 10.0;
  }
  while(out >= 1){
    pulse(2);
    out = out - 1.0;
  }  
}

void beepOut(float data){
  float out = data;
  while(out >= 10){
    beep(3);
    out = out - 10.0;
  }
  while(out >= 1){
    beep(2);
    out = out - 1.0;
  }  
  while(out >= 0.1){
    beep(1);
    out = out - 0.1;
  }  
}

void heat(unsigned long durh, unsigned long durc){
  digitalWrite(4, HIGH);
  delay(durh);
  digitalWrite(4, LOW);
  delay(durc);
}

void checkSensors(){
  delay(1000);
  sensors.requestTemperatures();  
  float currentTemp = sensors.getTempCByIndex(SENSOR_INDEX);    
  if(currentTemp < 10){
    beepOut(0.2);
    delay(1000);
    beepOut(currentTemp);
    delay(2000);
    checkSensors();
  }
  else if(currentTemp > 40){
    beepOut(0.3);
    delay(1000);
    beepOut(currentTemp);
    delay(2000);
    checkSensors();
  }
  else {
    beepOut(0.1);
  }  
}

void setup(){
  beepOut(0.1);
  heatingTime = cycleTime/6.0; 
  integralFactor = cycleTime / 100.0;
  pinMode(1, OUTPUT);
  pinMode(2, OUTPUT);
  pinMode(4, OUTPUT);
  sensors.begin();
  sensors.getAddress(sensorDeviceAddress, 0);
  sensors.setResolution(sensorDeviceAddress, SENSOR_RESOLUTION);  
  checkSensors();
}


void loop(){  
  sensors.requestTemperatures();  

  float currentTemp = sensors.getTempCByIndex(SENSOR_INDEX);    
  float error = targetTemp - currentTemp; 
  float addit =  integralFactor * error;
  
  heatingTime = heatingTime + addit;  

  if(error < -0.5){
    debugOut(1);
  }
  else if(error > -0.5 && error < 0.5){
    debugOut(2);
  }
  else if(error > 0.5){
    debugOut(3);
  }  
  delay(1000);
  debugOut(error< 0 ? -1*error : error);

  if (heatingTime < 0.0){
    heatingTime = 0.0;
  }
  else if(heatingTime > cycleTime){
    heatingTime = cycleTime;    
  }  
  
  if(heatingTime > 0){    
    heat(heatingTime, cycleTime - heatingTime);
  }  
  else {
    delay(cycleTime);
  }
}
