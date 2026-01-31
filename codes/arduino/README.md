#Arduino Deployment Guide
This guide outlines the steps to compile the project using PlatformIO and upload the firmware to the Arduino board.  
##Prerequisites
PlatformIO: Ensure PlatformIO is installed to manage the project build.
Arduino IDE: Required for the final upload step.
Hardware: Arduino UNO connected to the computer via USB.  

Project Initialization

1. Create and initialize the project directory: 
```bash
mkdir pt100_project
cd pt100_project
pio project init --board uno

2. Install the required Arduino libraries for the LCD and ADC:  
```bash

pio lib install "LiquidCrystal"
pio lib install "Adafruit ADS1X15"
```
