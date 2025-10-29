/*
 * 프로젝트명: 주차 관제 시스템
 * 작성자: 홍명진
 * 작성일: 2025-10-29
 * 설명: 본 프로젝트는 주차 관제 시스템으로 시리얼 통신을 이용해서 차단기를 제어하고(open, close) 
   Flask 웹서버와 연동하여 gui에서도 서보모터를 제어할 수 있게 구현하였습니다.
 * 하드웨어: Arduino Uno, 서보 모터
 */

#include "ParkingGate.h"
#define SERVO 3

ParkingGate gate(SERVO);

void setup() {
    Serial.begin(9600);
    gate.begin();
}

void loop() {
    gate.update();
}
