#include <Arduino.h>
#include "HX711.h"

const int LOADCELL_DOUT_PIN = 4, LOADCELL_SCK_PIN = 5;
const int LOADCELL_DOUT_PIN2 = 12, LOADCELL_SCK_PIN2 = 13;

HX711 scale, scale2;

void setup() {
    Serial.begin(115200); // 9600이면 1초에 900bytes 정도 전송 가능.
//    Serial.begin(9600);
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

    Serial.println((String) reading + ", " + reading2); // (String) 없애면 알아볼 수 없는 값 나옴.
  }
  else{
    Serial.println("hx711 connect error");
  }
  delay(100); // 시간이 길어지면 receiver에서 출력되는 값이 더 많아짐. 
              // 시리얼통신이기 때문에 직렬로 입력되는 data가 너무 빨리 들어가면 named pipe가 출력할 때 
              // 과부하가 걸려서 자동 종료되는 원리?
}
