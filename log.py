import os
from datetime import datetime

# global state
log_entries = []
previous_values = {
    "EAR": None,
    "MAR": None,
    "PERCLOS": None,
    "BLINKS": 0,
    "YAWNS": 0,
    "MAX_CLOSURE_DURATION": 0.0,
    "DROWSINESS_LEVEL": None
}

def log_change(label, value):
    """Log when a value changes with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entries.append(f"[{timestamp}] {label} changed to {value}")

def save_logs_to_file():
    """Write all collected logs to a file inside the 'logs' folder."""
    # Define logs folder path
    log_folder = "logs"
    os.makedirs(log_folder, exist_ok=True)

    # Create unique file name
    filename = datetime.now().strftime("drowsiness_log_%Y%m%d_%H%M%S.txt")
    file_path = os.path.join(log_folder, filename)

    # Write log entries
    with open(file_path, "w") as f:
        for entry in log_entries:
            f.write(entry + "\n")

    print(f"\nLog saved to: {file_path}")

def get_previous_values():
    return previous_values
