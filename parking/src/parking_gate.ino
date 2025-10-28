#include <Servo.h>
#define SERVO 2
#define TRIG 6  // 초음파 trig핀
#define ECHO 7  // 초음파 echo핀

Servo gateServo;
int i = 0;  // 0 = 닫힘, 1 = 열림

void setup() {
  Serial.begin(9600);
  gateServo.attach(SERVO);
  gateServo.write(0); // 닫힘
  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);
}

void loop() {
  // 초음파 TRIG
  digitalWrite(TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG, LOW);

  // 거리 측정
  unsigned long duration = pulseIn(ECHO, HIGH);
  float distance = duration * 0.034 / 2;

  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");

  // 문  열고 닫기 조건
  if (distance < 8 && i == 0) {
    Serial.println("가까이 접근 - 게이트 열림");
    gateServo.write(120);
    i = 1;
    delay(3000);
  }
  else if (distance >= 9 && i == 1) {
    Serial.println("멀어짐 - 게이트 닫힘");
    gateServo.write(0);
    i = 0;
    delay(3000);
  }
  delay(500);
}