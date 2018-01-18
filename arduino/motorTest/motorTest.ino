#include <Servo.h>

Servo s;
int i = 50;
bool up = true;
const int pin = 5; // A3

void setup() {
  s.attach(pin);
  digitalWrite(17, HIGH);
  s.write(90);
}

void loop() {
  s.write(map(i, -5, 101, 0, 180));
  i += up ? 1 : -1;
  if (i >= 100) {
    up = false;
    digitalWrite(17, LOW);
  } else if (i <= 0) {
    up = true;
    digitalWrite(17, HIGH);
  }
  delay(20);
}
