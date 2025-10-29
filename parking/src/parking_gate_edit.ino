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
