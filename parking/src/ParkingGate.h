#ifndef PARKING_GATE_H
#define PARKING_GATE_H

#include <Servo.h>
#include <Arduino.h>

class ParkingGate {
public:
    ParkingGate(uint8_t servoPin, uint8_t trigPin, uint8_t echoPin);
    void begin();
    void update();

private:
    void openGate();
    void closeGate();
    float measureDistance();

    Servo gateServo;
    uint8_t SERVO_PIN;
    uint8_t TRIG_PIN;
    uint8_t ECHO_PIN;
    int state;  // 0 = closed, 1 = open
    String command;
};

#endif