# Drowsy Driver - Final Release (raspberry pi version)

A real-time drowsiness detection demo using computer vision to monitor eye blinks, yawns, and eye closure patterns to determine users drowsiness-level 1-5 and alert if user is too drowsy. This version is for running on raspberry pi. Buzzer should be on pin 9(ground) and 12, part: ps1240. For testing on pc checkout branch Final-Release.

## Requirements

- **Raspberry Pi OS Legacy 64-bit (Debian Bookworm)** - comes with Python 3.11 pre-installed
- **Raspberry Pi Camera Module** v3
- **Buzzer (ps1240)** connected to GPIO pins 9 (ground) and 12

## Installation

### Step 1: Verify Python 3.11
Bookworm comes with Python 3.11 by default. Verify:
```bash
python3 --version
```
You should see `Python 3.11.x`.

### Step 2: Verify libcamera is installed
```bash
libcamera-hello --list-cameras
```
If you see your camera listed, libcamera is working. If not, update your system:
```bash
sudo apt update
sudo apt upgrade
```

### Step 3: Clone the repository
```bash
cd ~
git clone https://github.com/yourusername/Drowsy-Driver.git
cd Drowsy-Driver
```

### Step 4: Create virtual environment
```bash
python3 -m venv venv
```

### Step 5: Activate virtual environment
```bash
source venv/bin/activate
```
You should see `(venv)` appear in your terminal prompt.

### Step 6: Upgrade pip
```bash
pip install --upgrade pip
```

### Step 7: Install Python dependencies
```bash
pip install -r requirements.txt
pip install picamera2
pip install gpiozero
```

## Running the Application

### Step 1: Navigate to project directory
```bash
cd ~/Drowsy-Driver
```

### Step 2: Activate virtual environment
```bash
source venv/bin/activate
```

### Step 3: Run the application
```bash
python main.py
```

### Step 4: Monitor and control
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

### Buzzer Alerts
- Activates when drowsiness level reaches 4 or 5
- Activates when user closes eyes for more than 0.5 seconds


