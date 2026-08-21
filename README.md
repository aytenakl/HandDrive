# 🚗 HandDrive

### Computer Vision Based Gesture-Controlled Robotic Car

**HandDrive** is a real-time robotic car controlled using **hand gestures** detected through a webcam.

The project combines **Computer Vision, Hand Gesture Recognition, Python, MediaPipe, OpenCV, Arduino, and an L298N Motor Driver** to create a hands-free human-machine interface for controlling a robotic car.

---

## 📌 About The Project

HandDrive allows the user to control a robotic car by moving their hands in front of a camera.

Instead of using a traditional remote control, the system uses **MediaPipe Hand Landmarker** to detect two hands and analyze the angle between their wrist positions.

Python converts the detected hand movement into a simple movement command and sends it to the Arduino through **Serial Communication**.

The Arduino receives the command and controls the motors through an **L298N Motor Driver**.

### System Flow

```text
Webcam
   ↓
OpenCV
   ↓
MediaPipe Hand Landmarker
   ↓
21 Hand Landmarks
   ↓
Hand Position & Angle Analysis
   ↓
Gesture Classification
   ↓
Serial Command
   ↓
Arduino
   ↓
L298N Motor Driver
   ↓
DC Motors
   ↓
🚗 Robotic Car
```

---

## 🎯 Project Goal

The main goal of HandDrive is to combine:

* 🤖 Robotics
* 👁️ Computer Vision
* ✋ Hand Gesture Recognition
* 🐍 Python
* 🔌 Arduino
* 📡 Serial Communication

into an interactive system for controlling a robotic vehicle using natural hand movements.

---

## ✋ Gesture Controls

The current version uses two detected hands to determine the movement direction.

| Hand Position                  | Command | Car Action |
| ------------------------------ | ------- | ---------- |
| ↔️ Hands approximately aligned | `F`     | Forward    |
| ↗️ Hands angled                | `R`     | Right      |
| ↖️ Hands angled                | `L`     | Left       |
| ❌ One/no hand detected         | `S`     | Stop       |

### Serial Commands

```text
F → Forward
B → Backward
L → Left
R → Right
S → Stop
```

The Arduino also supports **Backward** through the `B` command, allowing the system to be extended with a backward gesture in future versions.

---

## 🧠 Computer Vision

The project uses **MediaPipe Hand Landmarker** to detect hands in real time.

Each detected hand contains **21 landmarks**, including:

* Wrist
* Thumb
* Index Finger
* Middle Finger
* Ring Finger
* Pinky

The current Python implementation uses the wrist position of each detected hand.

For two detected hands:

```python
dx = x2 - x1
dy = y2 - y1

angle = math.degrees(math.atan2(dy, dx))
```

The calculated angle is then used to determine whether the car should move:

* Forward
* Left
* Right

If two hands are not detected, the system sends the stop command.

---

## 🛑 Safety Feature

Safety is an important part of the project.

The car automatically receives:

```text
S
```

when:

* No hands are detected.
* Only one hand is detected.
* The camera fails.
* The Python program is closed.

Before exiting the program, Python also sends:

```python
arduino.write(b"S")
```

This helps prevent the car from continuing to move after the program is stopped.

---

## 🛠️ Technologies Used

### Software

* Python
* OpenCV
* MediaPipe
* PySerial
* Math

### Hardware

* Arduino
* L298N Motor Driver
* DC Motors
* Robotic Car Chassis
* Webcam
* USB Serial Communication
* HC Bluetooth module *(supported by Arduino code)*

---

## 🔌 Arduino Pin Configuration

The Arduino uses the following L298N connections:

| Component | Arduino Pin |
| --------- | ----------: |
| ENA       |           6 |
| IN1       |           4 |
| IN2       |           5 |
| ENB       |           9 |
| IN3       |           7 |
| IN4       |           8 |

### Bluetooth

The Arduino uses `SoftwareSerial`:

| Bluetooth | Arduino |
| --------- | ------: |
| RX        |      10 |
| TX        |      11 |

The motor speed is currently set using:

```cpp
analogWrite(ENA, 180);
analogWrite(ENB, 180);
```

---

## 📂 Project Structure

```text
HandDrive/
│
├── car.py
├── car code arduino2.ino
├── hand_landmarker.task
└── README.md
```

