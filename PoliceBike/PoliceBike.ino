#include <Adafruit_NeoPixel.h>

#define PIN         0
#define NUMPIXELS   24
#define BRIGHTNESS  255
#define BLINKYELLOW 40
Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

unsigned int dly = 150;
#define DEBOUNCE 50
unsigned int previousState = LOW;
unsigned int buttonState = 0;
unsigned long lastDebounceTime = 0;
unsigned long timePressed = 0;
unsigned int state = 0;
unsigned int mode = 0;

void reset() {
  for (unsigned int s = 0; s < 24; s++) {
    strip.setPixelColor(s, 0, 0, 0);
  }
  strip.show();
  noTone(4);
}

void switchL1() {
  reset();
  if (mode == 0) {
    state = (state + 1) % 4;
  }
  else if (mode == 1) {
    state = (state + 1) % 5;
  }
  else {
    state = (state + 1) % 3;
  }
}

void switchL2() {
  reset();
  mode = (mode + 1) % 4;
  state = 0;
}

void getButton() {
  unsigned long currentS = millis();
  buttonState = digitalRead(2);

  if ( (currentS - lastDebounceTime) > DEBOUNCE) {
    if (buttonState == HIGH && previousState == LOW) {
      timePressed = currentS;
      previousState = HIGH;
    }
    else if (buttonState == LOW && previousState == HIGH) {
      unsigned long interval = currentS - timePressed;
      previousState = LOW;
      timePressed = 0;
      if (interval > 1000) {
        switchL2();
      }
      else {
        switchL1();
      }
    }

    lastDebounceTime = millis(); //set the current time
  }
}

unsigned int waitDly = 500;

void wait() {
  strip.setPixelColor(3 - mode, 0, BLINKYELLOW, 0);
  strip.show();
}

unsigned int index = 0;
unsigned int leftSiren1[] =  {1, 1, 0, 0, 1, 1, 0, 0};
unsigned int rightSiren1[] = {0, 0, 1, 1, 0, 0, 1, 1 };
unsigned int leftSiren2[] =  {1, 0, 1, 0, 2, 0, 2, 0};
unsigned int rightSiren2[] = {2, 0, 2, 0, 1, 0, 1, 0 };

unsigned int horn1[]      = {440, 585};
unsigned int horn2[]      = {466, 622};

unsigned int dly1 = 150;
unsigned int dly2 = 100;

unsigned long previousMillis = 0;

unsigned int blinkDly = 150;
unsigned int blinkPos = 1;


void blink(unsigned int pixels[]) {
  for (unsigned int s = 0; s < 24; s++) {
    if (pixels[s] == 0) {
      strip.setPixelColor(s, 0, 0, 0);
    }
    else {
      strip.setPixelColor(s, BRIGHTNESS, BLINKYELLOW, 0);
    }
  }
  strip.show();
}

void leftBlinker() {
  unsigned int pixels[] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};

  for (unsigned int blk = 0; blk < blinkPos; blk++) {
    pixels[blk] = 1;
    pixels[7 - blk] = 1;
    pixels[19 - blk] = 1;
  }

  blink(pixels);


  blinkPos = (blinkPos + 1) % 5;
}

void rightBlinker() {
  unsigned int pixels[] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};

  for (unsigned int blk = 0; blk < blinkPos; blk++) {
    pixels[8 + blk] = 1;
    pixels[15 - blk] = 1;
    pixels[20 + blk] = 1;
  }

  blink(pixels);

  blinkPos = (blinkPos + 1) % 5;
}

unsigned int warnIndex = 0;

void warnBlinker() {
  if (warnIndex == 0 || warnIndex == 2) {
    tone(4, 1000);
  }
  else {
    noTone(4);
  }
  unsigned int r = (warnIndex % 2 == 0) ? BRIGHTNESS : 0;
  unsigned int g = (warnIndex % 2 == 0) ? BLINKYELLOW : 0;

  for (unsigned int s = 0; s < 24; s++) {
    strip.setPixelColor(s, r, g, 0);
  }

  strip.show();
  warnIndex = (warnIndex + 1) % 8;
}


