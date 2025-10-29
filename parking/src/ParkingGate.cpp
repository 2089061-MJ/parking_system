#include "ParkingGate.h"

ParkingGate::ParkingGate(uint8_t servoPin)
    : SERVO_PIN(servoPin), state(0) {
}

void ParkingGate::begin() {
    gateServo.attach(SERVO_PIN);
    gateServo.write(0);  // 초기 닫힘
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
                    state = 1;
                }
                else if (command == "close") {
                    gateServo.write(0);
                    Serial.println("게이트 닫힘");
                    state = 0;
                }
            }
            command = "";
        } else {
            command += c;
        }
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
