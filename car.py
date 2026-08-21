import cv2
import mediapipe as mp
from mediapipe.tasks import python   
from mediapipe.tasks.python import vision
import serial
import time
import math

WIDTH = 640
HEIGHT = 360

arduino = serial.Serial("COM16", 9600)
time.sleep(2)

model_path = r"C:\Users\lenovo loq\OneDrive\Desktop\Hand_Click_Project2\hand_landmarker.task"
base_options = python.BaseOptions(
    model_asset_path=model_path
)

options = vision.HandLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.IMAGE,
    num_hands=2
)

detector = vision.HandLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
cap.set(cv2.CAP_PROP_FPS, 30)

last_command = ""

while cap.isOpened():

    success, frame = cap.read()

    if not success:
        continue

    frame = cv2.flip(frame, 1)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb_frame
    )

    result = detector.detect(mp_image)

    command = "S"

    if len(result.hand_landmarks) == 2:

        hand1 = result.hand_landmarks[0]
        hand2 = result.hand_landmarks[1]

        x1 = hand1[0].x * WIDTH
        y1 = hand1[0].y * HEIGHT

        x2 = hand2[0].x * WIDTH
        y2 = hand2[0].y * HEIGHT

        dx = x2 - x1
        dy = y2 - y1

        angle = math.degrees(math.atan2(dy, dx))

        if angle < 0:
            angle += 180

        if angle < 65:
            command = "R"

        elif angle > 115:
            command = "L"

        else:
            command = "F"

        for hand in result.hand_landmarks:

            for landmark in hand:

                cx = int(landmark.x * WIDTH)
                cy = int(landmark.y * HEIGHT)

                cv2.circle(
                    frame,
                    (cx, cy),
                    4,
                    (0, 255, 0),
                    cv2.FILLED
                )

        cv2.line(
            frame,
            (int(x1), int(y1)),
            (int(x2), int(y2)),
            (255, 255, 0),
            3
        )

        cv2.putText(
            frame,
            f"Angle: {int(angle)}",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

    else:
        command = "S"

    if command != last_command:
        arduino.write(command.encode())
        last_command = command

    if command == "F":
        text = "FORWARD"

    elif command == "L":
        text = "LEFT"

    elif command == "R":
        text = "RIGHT"

    else:
        text = "STOP"

    cv2.putText(
        frame,
        text,
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2
    )

    cv2.imshow(
        "Hand Controlled Car",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

arduino.write(b"S")

cap.release()
arduino.close()
cv2.destroyAllWindows()
