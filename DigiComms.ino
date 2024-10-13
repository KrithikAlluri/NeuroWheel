#include "arduino_secrets.h"

#include <Wire.h>
#include <Adafruit_MCP4725.h>

Adafruit_MCP4725 dac1;
Adafruit_MCP4725 dac2;
// Define the pins for reading signals from Raspberry Pi
const int leftMotorPowerPin = 2;     // Arduino pin to receive left motor power signal
const int rightMotorPowerPin = 3;    // Arduino pin to receive right motor power signal
const int leftMotorDirectionPin = 4; // Arduino pin to receive left motor direction signal
const int rightMotorDirectionPin = 5; // Arduino pin to receive right motor direction signalial.begin(9600);


void loop() {
  // Read the digital signals from Raspberry Pi
  

  // Debugging: Print the status to serial monitor
  Serial.print("Left Power: ");
  Serial.print(leftPower ? "ON" : "OFF");
  Serial.print(" | Left Direction: ");
  Serial.print(leftDirection ? "FORWARD" : "BACKWARD");
  Serial.print(" | Right Power: ");
  Serial.print(rightPower ? "ON" : "OFF");
  Serial.print(" | Right Direction: ");
  Serial.println(rightDirection ? "FORWARD" : "BACKWARD");

  // Based on the received signals, control the motors here
  // (Implementation depends on how your motors are wired)

  delay(500); // Small delay to avoid flooding the serial output
}
void setup(void) {
  Serial.begin(9600);
  Serial.println("MCP4725 Dual Module Test");
// Set pins as input
  pinMode(leftMotorPowerPin, INPUT);
  pinMode(rightMotorPowerPin, INPUT);
  pinMode(leftMotorDirectionPin, INPUT);
  pinMode(rightMotorDirectionPin, INPUT);

  // Initialize the first DAC at address 0x60
  if (!dac1.begin(0x60)) {
    Serial.println("Failed to find DAC1 at 0x60");
    while (1);
  }

  // Initialize the second DAC at address 0x61
  if (!dac2.begin(0x61)) {
    Serial.println("Failed to find DAC2 at 0x61");
    while (1);
  }
}

void setVoltages(int v1, int v2) {
  dac1.setVoltage((v1 / 5.0) * 4095, false); // Set DAC1 to v1 volts
  dac2.setVoltage((v2 / 5.0) * 4095, false); // Set DAC2 to v2 volts
  Serial.println("Voltage DAC 1: " + String(v1) + "  Voltage DAC 2: " + String(v2));
}

void loop() {
  // Read the digital signals from Raspberry Pi
  bool leftPower = digitalRead(leftMotorPowerPin);
  bool rightPower = digitalRead(rightMotorPowerPin);
  bool leftDirection = digitalRead(leftMotorDirectionPin);
  bool rightDirection = digitalRead(rightMotorDirectionPin);

  // Determine voltages for the left and right motors
  float leftVoltage = 2.5;  // Default is neutral
  float rightVoltage = 2.5; // Default is neutral

  // Set voltage for left motor based on power and direction
  if (leftPower) {
    if (leftDirection) {
      leftVoltage = 4.5;  // Full forward
    } else {
      leftVoltage = 0.5;  // Full backward
    }
  }

  // Set voltage for right motor based on power and direction
  if (rightPower) {
    if (rightDirection) {
      rightVoltage = 4.5;  // Full forward
    } else {
      rightVoltage = 0.5;  // Full backward
    }
  }

  // Apply the calculated voltages
  setVoltages(leftVoltage, rightVoltage);

  delay(500);
}