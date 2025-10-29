#include "ParkingGate.h"

#define SERVO 3
#define TRIG A0 
#define ECHO A1

ParkingGate gate(SERVO, TRIG, ECHO);

void setup() {
    Serial.begin(9600);
    gate.begin();
}

void loop() {
    gate.update();
}
