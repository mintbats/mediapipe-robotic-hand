#include <Servo.h>

Servo thumbServo;
Servo indexServo;
Servo middleServo;
Servo ringServo;
Servo pinkyServo;

const int THUMB_PIN  = 10;
const int INDEX_PIN  = 3;
const int MIDDLE_PIN = 5;
const int RING_PIN   = 6;
const int PINKY_PIN  = 9;

void setup() {

  Serial.begin(9600);

  thumbServo.attach(THUMB_PIN);
  indexServo.attach(INDEX_PIN);
  middleServo.attach(MIDDLE_PIN);
  ringServo.attach(RING_PIN);
  pinkyServo.attach(PINKY_PIN);
}

void loop() {

  if (Serial.available() > 0) {

    String data = Serial.readStringUntil('\n');

    // Python sends:
    // THUMB,INDEX,MIDDLE,RING,PINKY

    int comma1 = data.indexOf(',');
    int comma2 = data.indexOf(',', comma1 + 1);
    int comma3 = data.indexOf(',', comma2 + 1);
    int comma4 = data.indexOf(',', comma3 + 1);

    // Ignore bad/incomplete messages
    if (
      comma1 == -1 ||
      comma2 == -1 ||
      comma3 == -1 ||
      comma4 == -1
    ) {
      return;
    }

    int thumbAngle =
      data.substring(0, comma1).toInt();

    int indexAngle =
      data.substring(comma1 + 1, comma2).toInt();

    int middleAngle =
      data.substring(comma2 + 1, comma3).toInt();

    int ringAngle =
      data.substring(comma3 + 1, comma4).toInt();

    int pinkyAngle =
      data.substring(comma4 + 1).toInt();


    // HARD SAFETY LIMITS

    thumbAngle = constrain(
      thumbAngle, 0, 180
    );

    indexAngle = constrain(
      indexAngle, 0, 180
    );

    middleAngle = constrain(
      middleAngle, 0, 180
    );

    ringAngle = constrain(
      ringAngle, 70, 180
    );

    pinkyAngle = constrain(
      pinkyAngle, 0, 180
    );


    // MOVE SERVOS

    thumbServo.write(thumbAngle);
    indexServo.write(indexAngle);
    middleServo.write(middleAngle);
    ringServo.write(ringAngle);
    pinkyServo.write(pinkyAngle);
  }
}