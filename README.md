# HandDrive
HandDrive 🚗✋

Computer Vision Based Gesture-Controlled Car using Python, MediaPipe, OpenCV & Arduino

📌 About The Project

HandDrive is a real-time gesture-controlled robotic car project that allows the user to control a car using hand movements captured through a camera.

Instead of using a traditional remote control, the system uses Computer Vision to detect the user's hands and interpret their gestures as movement commands.

The camera captures the user's hands, MediaPipe detects the 21 hand landmarks, and Python analyzes the position and angle of the hands to determine the desired direction.

The movement command is then sent from Python to an Arduino through serial communication, allowing the Arduino to control the robotic car.

🎯 Project Goal

The main goal of this project is to combine:

🤖 Robotics
👁️ Computer Vision
✋ Hand Gesture Recognition
🐍 Python
🔌 Arduino
📡 Serial Communication

to create a simple and interactive human-machine interface for controlling a robotic car.

⚙️ How It Works

The system follows this process:

Camera
   ↓
OpenCV
   ↓
MediaPipe Hand Detection
   ↓
21 Hand Landmarks
   ↓
Hand Gesture Analysis
   ↓
Calculate Hand Angle
   ↓
Determine Direction
   ↓
Serial Communication
   ↓
Arduino
   ↓
Motor Driver
   ↓
🚗 Car Movement
✋ Gesture Controls

The car responds to the user's hand positions and gestures.

Hand Gesture	Command	Car Action
✋ Two hands aligned	F	Forward
↖️ Hands angled	L	Left
↗️ Hands angled	R	Right
✊✊ Two fists	S	Stop
One hand	S	Stop
No hands detected	S	Stop

The Python program sends simple commands through the serial connection:

F → Forward
L → Left
R → Right
S → Stop
🧠 Computer Vision

The project uses MediaPipe Hand Landmarker to detect the user's hands.

Each detected hand contains 21 landmarks representing important points such as:

Wrist
Thumb
Index Finger
Middle Finger
Ring Finger
Pinky

These landmarks are used to analyze the hand position and determine whether the user is making a fist or changing the steering direction.

📐 Steering System

When two hands are detected, the system calculates the angle between their wrist positions.

The angle is calculated using:

angle = math.degrees(
    math.atan2(
        y2 - y1,
        x2 - x1
    )
)

The calculated angle determines the steering command.

Angle < -15°  → RIGHT
Angle >  15°  → LEFT
Otherwise     → FORWARD
✊ Emergency Stop

Safety is an important part of the project.

If both hands are detected as fists:

Two Fists → STOP

The system also automatically stops the car when:

No hands are detected.
Only one hand is detected.
The camera fails.
The program is closed.

Before exiting, Python sends:

S

to ensure that the car receives a stop command.

🛠️ Technologies Used
Software
Python
OpenCV
MediaPipe
PySerial
Math
Hardware
Arduino
DC Motors
Motor Driver
Robotic Car Chassis
USB / Serial Communication
📂 Project Structure
HandDrive/
│
├── videos/
│   └── v/
│       └── car2.py
│
├── hand_landmarker.task
│
├── Arduino/
│   └── HandDrive.ino
│
├── README.md
│
└── requirements.txt
📦 Installation

Clone the repository:

git clone https://github.com/YOUR_USERNAME/HandDrive.git

Enter the project folder:

cd HandDrive

Install the required Python libraries:

pip install opencv-python mediapipe pyserial
▶️ Running The Project

First, connect the Arduino to the computer.

Then check the Arduino's COM port.

For example:

SERIAL_PORT = "COM5"

Change COM5 to the COM port assigned to your Arduino.

Make sure the baud rate matches the Arduino code:

SERIAL_BAUD = 9600

Then run:

python car2.py

The camera will open and the system will start detecting your hands.

Press:

Q

to close the program.

🔌 Serial Communication

Python communicates with the Arduino using PySerial.

The communication settings are:

Port: COM5
Baud Rate: 9600

The Python program sends one of four commands:

F
L
R
S

The Arduino receives these commands and controls the motors accordingly.

🚗 Arduino Side

The Arduino is responsible for receiving the commands from Python and controlling the motor driver.

Conceptually:

F → Move Forward
L → Turn Left
R → Turn Right
S → Stop

This creates a clear separation between the two parts of the project:

Python
│
├── Camera
├── OpenCV
├── MediaPipe
├── Gesture Detection
└── Serial Commands
          │
          ↓
       Arduino
          │
          ├── Motor Driver
          └── Motors
💡 Future Improvements

Possible improvements for future versions include:

 Add backward movement.
 Add speed control using hand distance.
 Add more gestures.
 Add Bluetooth communication.
 Add obstacle detection.
 Add ultrasonic sensors.
 Add autonomous driving mode.
 Improve hand tracking stability.
 Add a graphical control interface.
 Add real-time speed monitoring.
 Add multiple gesture profiles.
🎥 Demo

A demonstration video of the project will be added here.
