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



Hand Tracking:
The webcam is processed using MediaPipe, which detects 21 landmarks on the user's hand.

For each finger, selected landmarks are used to calculate a bend angle:

Finger: Lanmarks used

Thumb: MCP (2), IP(3), TIP(4)

Index: MCP (5), PIP(6), TIP(8)

Middle: MCP (9), IP(10), TIP(12)

Ring: MCP (13), IP(14), TIP(16)

Pinky: MCP (17), IP(18), TIP(20)

The angles between these landmarks are used to calculate how bent each finger is. These hand angles are then mapped to calibrated servo angle for the robotic hand.









Credits:

The 3D printed robotic hand model used in this project is based on the Arduino Flex Sensor Controlled Robot Hand project by Viral Science

