#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <PxMatrix.h>
#include <Ticker.h>

#define P_LAT 16
#define P_A 5
#define P_B 4
#define P_C 15
#define P_D 12
#define P_E 0
#define P_OE 2
#define Mwidth 32
#define Mheight 32

const char* ssid= YOUR WIFI;
const char* pass= YOUR WIFI PASSWORD;
ESP8266WebServer server;
PxMATRIX display(32,32,P_LAT, P_OE,P_A,P_B,P_C,P_D);
Ticker display_ticker;

uint16_t myRED = display.color565(255, 0, 0);
uint16_t myGREEN = display.color565(0, 255, 0);
uint16_t myBLUE = display.color565(0, 0, 255);
uint16_t myWHITE = display.color565(255, 255, 255);
uint16_t myBLACK = display.color565(0, 0, 0);

uint8_t display_draw_time=70;

void setup() {
  Serial.begin(115200);
  Serial.println();
  
  display.begin(16);
  display.clearDisplay();
  display_ticker.attach(0.004, updater);
  yield();
  
  WiFi.begin(ssid,pass);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println(".");
  }
  Serial.print("NodeMCU IP Address:");
  Serial.print(WiFi.localIP());

  server.on("/",[](){server.send(200,"text/plain", "Hello");});
  server.on("/setColor", setPixelColor);
  server.on("/clear", clearMatrix);
  server.begin();
}

void loop() {
  server.handleClient();
  delay(50);

}

void updater() {
  display.display(display_draw_time);
}

void setPixelColor()
{
  String x = server.arg("X");
  String y = server.arg("Y");
  String r = server.arg("red");
  String g = server.arg("green");
  String b = server.arg("blue");
  uint16_t color = display.color565(r.toInt(),g.toInt(),b.toInt());
  display.drawPixel(x.toInt(), y.toInt(), color);
  String msg = x+ " " + y + " " + r + " " + g + " " + b;
  server.send(200,"text/plain",msg);
}

void clearMatrix()
{
  for (int i=0; i<32; i++) {
    for (int j=0; j<32; j++) {
      display.drawPixel(i,j,0x000);
    }
  }
  server.send(200);
}
