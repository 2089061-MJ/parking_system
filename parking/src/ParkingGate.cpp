#include "ParkingGate.h"

ParkingGate::ParkingGate(uint8_t servoPin, uint8_t trigPin, uint8_t echoPin)
    : SERVO_PIN(servoPin), TRIG_PIN(trigPin), ECHO_PIN(echoPin), state(0) {
}

void ParkingGate::begin() {
    gateServo.attach(SERVO_PIN);
    gateServo.write(0);  // 초기 닫힘
    pinMode(TRIG_PIN, OUTPUT);
    pinMode(ECHO_PIN, INPUT);
    command = "";
}

void ParkingGate::update() {
    // 시리얼 명령 처리
    if (Serial.available()) {
        char c = Serial.read();

        if (c == '\n' || c == '\r') {
            command.trim();
            if (command.length() > 0) {
                Serial.println("받은 데이터 : " + command);

                if (command == "open") {
                    gateServo.write(120);
                    Serial.println("게이트 열림");
                }
                else if (command == "close") {
                    gateServo.write(0);
                    Serial.println("게이트 닫힘");
                }
            }
            command = "";
        } else {
            command += c;
        }
    }

    // 초음파 거리 측정
    float distance = measureDistance();
    Serial.print("Distance: ");
    Serial.print(distance);
    Serial.println(" cm");

    // 자동 열림/닫힘 로직
    if (distance < 8 && state == 0) {
        Serial.println("가까이 접근 - 게이트 열림");
        openGate();
        delay(3000);
    }
    else if (distance >= 9 && state == 1) {
        Serial.println("멀어짐 - 게이트 닫힘");
        closeGate();
        delay(3000);
    }

    delay(500);
}

void ParkingGate::openGate() {
    gateServo.write(120);
    state = 1;
}

void ParkingGate::closeGate() {
    gateServo.write(0);
    state = 0;
}

float ParkingGate::measureDistance() {
    digitalWrite(TRIG_PIN, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIG_PIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG_PIN, LOW);

    unsigned long duration = pulseIn(ECHO_PIN, HIGH);
    return duration * 0.034 / 2;
}