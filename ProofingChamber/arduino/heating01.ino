
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
unsigned long cycleTime = 10000;
unsigned long heatingTime;

void pulse(int dur){
  digitalWrite(1, HIGH);  
  delay(dur*80);
  digitalWrite(1, LOW);  
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

void heat(unsigned long dur){
  digitalWrite(4, HIGH);
  delay(dur);
  digitalWrite(4, LOW);
}

void setup(){
  heatingTime = cycleTime/6.0; 
  integralFactor = cycleTime * 0.025;
  pinMode(1, OUTPUT);
  pinMode(4, OUTPUT);
  sensors.begin();
  sensors.getAddress(sensorDeviceAddress, 0);
  sensors.setResolution(sensorDeviceAddress, SENSOR_RESOLUTION);
}


void loop(){
  debugOut(2);
  sensors.requestTemperatures();  

  float currentTemp = sensors.getTempCByIndex(SENSOR_INDEX);    
  float error = targetTemp - currentTemp; 
  float addit =  integralFactor * error;
  heatingTime = heatingTime + addit;  

  if (heatingTime < 0.0){
    heatingTime = 0.0;
  }
  else if(heatingTime > cycleTime){
    heatingTime = cycleTime;    
  }  
  
  if(heatingTime > 0){
    //debugOut(heatingTime/1000.0);
    heat(heatingTime);
  }
  debugOut(3);
  delay(cycleTime - heatingTime);
}
