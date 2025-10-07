# Drowsy Driver - Demo Release/First Release

A real-time drowsiness detection demo using computer vision to monitor eye blinks, yawns, and eye closure patterns.

## Requirements & Installation

### **Python 3.11 required**

1. Clone the repository:
   ```bash
   git clone https://github.com/mringsby/Drowsy-Driver.git```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the demo:
   ```bash
   python main.py
   ```

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

## Demo Features

- Real-time face landmark detection
- Eye closure warnings
- Yawn detection alerts
- Drowsiness metrics
