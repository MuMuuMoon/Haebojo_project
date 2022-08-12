#include <ESP8266WiFiMulti.h>
#include <WiFiClientSecure.h>
#include <ESP8266WiFiGeneric.h>
#include <ESP8266WiFiSTA.h>
#include <WiFiClientSecureBearSSL.h>
#include <WiFiServerSecure.h>
#include <WiFiClient.h>
#include <ESP8266WiFiType.h>
#include <WiFiServer.h>
#include <WiFiUdp.h>
#include <ESP8266WiFiGratuitous.h>
#include <BearSSLHelpers.h>
#include <ESP8266WiFi.h>
#include <CertStoreBearSSL.h>
#include <ESP8266WiFiScan.h>
#include <WiFiServerSecureBearSSL.h>
#include <ArduinoWiFiServer.h>
#include <ESP8266WiFiAP.h>
const char* ssid="U+Net0A7D";
const char* password="1C1B032653";
WiFiServer server(80);

#include <Arduino.h>
#include "HX711.h"
const int LOADCELL_DOUT_PIN = 4, LOADCELL_SCK_PIN = 5;
const int LOADCELL_DOUT_PIN2 = 12, LOADCELL_SCK_PIN2 = 13;
HX711 scale, scale2;

void setup() {
  Serial.begin(115200);
  delay(100);

  Serial.println();
  Serial.print("CONNECTING TO ");
  Serial.println(ssid);

  //Start WiFi connection.
  WiFi.begin(ssid, password);
  while(WiFi.status()!= WL_CONNECTED){
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.println("Wifi connected!");

  //Start the server
  server.begin();
  Serial.println("Server started");

  //Print the IP adress
  Serial.println(WiFi.localIP());

  //Read 2 loadcells data 
  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  scale2.begin(LOADCELL_DOUT_PIN2, LOADCELL_SCK_PIN2);
  scale.set_scale();
  scale2.set_scale();
  scale.tare();
  scale2.tare();
}

void loop() {
  long reading, reading2;
  if (scale.is_ready() && scale2.is_ready()){
    reading = scale.get_units(10);
    reading2= scale2.get_units(10);

    Serial.println((String) reading + ", " + reading2);
  }
  else{
    Serial.println("hx711 connect error");
  }
  delay(100);
  WiFiClient client= server.available();
  client.println("HTTP/1.1 200 OK");
  client.println("Content-Type: text/html");
  client.println("Connection: close");
  client.println("Refresh: 1"); // 1초마다 자동으로 웹페이지 새로고침.
  client.println();
  client.println("<!DOCTYPE html>");
  client.println("<html xmlns='http://www.w3.org/1999/xhtml'>");
  client.println("<head>\n<meta http-equiv='Content-Type' content='text/html; charset=utf-8' />");
  //client.println("<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />");
  //client.println("<head>\n<meta charset='UTF-8'>");
  
  client.println("<title>SMART SHELF</title>"); // 웹 서버 페이지 제목 설정
  client.println("</head>\n<body>");
  client.println("<center>");
  client.println("<H1>NodeMCU_esp8266wifi_2loadcells test</H1>"); // 페이지 내용 설정
  client.println("<br>");
  client.println("<br>");
  client.println((String) reading + ", " + reading2);
  client.println("<pre>");
  client.print("</body>\n</html>");
  

}
