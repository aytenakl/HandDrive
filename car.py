import cv2
import mediapipe as mp
import math
import serial
import time


# ==========================================
# SETTINGS
# ==========================================

CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

MODEL_PATH = "hand_landmarker.task"

# Change COM5 to your Arduino COM port
SERIAL_PORT = "COM5"

SERIAL_BAUD = 9600


# ==========================================
# CONNECT TO ARDUINO
# ==========================================

arduino = serial.Serial(
    SERIAL_PORT,
    SERIAL_BAUD,
    timeout=1
)

time.sleep(2)

print("Arduino connected!")


# ==========================================
# MEDIAPIPE
# ==========================================

BaseOptions = mp.tasks.BaseOptions

HandLandmarker = mp.tasks.vision.HandLandmarker

HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions

RunningMode = mp.tasks.vision.RunningMode


options = HandLandmarkerOptions(

    base_options=BaseOptions(
        model_asset_path=MODEL_PATH
    ),

    running_mode=RunningMode.IMAGE,

    num_hands=2,

    min_hand_detection_confidence=0.5,

    min_hand_presence_confidence=0.5,

    min_tracking_confidence=0.5
)


detector = HandLandmarker.create_from_options(
    options
)


# ==========================================
# CAMERA
# ==========================================

camera = cv2.VideoCapture(0)

camera.set(
    cv2.CAP_PROP_FRAME_WIDTH,
    CAMERA_WIDTH
)

camera.set(
    cv2.CAP_PROP_FRAME_HEIGHT,
    CAMERA_HEIGHT
)


# ==========================================
# CALCULATE ANGLE
# ==========================================

def calculate_angle(point1, point2):

    x1, y1 = point1

    x2, y2 = point2

    angle = math.degrees(
        math.atan2(
            y2 - y1,
            x2 - x1
        )
    )

    return angle


# ==========================================
# CHECK FIST
# ==========================================

def is_fist(hand):

    index_tip = hand[8]

    middle_tip = hand[12]

    ring_tip = hand[16]

    pinky_tip = hand[20]


    index_pip = hand[6]

    middle_pip = hand[10]

    ring_pip = hand[14]

    pinky_pip = hand[18]


    fingers_closed = 0


    if index_tip.y > index_pip.y:

        fingers_closed += 1


    if middle_tip.y > middle_pip.y:

        fingers_closed += 1


    if ring_tip.y > ring_pip.y:

        fingers_closed += 1


    if pinky_tip.y > pinky_pip.y:

        fingers_closed += 1


    if fingers_closed >= 3:

        return True


    return False


# ==========================================
# SEND COMMAND
# ==========================================

last_command = ""


def send_command(command):

    global last_command


    # Don't send the same command repeatedly
    if command != last_command:

        arduino.write(
            (command + "\n").encode()
        )

        print("Arduino command:", command)

        last_command = command


# ==========================================
# MAIN LOOP
# ==========================================

try:

    while True:

        success, frame = camera.read()


        if not success:

            print("Camera error")

            break


        # Mirror camera

        frame = cv2.flip(
            frame,
            1
        )


        # ======================================
        # BGR TO RGB
        # ======================================

        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )


        # ======================================
        # MEDIAPIPE IMAGE
        # ======================================

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )


        # ======================================
        # DETECT HANDS
        # ======================================

        result = detector.detect(
            mp_image
        )


        direction = "STOP"

        steering_angle = 0

        fist_count = 0


        # ======================================
        # HANDS FOUND
        # ======================================

        if result.hand_landmarks:

            hands = result.hand_landmarks


            # ==================================
            # CHECK HANDS
            # ==================================

            for hand in hands:


                # Draw 21 landmarks

                for landmark in hand:

                    x = int(
                        landmark.x *
                        CAMERA_WIDTH
                    )

                    y = int(
                        landmark.y *
                        CAMERA_HEIGHT
                    )


                    cv2.circle(
                        frame,
                        (x, y),
                        4,
                        (255, 0, 0),
                        -1
                    )


                # Check fist

                if is_fist(hand):

                    fist_count += 1


            # ==================================
            # TWO HANDS
            # ==================================

            if len(hands) == 2:

                hand1 = hands[0]

                hand2 = hands[1]


                # Wrist points

                wrist1 = hand1[0]

                wrist2 = hand2[0]


                x1 = int(
                    wrist1.x *
                    CAMERA_WIDTH
                )

                y1 = int(
                    wrist1.y *
                    CAMERA_HEIGHT
                )


                x2 = int(
                    wrist2.x *
                    CAMERA_WIDTH
                )

                y2 = int(
                    wrist2.y *
                    CAMERA_HEIGHT
                )


                # Draw line between hands

                cv2.line(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    4
                )


                # Calculate steering angle

                steering_angle = calculate_angle(
                    (x1, y1),
                    (x2, y2)
                )


                # ==================================
                # TWO FISTS = STOP
                # ==================================

                if fist_count == 2:

                    direction = "STOP"

                    send_command("S")


                # ==================================
                # STEERING
                # ==================================

                else:

                    if steering_angle < -15:

                        direction = "RIGHT"

                        send_command("R")


                    elif steering_angle > 15:

                        direction = "LEFT"

                        send_command("L")


                    else:

                        direction = "FORWARD"

                        send_command("F")


            else:

                # If there are not two hands
                # stop the car

                direction = "STOP"

                send_command("S")


        else:

            # No hands = STOP

            direction = "STOP"

            send_command("S")


        # ======================================
        # DISPLAY FISTS
        # ======================================

        cv2.putText(
            frame,
            f"Fists: {fist_count}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )


        # ======================================
        # DISPLAY ANGLE
        # ======================================

        cv2.putText(
            frame,
            f"Angle: {int(steering_angle)}",
            (20, 75),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )


        # ======================================
        # DISPLAY DIRECTION
        # ======================================

        cv2.putText(
            frame,
            f"Direction: {direction}",
            (20, 115),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 255),
            3
        )


        # ======================================
        # DISPLAY CONNECTION
        # ======================================

        cv2.putText(
            frame,
            "Arduino: Connected",
            (20, 155),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )


        # ======================================
        # SHOW CAMERA
        # ======================================

        cv2.imshow(
            "Hand Gesture Controlled Car",
            frame
        )


        # ======================================
        # Q TO EXIT
        # ======================================

        if cv2.waitKey(1) & 0xFF == ord("q"):

            break


finally:

    # ALWAYS STOP CAR BEFORE EXIT

    try:

        arduino.write(
            b"S\n"
        )

    except:

        pass


    camera.release()

    detector.close()

    arduino.close()

    cv2.destroyAllWindows()

    print("Car stopped.")
    print("Program closed.")