void siren(unsigned int leftS[], unsigned int rightS[]) {
  unsigned int redL = (leftS[index] == 2) ? BRIGHTNESS : 0;
  unsigned int redR = (rightS[index] == 2) ? BRIGHTNESS : 0;
  unsigned int blueL = (leftS[index] == 1) ? BRIGHTNESS : 0;
  unsigned int blueR = (rightS[index] == 1) ? BRIGHTNESS : 0;


  for (unsigned int i = 0; i < 24; i++) {
    if (i < 8) {
      strip.setPixelColor(i, redL, 0, blueL);
    }
    else if (i < 16) {
      strip.setPixelColor(i, redR, 0, blueR);
    }
    else if (i < 20) {
      strip.setPixelColor(i, redL, 0, blueL);
    }
    else {
      strip.setPixelColor(i, redR, 0, blueR);
    }

  }

  strip.show();
  index = (index + 1) % 8;
}

void siren(unsigned int leftS[], unsigned int rightS[], unsigned int h[]) {

  if (index == 0) {
    tone(4, h[0]);
  }
  else if (index == 4) {
    tone(4, h[1]);
  }

  siren(leftS, rightS);
}

unsigned int lightDly = 500;

void headLight() {
  for (unsigned int i = 0; i < 16; i++) {
    strip.setPixelColor(i, BRIGHTNESS, BRIGHTNESS, BRIGHTNESS);
  }
  for (unsigned int i = 16; i < 24; i++) {
    strip.setPixelColor(i, BRIGHTNESS, 0, 0);
  }
  strip.show();
}

unsigned int strobeDly = 30;
unsigned int strobeOn = 0;

void strobeLight() {

  if (strobeOn == 0) {
    for (unsigned int i = 0; i < 24; i++) {
      strip.setPixelColor(i, 0, 0, 0);
    }
    strobeOn = 1;
  }
  else {
    for (unsigned int i = 0; i < 24; i++) {
      strip.setPixelColor(i, BRIGHTNESS, BRIGHTNESS, BRIGHTNESS);
    }
    strobeOn = 0;
  }
  strip.show();
}


int rbColors[8][3] = {
  {0, 0, 255},
  {0, 255, 0},
  {255, 0, 0},
  {0, 255, 255},
  {255, 255, 0},
  {255, 0, 255},
  {255, 255, 255},
  {255, 127, 0}
};

unsigned int rbState[] = {0, 4, 2, 6, 1, 7, 3, 5, 0, 4, 2, 6, 1, 7, 3, 5, 0, 4, 2, 6, 1, 7, 3, 5};
unsigned int rb1Dly = 200;

void rainbow1() {
  for (unsigned int l = 0; l < 24; l++) {
    strip.setPixelColor(l, rbColors[rbState[l]][0], rbColors[rbState[l]][1], rbColors[rbState[l]][2]);
    rbState[l] = (rbState[l] + 1) % 8;
  }
  strip.show();
}


unsigned int rb2Dly = 200;

void rainbow2() {
  for (unsigned int e = 0; e < 6; e++) {
    for (unsigned int l = e * 4; l < (e + 1) * 4; l++) {
      strip.setPixelColor(l, rbColors[rbState[e]][0], rbColors[rbState[e]][1], rbColors[rbState[e]][2]);
    }
    rbState[e] = (rbState[e] + 1) % 8;
  }

  strip.show();
}


void setup() {
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

    switch (mode) {
      case 0:
        switch (state)
        {
          case 1:
            dly = blinkDly;
            leftBlinker();
            break;
          case 2:
            dly = blinkDly;
            rightBlinker();
            break;
          case 3:
            dly = blinkDly;
            warnBlinker();
            break;
          default:
            dly = waitDly;
            wait();
        }
        break;
      case 1:
        switch (state)
        {
          case 1:
            dly = dly1;
            siren(leftSiren1, rightSiren1);
            break;
          case 2:
            dly = dly1;
            siren(leftSiren1, rightSiren1, horn1);
            break;
          case 3:
            dly = dly2;
            siren(leftSiren2, rightSiren2);
            break;
          case 4:
            dly = dly2;
            siren(leftSiren2, rightSiren2, horn2);
            break;
          default:
            dly = waitDly;
            wait();
        }
        break;
      case 2:
        switch (state)
        {
          case 1:
            dly = lightDly;
            headLight();
            break;
          case 2:
            dly = strobeDly;
            strobeLight();
            break;
          default:
            dly = waitDly;
            wait();
        }
        break;
      default:
        switch (state)
        {
          case 1:
            dly = rb1Dly;
            rainbow1();
            break;
          case 2:
            dly = rb2Dly;
            rainbow2();
            break;
          default:
            dly = waitDly;
            wait();
        }
    }

  }
}
