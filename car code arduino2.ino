#include <SoftwareSerial.h>

// ==================== L298N Motor Driver Pins ====================

#define ENA 6
#define IN1 4
#define IN2 5

#define ENB 9
#define IN3 7
#define IN4 8

// ==================== Bluetooth ====================

SoftwareSerial bluetooth(10, 11);
// Arduino RX = 10
// Arduino TX = 11


void setup() {

  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);

  pinMode(ENB, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  analogWrite(ENA, 180);
  analogWrite(ENB, 180);

  // USB Serial - Python
  Serial.begin(9600);

  // Bluetooth
  bluetooth.begin(9600);

  stopCar();
}


void loop() {

  // ==================== Python / USB ====================

  if (Serial.available() > 0) {

    char command = Serial.read();

    if (command == 'F') {
      forward();
    }

    else if (command == 'B') {
      backward();
    }

    else if (command == 'L') {
      turnLeft();
    }

    else if (command == 'R') {
      turnRight();
    }

    else if (command == 'S') {
      stopCar();
    }
  }


  // ==================== Bluetooth ====================

  if (bluetooth.available() > 0) {

    char command = bluetooth.read();

    if (command == 'F') {
      forward();
    }

    else if (command == 'B') {
      backward();
    }

    else if (command == 'L') {
      turnLeft();
    }

    else if (command == 'R') {
      turnRight();
    }

    else if (command == 'S') {
      stopCar();
    }
  }
}


// ==================== Forward ====================

void forward() {

  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);

  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
}


// ==================== Backward ====================

void backward() {

  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);

  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
}


// ==================== Left ====================

void turnLeft() {

  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);

  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
}


// ==================== Right ====================

void turnRight() {

  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);

  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
}


// ==================== Stop ====================

void stopCar() {

  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);

  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
}