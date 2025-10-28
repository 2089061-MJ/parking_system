#include <SoftwareSerial.h>
#include <Servo.h>
#define ir_start_pin 4
#define ir_end_pin 5
#define SERVO 6

#define DEBUG true
SoftwareSerial esp8266(2, 3);

const String server_ip = "192.168.0.14";
const int server_port = 5000;

Servo gateServo;

bool car_in = false;
bool car_out = false;

void setup(){
  Serial.begin(9600);
  esp8266.begin(9600);

  pinMode(ir_start_pin, INPUT);
  pinMode(ir_end_pin, INPUT);
  
  gateServo.attach(SERVO);
  gateServo.write(0); // 초기 설정은 0(게이트 문)

  sendData("AT+RST\r\n", 2000, DEBUG);
  sendData("AT+CWMODE=1\r\n", 1000, DEBUG);
  sendData("AT+CWJAP=\"202호 강의실 2.4\",\"4719222202\"\r\n", 5000, DEBUG);
  sendData("AT+CIPMUX=0\r\n", 1000, DEBUG);
  sendData("AT+CIPSTATUS\r\n", 2000, DEBUG);
  sendData("AT+CIFSR\r\n", 2000, DEBUG);
}
void loop() {
  if (digitalRead(ir_start_pin) == HIGH && !car_in) {
    car_in = true;
    Serial.println("차량이 입차하였습니다.");
    openGate();
    sendMsg("CAR_IN");
    delay(5000);
    closeGate();
  }
   if (digitalRead(ir_start_pin) == LOW) {
    car_in = false;  // 센서가 LOW 되면 다시 이벤트 가능
  }

  if (digitalRead(ir_end_pin) == HIGH && !car_out) {
    car_out = true;
    Serial.println("차량이 출차하였습니다.");
    openGate();
    sendMsg("CAR_OUT");
    delay(5000);
    closeGate();
  }
  if (digitalRead(ir_end_pin) == LOW) {
    car_out = false;
  }
}

void openGate() {
  gateServo.write(90);
  Serial.println("게이트 열림");
}
void closeGate() {
  gateServo.write(0);
  Serial.println("게이트 닫힘");
}
void sendMsg(String event_type) {
  // json 데이터 형식으로 Flask 서버로 보냄
  String jsonData = "{\"event_type\":\"" + event_type + "\"}";
  String cmd = "AT+CIPSTART=\"TCP\",\"" + server_ip + "\"," + String(server_port) + "\r\n";
  sendData(cmd, 2000, DEBUG);

  String httpRequest = "POST /event HTTP/1.1\r\n";
  httpRequest += "Host: " + server_ip + "\r\n";
  httpRequest += "Content-Type: application/json\r\n";
  httpRequest += "Content-Length: " + String(jsonData.length()) + "\r\n\r\n";
  httpRequest += jsonData;

  cmd = "AT+CIPSEND=" + String(httpRequest.length()) + "\r\n";
  sendData(cmd, 2000, DEBUG);
  sendData(httpRequest, 2000, DEBUG);
  sendData("AT+CIPCLOSE\r\n", 1000, DEBUG);

  Serial.println("Flask 서버로 이벤트 전송 완료: " + event_type);
}

String sendData(String command, const int timeout, boolean debug) {
  String response = "";
  esp8266.print(command);
  long int time = millis();

  while ((time + timeout) > millis()) {
    while (esp8266.available()) {
      char c = esp8266.read();
      response += c;
    }
  }
  if (debug) {
    Serial.print(response);
  }
  return response;
}

