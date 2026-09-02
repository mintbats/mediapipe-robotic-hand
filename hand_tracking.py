# Robotic hand control using MediaPipe and Arduino
"""
MediaPipe Robotic Hand Controller

Tracks one hand using MediaPipe, calculates finger bend angles,
maps them to calibrated servo positions, smooths commands using EMA, 
and sends five servo angles to an Arduino over serial

"""
# 1. Imports

import cv2
import mediapipe as mp
import math
import serial
import time


# 2. Arduino serial connection

SERIAL_PORT = "COM3"
BAUD_RATE = 9600

arduino = serial.Serial(SERIAL_PORT, BAUD_RATE)

time.sleep(2)

print("Connected to Arduino on COM3")


# 3. MediaPipe

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

# track one hand with 70% detection and tracking confidence thresholds
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)

# 4. Camera

# use default cam (0), DirectShow
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

print("Camera opened:", cap.isOpened())

if not cap.isOpened():
    print("ERROR: Camera could not be opened.")
    print("Try changing camera number 0 to 1 or 2.")

    arduino.close()
    exit()


# 5. Finger landmarks
# Thumb: MCP, IP, TIP
# Others: MCP, PIP, TIP

fingers = {
    "THUMB":  (2, 3, 4),
    "INDEX":  (5, 6, 8),
    "MIDDLE": (9, 10, 12),
    "RING":   (13, 14, 16),
    "PINKY":  (17, 18, 20)
}


# 6. Calibration

calibration = {

    "THUMB": {
        "human_closed": 80,
        "human_open": 170,
        "servo_closed": 180,
        "servo_open": 0
    },

    "INDEX": {
        "human_closed": 6,
        "human_open": 178,
        "servo_closed": 0,
        "servo_open": 180
    },

    "MIDDLE": {
        "human_closed": 5,
        "human_open": 178,
        "servo_closed": 0,
        "servo_open": 180
    },

    "RING": {
        "human_closed": 11,
        "human_open": 175,
        "servo_closed": 70,
        "servo_open": 180
    },

    "PINKY": {
        "human_closed": 20,
        "human_open": 171,
        "servo_closed": 180,
        "servo_open": 0
    }
}

# 7. Calculate finger angle

def calculate_angle(a, b, c):

    # vector B -> A
    ba_x = a.x - b.x
    ba_y = a.y - b.y

    # vector B -> C
    bc_x = c.x - b.x
    bc_y = c.y - b.y

    # dot product
    dot_product = (ba_x * bc_x + ba_y * bc_y)

    # length of vector BA
    magnitude_ba = math.sqrt(ba_x**2 + ba_y**2)

    # length of vector BC
    magnitude_bc = math.sqrt(bc_x**2 + bc_y**2)


    # prevent division by zero
    if magnitude_ba == 0 or magnitude_bc == 0:
        return 0


    # cos(theta)
    cos_angle = dot_product / (magnitude_ba * magnitude_bc)

    # prevent floating-point errors
    cos_angle = max(-1.0, min(1.0, cos_angle))

    # radians -> degrees
    angle = math.degrees(math.acos(cos_angle))

    return angle

# 8. Map human angle to servo angle
# @params 
# value - current human finger angle
# in_min - human close angle
# in_max - human open angle
# out_min - servo close angle
# out_max - servo open angle

def map_value(value, in_min, in_max, out_min, out_max):

    # clamp human angle to calibrated range
    value = max(in_min, min(value, in_max))

    mapped = (
        out_min 
        + (value - in_min) 
        * (out_max - out_min) 
        / (in_max - in_min)
    )

    return mapped

# 9. EMA smoothing

alpha = 0.2

smoothed_angles = {
    "THUMB": None,
    "INDEX": None,
    "MIDDLE": None,
    "RING": None,
    "PINKY": None
}


def ema(new_value, previous_value, alpha):

    if previous_value is None:
        return new_value

    return (alpha * new_value + (1 - alpha) * previous_value)

# 10. Deadband

DEADBAND = 3

last_sent_angles = {
    "THUMB": None,
    "INDEX": None,
    "MIDDLE": None,
    "RING": None,
    "PINKY": None
}

def should_send(new_commands):

    for finger in new_commands:

        old_value = last_sent_angles[finger]
        new_value = new_commands[finger]

        # first reading always sends
        if old_value is None:
            return True

        # send if ANY servo changes >= deadband
        if abs(new_value - old_value) >= DEADBAND:
            return True

    return False

# 11. No hand safety

last_hand_time = time.time()

NO_HAND_TIMEOUT = 1.0

# open servo positions
OPEN_COMMANDS = {
    "THUMB": 0,
    "INDEX": 180,
    "MIDDLE": 180,
    "RING": 180,
    "PINKY": 0
}

open_sent = False


# 12. Sends commands to Arduino

def send_commands(commands):

    # Serial order: THUMB,INDEX,MIDDLE,RING,PINKY

    message = (
        f"{commands['THUMB']},"
        f"{commands['INDEX']},"
        f"{commands['MIDDLE']},"
        f"{commands['RING']},"
        f"{commands['PINKY']}\n"
    )


    arduino.write(message.encode())

    # remember what was actually sent
    for finger in commands:

        last_sent_angles[finger] = commands[finger]

    print("SENT:", message.strip())


# 13. Main camera loop

while True:

    success, frame = cap.read()

    if not success:

        print("ERROR: Camera opened but frame could not be read.")

        break

    # flip fran horizontally for mirror view

    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = hands.process(rgb)

    servo_commands = {}

    # find hand
    if result.multi_hand_landmarks:

        last_hand_time = time.time()

        open_sent = False

        # get first detected hand
        hand = result.multi_hand_landmarks[0]

        # hand skeleton
        mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

        # process each finger
        for finger, points in fingers.items():

            point1_id, point2_id, point3_id = points

            point1 = hand.landmark[point1_id]

            point2 = hand.landmark[point2_id]

            point3 = hand.landmark[point3_id]

            human_angle = calculate_angle(point1, point2, point3)

            c = calibration[finger]

            raw_servo_angle = map_value(
                human_angle,

                c["human_closed"],
                c["human_open"],

                c["servo_closed"],
                c["servo_open"]
            )

            smoothed_angles[finger] = ema(raw_servo_angle, smoothed_angles[finger], alpha)

            smooth_servo_angle = smoothed_angles[finger]

            servo_commands[finger] = int(round(smooth_servo_angle))

            print(
                f"{finger}: "
                f"Hand={human_angle:.1f}°  "
                f"Raw={raw_servo_angle:.1f}°  "
                f"EMA={smooth_servo_angle:.1f}°"
            )


        if len(servo_commands) == 5:

            if should_send(servo_commands):

                send_commands(servo_commands)

            else:

                print("NO SEND -> change smaller than deadband")

        print("------------------")

    else:

        time_without_hand = (time.time() - last_hand_time)

        if (time_without_hand > NO_HAND_TIMEOUT and not open_sent):

            send_commands(OPEN_COMMANDS)

            open_sent = True

            print("NO HAND -> OPEN")


    cv2.imshow("Hand Tracking", frame)

    # Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# 14. Clean up

cap.release()

cv2.destroyAllWindows()

arduino.close()

hands.close()

print("Arduino connection closed")
print("Camera closed")