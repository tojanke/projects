#include <Adafruit_NeoPixel.h>

// set to pin connected to data input of WS8212 (NeoPixel) strip
#define PIN         0

// number of LEDs (NeoPixels) in your strip
// (please note that you need 3 bytes of RAM available for each pixel)
#define NUMPIXELS   24

#define BRIGHTNESS  255

#define BLINKYELLOW 40

// decrease to speed up, increase to slow down (it's not a delay actually)
int dly = 150;
#define DEBOUNCE 50

Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);




int previousState = LOW;
int buttonState = 0; //this variable tracks the state of the button, low if not pressed, high if pressed
int state = 0;
int mode = 0;
 
long lastDebounceTime = 0;  // the last time the output pin was toggled

unsigned long timePressed=0;

void reset(){
   for(int s = 0; s < 24; s++){
    
    strip.setPixelColor(s,0, 0, 0);
    
    
  }
  
  strip.show();
  noTone(4);
}

void switchL1(){
   reset();
      if(mode==0){
        state = (state + 1)%4;      
      }      
      else if(mode==1){
        state = (state + 1)%5; 
      }
      else {
        state = (state + 1)%3;        
      }
}

void switchL2(){
  reset();
  mode=(mode + 1)%4;
  state=0;
}

void getButton(){
   unsigned long currentS = millis();
  //sample the state of the button - is it pressed or not?
  buttonState = digitalRead(2);
 
  //filter out any noise by setting a time buffer
  if ( (currentS - lastDebounceTime) > DEBOUNCE) {   
    if(buttonState==HIGH && previousState==LOW){
      timePressed = currentS;
      previousState = HIGH;
    }
    else if(buttonState==LOW && previousState==HIGH){
      unsigned long interval = currentS - timePressed;
      previousState = LOW;
      timePressed=0;
      if(interval > 1000){
        switchL2();
      }
      else {
        switchL1();
      }
    }
   
      lastDebounceTime = millis(); //set the current time 
  }//close if(time buffer)
}



int waitDly=500;

void wait(){
  strip.setPixelColor(3-mode,0, BLINKYELLOW, 0);
  strip.show();
}




int index = 0;
int leftSiren1[] =  {1,1,0,0,1,1,0,0};
int rightSiren1[] = {0,0,1,1,0,0,1,1 };
int leftSiren2[] =  {1,0,1,0,2,0,2,0};
int rightSiren2[] = {2,0,2,0,1,0,1,0 };

int horn1[]      = {440,585};
int horn2[]      = {466,622};

int dly1 = 150;
int dly2 = 100;

unsigned long previousMillis = 0; 


int blinkDly=150;
int blinkPos=1;

void leftBlinker(){
int pixels[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};

  for(int blk = 0; blk < blinkPos; blk++){
    pixels[blk]=1;
    pixels[7-blk]=1;
    pixels[19-blk]=1;
  }  

  for(int s = 0; s < 24; s++){
    if(pixels[s]==0){
      strip.setPixelColor(s,0, 0, 0);
    }
    else {
     strip.setPixelColor(s,BRIGHTNESS, BLINKYELLOW, 0);
    }    
  }  
  strip.show();
  blinkPos = (blinkPos + 1)%5;
}

