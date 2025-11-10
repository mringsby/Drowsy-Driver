# Drowsy Driver - Final Release

A real-time drowsiness detection demo using computer vision to monitor eye blinks, yawns, and eye closure patterns to determine users drowsiness-level 1-5 and alert if user is too drowsy.

## Requirements & Installation

### **Python 3.11 required**

### Powershell first time installation

1. Clone the repository:
   ```bash
   git clone https://github.com/mringsby/Drowsy-Driver.git
   ```
2. Move to project directory:
   ```
   cd Drowsy-Driver
   ```
3. Move to Final-Release branch:
   ```
   git checkout Final-Release
   ```
4. Create virtual environment:
   ```
   py -3.11 -m venv venv
   ```
5. Activate venv, install dependencies, and run program (This will take some time, be patient)
   ```
   powershell -ExecutionPolicy Bypass -Command "& .\venv\Scripts\Activate.ps1; pip install -r requirements.txt; python main.py"
   ```

### Run program with Powershell after install
1. Move to project directory:
   ```
   cd Drowsy-Driver
   ```
2. Move to Final-Release branch:
   ```
   git checkout Final-Release
   ```
3. Activate venv and run:
   ```
   powershell -ExecutionPolicy Bypass -Command "& .\venv\Scripts\Activate.ps1; python main.py"
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
- **Drowsiness Level 1-5**: Indicator to show what drowsiness level the user currently is on