### Files

**`car.py`**

Python program responsible for:

* Opening the webcam
* Detecting hands
* Processing MediaPipe landmarks
* Calculating hand angle
* Determining movement direction
* Sending commands to Arduino

**`car code arduino2.ino`**

Arduino program responsible for:

* Receiving commands from Python
* Receiving Bluetooth commands
* Controlling the L298N motor driver
* Moving the robotic car

**`hand_landmarker.task`**

MediaPipe hand landmark model used for hand detection.

---

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/aytenakl/HandDrive.git
```

### 2. Enter the Project Directory

```bash
cd HandDrive
```

### 3. Install Python Dependencies

```bash
pip install opencv-python mediapipe pyserial
```

---

## ▶️ Running the Project

### Step 1 — Connect Arduino

Connect the Arduino to your computer using USB.

### Step 2 — Check the COM Port

Find the COM port assigned to your Arduino.

The current Python code uses:

```python
arduino = serial.Serial("COM16", 9600)
```

If your Arduino appears on another port, change `COM16`:

```python
arduino = serial.Serial("COM5", 9600)
```

### Step 3 — Upload the Arduino Code

Open the Arduino `.ino` file in Arduino IDE and upload it to the board.

Make sure the baud rate is:

```cpp
Serial.begin(9600);
```

### Step 4 — Run Python

```bash
python car.py
```

The webcam will open and begin detecting your hands.

### Step 5 — Control the Car

Move both hands in front of the camera to control the direction.

Press:

```text
Q
```

to close the program.

---

## 📡 Serial Communication

Python and Arduino communicate using **PySerial**.

### Communication Settings

```text
Port: COM16
Baud Rate: 9600
```

### Commands

```text
F → Forward
B → Backward
L → Left
R → Right
S → Stop
```

The Arduino checks both communication channels:

```text
Python / USB Serial
        ↓
     Arduino
        ↑
    Bluetooth
```

This means the same car can receive movement commands through either USB serial communication or Bluetooth.

---

## 🚗 Arduino Motor Control

The Arduino controls the two motors using the L298N motor driver.

### Forward

```text
Left Motor  → Forward
Right Motor → Forward
```

### Backward

```text
Left Motor  → Backward
Right Motor → Backward
```

### Left

```text
Left Motor  → Backward
Right Motor → Forward
```

### Right

```text
Left Motor  → Forward
Right Motor → Backward
```

### Stop

```text
Left Motor  → Stop
Right Motor → Stop
```

---

## 💡 Key Features

* ✋ Real-time hand tracking
* 👁️ Computer vision based control
* 🤖 Robotic car control
* 📐 Hand-angle based steering
* 🔌 Arduino serial communication
* 📡 Bluetooth command support
* 🛑 Automatic stop when hands are lost
* ⚡ Real-time camera processing
* 🧩 Modular Python and Arduino architecture

---

## 🔮 Future Improvements

Possible improvements for future versions:

* ↩️ Add a dedicated backward hand gesture
* ✋ Add more gesture commands
* ⚡ Dynamic speed control
* 📏 Use hand distance to control speed
* 🚧 Add ultrasonic obstacle detection
* 🤖 Add autonomous driving mode
* 📱 Create a mobile Bluetooth controller
* 🎨 Build a graphical user interface
* 📊 Add real-time speed monitoring
* 🎯 Improve gesture stability
* 🧠 Add machine-learning based custom gestures
* 🔄 Add gesture calibration
* 📹 Add project demonstration video

---

## 📸 Demo

A demonstration video and project images can be added here.
<img width="591" height="1280" alt="WhatsApp Image 2026-08-21 at 5 52 31 PM" src="https://github.com/user-attachments/assets/f54803e0-768a-4659-b2d2-89eed509ef72" />
## 🎥 Project Demo

### HandDrive in Action

The following video demonstrates real-time hand gesture control of the robotic car using Computer Vision, MediaPipe, Python, and Arduino.

[▶️ Watch the HandDrive Demo](./handdrive-demo.mp4)
<img width="591" height="1280" alt="handdrive-demo mp4" src="https://github.com/user-attachments/assets/b3714367-09c9-4806-8186-88071214ec25" />