void rightBlinker(){

  int pixels[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
  
  for(int blk = 0; blk < blinkPos; blk++){
    pixels[8+blk]=1;
    pixels[15-blk]=1;
    pixels[20+blk]=1;    
  }
  
 for(int s = 0; s < 24; s++){
    if(pixels[s]==0){
      strip.setPixelColor(s,0, 0, 0);
    }
    else {
     strip.setPixelColor(s,BRIGHTNESS, BLINKYELLOW, 0);
    }
    
  }
  
  strip.show();
  blinkPos = (blinkPos + 1)%5;
}

int warnIndex = 0;

void warnBlinker(){

  if(warnIndex==0 || warnIndex==2){
    tone(4,1000);
  }
  else {
    noTone(4);
  }

  if(warnIndex%2==0){ 
 for(int s = 0; s < 24; s++){
     strip.setPixelColor(s,BRIGHTNESS, BLINKYELLOW, 0);    
  }
  }
  else {
    
 for(int s = 0; s < 24; s++){
     strip.setPixelColor(s,0, 0, 0);    
  }
  }
  strip.show();
warnIndex = (warnIndex + 1) %8;
}


void siren(int leftS[], int rightS[]){
  int redL = 0;
  int redR = 0;
  int blueL = 0;
  int blueR = 0;  
  
  if(leftS[index]==0){
      blueL = 0;
      redL = 0;
    }
    else if(leftS[index]==1){
      blueL = BRIGHTNESS;
      redL = 0;
    }
    else if(leftS[index]==2) {
      blueL = 0;
      redL = BRIGHTNESS;
    } 

    if(rightS[index]==0){
      blueR = 0;
      redR = 0;
    }
    else if(rightS[index]==1){
      blueR = BRIGHTNESS;
      redR = 0;
    }
    else if(rightS[index]==2) {
      blueR = 0;
      redR = BRIGHTNESS;
    }
  
    for(int i=0; i<24; i++){
      if(i<8){
        strip.setPixelColor(i,redL, 0, blueL);        
      }
      else if(i<16){
        strip.setPixelColor(i,redR, 0, blueR);  
      }
      else if(i < 20){
        strip.setPixelColor(i,redL, 0, blueL);  
      }
      else {
        strip.setPixelColor(i,redR, 0, blueR);  
      }
      
    }   
  
    strip.show();
    index = (index + 1)%8;
  
}

void siren(int leftS[], int rightS[], int h[]){
  int redL = 0;
  int redR = 0;
  int blueL = 0;
  int blueR = 0;
  
  if(index == 0){
    tone(4,h[0]);  
  }
  else if(index == 4){
    tone(4,h[1]);  
  }
  if(leftS[index]==0){
      blueL = 0;
      redL = 0;
    }
    else if(leftS[index]==1){
      blueL = BRIGHTNESS;
      redL = 0;
    }
    else if(leftS[index]==2) {
      blueL = 0;
      redL = BRIGHTNESS;
    } 

    if(rightS[index]==0){
      blueR = 0;
      redR = 0;
    }
    else if(rightS[index]==1){
      blueR = BRIGHTNESS;
      redR = 0;
    }
    else if(rightS[index]==2) {
      blueR = 0;
      redR = BRIGHTNESS;
    }
  
    for(int i=0; i<8; i++){
      strip.setPixelColor(i,redL, 0, blueL);
    }
    for(int i=8; i<16; i++){
      strip.setPixelColor(i,redR, 0, blueR);
    } 
    for(int i=16; i<20; i++){
      strip.setPixelColor(i,redL, 0, blueL);
   }
    for(int i=20; i<24; i++){
      strip.setPixelColor(i,redR, 0, blueR);
    }
  
    strip.show();
    index = (index + 1)%8;
  
}

int lightDly = 500;

void headLight(){
  for(int i=0; i<16; i++){
      strip.setPixelColor(i,BRIGHTNESS, BRIGHTNESS, BRIGHTNESS);
    }
  for(int i=16; i<24; i++){
      strip.setPixelColor(i,BRIGHTNESS, 0, 0);
  }
  strip.show();
}

int strobeDly=30;
int strobeOn = 0;
 
void strobeLight(){
  if(strobeOn==0){
    for(int i=0; i<24; i++){
      strip.setPixelColor(i,0, 0, 0);
    }
    strobeOn=1;
  }
  else {
for(int i=0; i<24; i++){
      strip.setPixelColor(i,BRIGHTNESS, BRIGHTNESS, BRIGHTNESS);
    }
    strobeOn=0;
  }
strip.show();
}


int rbColors[8][3]={
{0,0,255},
{0,255,0},
{255,0,0},
{0,255,255},
{255,255,0},
{255,0,255},
{255,255,255},
{255,127,0}
};

int rbState[]={0,4,2,6,1,7,3,5,0,4,2,6,1,7,3,5,0,4,2,6,1,7,3,5};
int rb1Dly=200;

void rainbow1(){
  for(int l = 0; l < 24; l++){
    strip.setPixelColor(l, rbColors[rbState[l]][0], rbColors[rbState[l]][1], rbColors[rbState[l]][2]);
    rbState[l]=(rbState[l]+1)%8;
  }
  strip.show();
}


int rb2Dly=200;

void rainbow2(){
  for(int e = 0; e < 6; e++){
    for(int l = e*4; l < (e+1)*4; l++){
    strip.setPixelColor(l, rbColors[rbState[e]][0], rbColors[rbState[e]][1], rbColors[rbState[e]][2]);
    
  }
    rbState[e]=(rbState[e]+1)%8;
  }
  
  strip.show();
}


void setup() {
  // initialize LED strip
  strip.begin();
  strip.show();
  pinMode(0, OUTPUT);
  pinMode(2, INPUT);
  pinMode(4, OUTPUT); 
}


int counter = 0;

void loop() {
  getButton();
  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= dly) {
    previousMillis = currentMillis;
    if(mode==0){
      if(state ==1){
        dly = blinkDly;
        leftBlinker();
      }
      else if(state == 2){
        dly = blinkDly;
        rightBlinker();
      }
      else if(state == 3){
        dly = blinkDly;
        warnBlinker();
      }
      else {
        dly = waitDly;
        wait();
      }
    }
    else if(mode==1) {
      if(state==1){
        dly = dly1;
        siren(leftSiren1, rightSiren1);
       }
      else if(state==2){
        dly = dly1;
        siren(leftSiren1, rightSiren1, horn1);
      }
      else if(state==3){
        dly = dly2;
        siren(leftSiren2, rightSiren2);
      }
      else if(state==4){
        dly = dly2;
        siren(leftSiren2, rightSiren2, horn2);
      }
      else {
         dly = waitDly;
        wait();
      }
    } 
    else if(mode==2) {
      if(state==1){
        dly=lightDly;
        headLight();
      }
      else if(state==2){
        dly=strobeDly;
        strobeLight();
      }
      else {
         dly = waitDly;
          wait();
      }
    }
    else {
      if(state==1){
        dly=rb1Dly;
        rainbow1();
      }
      else if(state==2){
        dly=rb2Dly;
        rainbow2();
      }
      else {
         dly = waitDly;
          wait();
      }
    }
  }
}
