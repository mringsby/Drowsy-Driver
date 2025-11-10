# Drowsy Driver - Final Release (raspberry pi version)

A real-time drowsiness detection demo using computer vision to monitor eye blinks, yawns, and eye closure patterns to determine users drowsiness-level 1-5 and alert if user is too drowsy. This version is for running on raspberry pi. Buzzer should be on pin 9(ground) and 12, part: ps1240. For testing on pc checkout branch Final-Release.

## Requirements & Installation

### **PI OS Legacy 64-bit (debian bookworm) required**

### First time installation
1. Make sure libcamera is installed
2. 


## Usage

- Position yourself in front of the camera
- Press 'q' to quit
- Monitor real-time metrics on screen and console output every 1 minute

## Metrics Displayed

### Real-time Visual Metrics (On Screen)
- **EAR (Eye Aspect Ratio)**: Current eye openness level for blink detection
- **MAR (Mouth Aspect Ratio)**: Current mouth openness level for yawn detection
- **PERCLOS**: Percentage of eye closure over the last 60 seconds
- **Blink Counter**: Total number of blinks detected since start
- **Yawn Counter**: Total number of yawns detected since start
- **Visual Alerts**: "YAWN DETECTED!" warning when yawning occurs

### Console Output Metrics (Every 1 Minute)
- **Blink Frequency**: Average blinks per minute
- **Yawn Frequency**: Average yawns per minute  
- **Maximum Eye Closure Duration**: Longest continuous period eyes were closed (in seconds)
- **PERCLOS Percentage**: Drowsiness indicator based on eye closure time over 60-second window
- **Drowsiness Level 1-5**: Indicator to show what drowsiness level the user currently is on
