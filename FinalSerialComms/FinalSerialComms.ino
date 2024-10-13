#include "arduino_secrets.h"

#include <Wire.h>
#include <Adafruit_MCP4725.h>

// Create DAC objects
Adafruit_MCP4725 dac1;
Adafruit_MCP4725 dac2;

void setup() {
  // Start Serial communication
  Serial.begin(9600);

  // Initialize the DACs
  dac1.begin(0x60); // Address of first MCP4725 DAC
  dac2.begin(0x61); // Address of second MCP4725 DAC
  
  // Confirm initialization
  Serial.println("DACs Initialized");
}

void loop() {
  if (Serial.available() > 0) {
    // Read the incoming serial data
    String input = Serial.readStringUntil('\n');
    
    // Split the input into two values
    int separatorIndex = input.indexOf(',');
    int v1 = input.substring(0, separatorIndex).toInt();
    int v2 = input.substring(separatorIndex + 1).toInt();
    
    // Set the DAC voltages
    setVoltages(v1, v2);
  }
}

void setVoltages(int v1, int v2) {
  dac1.setVoltage((v1 / 5.0) * 4095, false); // Set DAC1 to v1 volts
  dac2.setVoltage((v2 / 5.0) * 4095, false); // Set DAC2 to v2 volts
  Serial.println("Voltage DAC 1: " + String(v1) + "  Voltage DAC 2: " + String(v2));
}