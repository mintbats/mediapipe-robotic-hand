MediaPipe Robotic Hand

A tendon-driven robotic hand that mirror a user's hand movement in real time using computer vision and servo motors.





Overview

This project uses a webcam and MediaPipe to detect hand landmarks and calculate finger bend angles.

The Arduino controls five servo motors that pull tendons attached to the robotic fingers.





Technologies

* Python
* OpenCV
* MediaPipe
* Arduino
* PySerial





How it works

Webcam -> MediaPipe -> Finger angle calculation -> Servo angle mapping -> EMA smoothing -> Serial communication -> Arduino -> Servo motors -> Robotic hand movement



