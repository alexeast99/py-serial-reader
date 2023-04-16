#include "Arduino.h"

void setup() {
    pinMode(LED_BUILTIN, OUTPUT);
    digitalWrite(LED_BUILTIN, HIGH);
    SerialUSB.begin();

}

void loop() {
    SerialUSB.println("Hello, world!");
    delay(1000);
}