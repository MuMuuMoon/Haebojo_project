#include <SoftwareSerial.h>

 long baud[8]={ 4800, 9600, 14400, 19200, 28800, 38400, 57600, 115200 };
 //SoftwareSerial BTSerial(4,5);   //bluetooth module Tx:Digital 2 Rx:Digital 3



// 명령어를 보내고 Response를 받는다.

void sendCmd(char* cmd)
{
  Serial1.write(cmd);
  Serial.print(cmd);
  Serial.print("-->");
  delay(400);
  while (Serial1.available()) {  Serial.write(Serial1.read()); }
  Serial.println();
}


void setup() {
  pinMode(8, OUTPUT);    //HC-05
  digitalWrite(8,HIGH);
 
  Serial.begin(9600);

  delay(1000);
  Serial.println("Search baud rate: Send AT, wait for OK");
  

  // 여러종류의 baud를 설정하여 맞는 속도를 찾는다.
  for(int i=0;i<8;i++) { 
    Serial.print("Baud :");
    Serial.println(baud[i]);    
    Serial1.begin( baud[i] );
    delay(500);
    // AT  명령어를 2번 정도 보낸다. 간혹 기존에 명령어가 잘못 들어간 경우가 있음.
    Serial1.print("AT\r\n");
    delay(100);
    Serial1.print("AT");
    delay(100);   // 지연시간은 꼭 필요하다.

    while(Serial1.available()){
      Serial.print((char)Serial1.read());  // OK 문자를 받는다.
      }
  }  
 

  // HM-10 상태를 자동으로 점검하기

  Serial.println();
  Serial.println("HM-10 status");
  sendCmd("AT+ADDR?");
  sendCmd("AT+FILT?");
  sendCmd("AT+NAME?");
  sendCmd("AT+PASS?");
  sendCmd("AT+POWE?");
  sendCmd("AT+MODE?");
  sendCmd("AT+ROLE?");
  sendCmd("AT+ADTY?");
  sendCmd("AT+SHOW?");
  sendCmd("AT+IMME?");
  sendCmd("AT+RSSI?");
  sendCmd("AT+UUID?");
  sendCmd("AT+TYPE?");
  sendCmd("AT+DISC?");
  sendCmd("AT+PWRM?");
  sendCmd("AT+NOTP?");
  sendCmd("AT+IBEA?");
  sendCmd("AT+SAVE?");
  sendCmd("AT");
}



void loop()

{
  if (Serial1.available())
    Serial.write(Serial1.read());
  if (Serial.available())
    Serial1.write(Serial.read());

}
