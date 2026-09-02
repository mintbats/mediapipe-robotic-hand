# MediaPipe Robotic Hand

A tendon-driven robotic hand that mirror a user's hand movement in real time using computer vision, MediaPipe hand tracking, and an Arduino.



## Overview

This project uses a webcam and MediaPipe to detect hand landmarks and calculate finger bend angles.

The Arduino controls five servo motors that pull tendons attached to the robotic fingers.



##### How it works

Webcam -> MediaPipe -> Finger angle calculation -> Servo angle mapping -> EMA smoothing -> Serial communication -> Arduino -> Servo motors -> Robotic hand movement



##### Hardware

* Arduino UNO r3
* MG90S micro servo motors x5
* Tendon driven 3D printed robotic hand based on the design by Viral Science
* Fishing line fore finger tendons
* Elastic cord for finger return
* Breadboard and jumper wires
* Webcam



##### Software

* Python
* OpenCV
* MediaPipe
* PySerial
* Arduino IDE





Hand Tracking
The webcam is processed using MediaPipe, which detects 21 landmarks on the user's hand.
---

For each finger, selected landmarks are used to calculate a bend angle:

Finger: Lanmarks used

Thumb: MCP (2), IP(3), TIP(4)

Index: MCP (5), PIP(6), TIP(8)

Middle: MCP (9), IP(10), TIP(12)

Ring: MCP (13), IP(14), TIP(16)

Pinky: MCP (17), IP(18), TIP(20)

The angles between these landmarks are used to calculate how bent each finger is. These hand angles are then mapped to calibrated servo angle for the robotic hand.





##### Finger Angle Calculation

Three landmarks form two vectors around the finger joint.

When the finger is straight, the calculated angle is close to 180°. As the finger bends, the angle decreases.

Each servo was experimentally calibrated to determine the suitable open and closed positions.

Each finger is calibrated independently because servo orientation, tendon routing, tendon tension, and mechanical limits affect its usable range.

&#x20;



##### EMA Smoothing

Raw hand tracking movements can fluctuate between video frames. Sending every fluctuation to servo can cause jittery movement.





##### Serial Communication

Python sends five calculated servo position to the Arduino through serial communication.

The values are transmitted as comma separated servo angles representing:

Thumb, Index, Middle, Ring, Pinky

The Arduino reads the incoming serial data, separates the values, converts to integers, and updates the corresponding servo motors.

A deadband is also used to avoid repeatedly sending very small changes.





##### Installation

pip install -r requirements.txt

The main python dependencies are:

* OpenCV
* MediaPipe
* PySerial

Upload the Arduino program to the Arduino board before running the python controller.





##### Running the Project

1. Connect the Arduino and servo control system
2. Upload the Arduino program
3. Connect the webcam
4. Check the serial port used by Arduino
5. Run: python hand\_tracking.py
6. Place a hand in view of the webcam
7. The detected finger movements are converted into commands for the robotic hand



##### What I Learned

Through this project, I worked with:

* Real time computer vision using OpenCV
* Hand landmark detection using MediaPipe
* Vector-based finger angle calculation
* Mapping computer vision measurements to physical actuator
* Servo Calibration
* EMA smoothing
* Serial communication between Python and Arduino
* Tendon-driven robotic mechanisms
* Integration and debugging of software, electronics, and mechanical components
* Git and GitHub version control and project documentation

##### 

##### Future Improvements

Possible future developments include:

* ROS2 integration
* Improved finger-joint tracking
* Improved tendon routing and mechanical calibration
* Designed a custom PCB to replace the breadboard and simplify servo power and signal wiring

##### 

##### Credits

The 3D printed robotic hand model used in this project is based on the Arduino Flex Sensor Controlled Robot Hand project by Viral Science.



Original project and 3D model:

https://www.viralsciencecreativity.com/post/arduino-flex-sensor-controlled-robot-hand

