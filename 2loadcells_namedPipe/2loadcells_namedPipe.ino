#include <Arduino.h>
#include "HX711.h"

const int LOADCELL_DOUT_PIN = 4, LOADCELL_SCK_PIN = 5;
const int LOADCELL_DOUT_PIN2 = 12, LOADCELL_SCK_PIN2 = 13;

HX711 scale, scale2;

void setup() {
    Serial.begin(115200);
    scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
    scale2.begin(LOADCELL_DOUT_PIN2, LOADCELL_SCK_PIN2);
    
    scale.set_scale();
    scale2.set_scale();

//    Serial.println("Tare. remove any weights");
//    delay(500);
    scale.tare();
    scale2.tare();
    Serial.println("Tare done");
}

void loop() {
  if (scale.is_ready() && scale2.is_ready()){
    long reading = scale.get_units(10);
    long reading2= scale2.get_units(10);

    Serial.println((String) reading + ", " + reading2);
  }
  else{
    Serial.println("hx711 connect error");
  }
  delay(100);
}
