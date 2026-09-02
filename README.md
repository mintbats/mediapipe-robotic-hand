MediaPipe Robotic Hand:

A tendon-driven robotic hand that mirror a user's hand movement in real time using computer vision and servo motors.





Overview

This project uses a webcam and MediaPipe to detect hand landmarks and calculate finger bend angles.

The Arduino controls five servo motors that pull tendons attached to the robotic fingers.





Technologies:

* Python
* OpenCV
* MediaPipe
* Arduino
* PySerial





Hardware:

* Arduino UNO r3
* MG90S micro servo motors x5
* Tendon driven 3D printed robotic hand based on the design by Viral Science
* Fishing line fore finger tendons
* Elastic cord for finger return
* Breadboard and jumper wires
* Webcam



How it works:

Webcam -> MediaPipe -> Finger angle calculation -> Servo angle mapping -> EMA smoothing -> Serial communication -> Arduino -> Servo motors -> Robotic hand movement



Credits:

The 3D printed robotic hand model used in this project is based on the Arduino Flex Sensor Controlled Robot Hand project by Viral Science

