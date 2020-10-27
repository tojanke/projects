#include <OneWire.h>
#include <DigiUSB.h>
#define DS18S20_ID 0x10
#define DS18B20_ID 0x28

OneWire ds(3);

byte data[12];
byte addr[8]; 

int relay = 4;


boolean readTemperature(){  
  if (!ds.search(addr)) {
    ds.reset_search();
    return false;
  }
  if (OneWire::crc8( addr, 7) != addr[7]) {
    return false;
  }
  if (addr[0] != DS18S20_ID && addr[0] != DS18B20_ID) {
    return false;
  }
 
  ds.reset();
  ds.select(addr);
  ds.write(0x44, 1); 
}
  
int getTemperature(){
  readTemperature();
  DigiUSB.delay(1000);
  byte i;  
  byte present = 0;
  present = ds.reset();
  ds.select(addr);
  // Issue Read scratchpad command
  ds.write(0xBE);
  // Receive 9 bytes
  for ( i = 0; i < 9; i++) {
    data[i] = ds.read();
  }
  // Calculate temperature value
  return ((( (data[1] << 8) + data[0] )*0.0625)*1.8)+32;
}


 
void setup ()
{
  pinMode (relay, OUTPUT); // Der Pin wird als Ausgang deklariert
}
 
void loop ()
{
  
  int temp = getTemperature();

  for(int i=0;i<temp;i++){
    digitalWrite (relay, HIGH); // "NO" ist nun kurzgeschlossen;
    delay (500);
    digitalWrite (relay, LOW); // "NC" ist nun kurzgeschlossen;
    delay (500);
  }
  
  delay(5000);
  
}
