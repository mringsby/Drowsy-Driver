import threading
from gpiozero import PWMOutputDevice
import time

# Shared state variable
buzzing = False

# Setup the buzzer (GPIO18 = pin 12)
buzzer = PWMOutputDevice(18, frequency=440, initial_value=0.0)

def buzz_control():
    global buzzing
    while True:
        buzzer.value = 0.5 if buzzing else 0.0

# Start the background thread immediately when this module loads
threading.Thread(target=buzz_control, daemon=True).start()
