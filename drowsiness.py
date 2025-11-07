import cv2 as cv
import time
from gpiozero import PWMOutputDevice
from time import sleep
from log import log_change

BPM_1 = 20  # Blinks per minute threshold for drowsiness lvl 1
PERCLOS_1 = 7.5  # PERCLOS threshold for drowsiness lvl 1

BPM_2 = 20  # Blinks per minute threshold for drowsiness lvl 2
PERCLOS_L_2 = 7.5  # PERCLOS threshold for drowsiness lvl 2
PERCLOS_H_2 = 10.0  # PERCLOS threshold for drowsiness lvl 2

BPM_3 = 20 # Blinks per minute threshold for drowsiness lvl 3
PERCLOS_3 = 10.0 # PERCLOS threshold for drowsiness lvl 3
YPM_3 = 0  # Yawns per minute threshold for drowsiness lvl 3
MCD_3 = 0.4 # Maximum Closure Duration threshold for drowsiness lvl 3 (in seconds)

BPM_4 = 25 # Blinks per minute threshold for drowsiness lvl 4
PERCLOS_4 = 10.0 # PERCLOS threshold for drowsiness lvl 4
YPM_4 = 0.5  # Yawns per minute threshold for drowsiness lvl 4
MCD_4 = 1.0 # Maximum Closure Duration threshold for drowsiness lvl 4 (in seconds)

BPM_5 = 25 # Blinks per minute threshold for drowsiness lvl 5
PERCLOS_5 = 12.0 # PERCLOS threshold for drowsiness lvl 5
YPM_5 = 1.0 # Yawns per minute threshold for drowsiness lvl 5
MCD_5 = 2.0 # Maximum Closure Duration threshold for drowsiness lvl 5 (in seconds)



class DrowsinessDetector:
    def __init__(self, ear_threshold=0.20, consec_frames=15, blink_threshold=0.17, blink_reset_threshold=0.19, mar_threshold=0.60, yawn_consec_frames=15):

        #Thresholds
        self.EAR_THRESHOLD = ear_threshold
        self.CONSEC_FRAMES = consec_frames
        self.BLINK_THRESHOLD = blink_threshold
        self.BLINK_RESET_THRESHOLD = blink_reset_threshold
        self.MAR_THRESHOLD = mar_threshold
        self.YAWN_CONSEC_FRAMES = yawn_consec_frames
        self.LVL_HELPER = 0
        self.TMP_DROWSY_LVL = 0

        # Counters and helper variables
        self.eye_closed_counter = 0
        self.blink_reset = True
        self.start_time = time.time()
        self.print_counter = 0
        self.yawn_frame_counter = 0
        self.yawn_reset = True
        self.eye_closed_print = True
        self.mcd_reset = 5
        self.buzzer_active = False

        # Metrics
        self.maximum_closure_duration = 0 # max times eyes were closed in seconds
        self.blink_frequency = 0 # blinks per minute
        self.yawn_frequency = 0 # yawns per minute
        self.yawn_counter = 0 # total yawns
        self.blink_counter = 0 # total blinks

        # Drowsiness level
        self.drowsy_lvl = 1
        self.buzzer = PWMOutputDevice(18)

    def calculate_drowsy_lvl(self, ear, mar, perclos):

        self.set_eye_metrics(ear)
        self.set_yawn_frequency(mar)

        if self.TMP_DROWSY_LVL < 5:
            self.LVL_HELPER = 0
            if self.blink_frequency >= BPM_5:
                self.LVL_HELPER += 1
            if perclos > PERCLOS_5:
                self.LVL_HELPER += 1
            if self.yawn_frequency >= YPM_5:
                self.LVL_HELPER += 1
            if self.maximum_closure_duration >= MCD_5:
                self.LVL_HELPER += 1
            if self.LVL_HELPER >= 3:
                self.TMP_DROWSY_LVL = 5
                self.buzzer.frequency = 600
                self.buzzer.value = 0.5
                log_change("Buzzer active", "ON (Level 5)")
                self.buzzer_active = True

        if self.TMP_DROWSY_LVL < 4:
            self.LVL_HELPER = 0
            if self.blink_frequency >= BPM_4:
                self.LVL_HELPER += 1
            if perclos > PERCLOS_4:
                self.LVL_HELPER += 1
            if self.yawn_frequency >= YPM_4:
                self.LVL_HELPER += 1
            if self.maximum_closure_duration >= MCD_4:
                self.LVL_HELPER += 1
            if self.LVL_HELPER >= 3:
                self.TMP_DROWSY_LVL = 4
                self.buzzer.frequency = 600
                self.buzzer.value = 0.5
                log_change("Buzzer active", "ON (Level 4)")
                self.buzzer_active = True

        if self.TMP_DROWSY_LVL < 3:
            self.LVL_HELPER = 0
            if self.blink_frequency > BPM_3:
                self.LVL_HELPER += 1
            if perclos > PERCLOS_3:
                self.LVL_HELPER += 1
            if self.yawn_frequency > YPM_3:
                self.LVL_HELPER += 1
            if self.maximum_closure_duration >= MCD_3:
                self.LVL_HELPER += 1
            if self.LVL_HELPER >= 3:
                self.TMP_DROWSY_LVL = 3

        if self.TMP_DROWSY_LVL < 2:
            self.LVL_HELPER = 0
            if self.blink_frequency > BPM_2:
                self.LVL_HELPER += 1
            if PERCLOS_L_2 < perclos <= PERCLOS_H_2:
                self.LVL_HELPER += 1
            if self.LVL_HELPER >= 1:
                self.TMP_DROWSY_LVL = 2

        if self.TMP_DROWSY_LVL < 1:
            self.LVL_HELPER = 0
            if self.blink_frequency <= BPM_1:
                self.LVL_HELPER += 1
            if perclos <= PERCLOS_1:
                self.LVL_HELPER += 1
            if self.LVL_HELPER <= 2:
                self.TMP_DROWSY_LVL = 1

        self.drowsy_lvl = self.TMP_DROWSY_LVL
        self.TMP_DROWSY_LVL = 0

        elapsed_minutes = (time.time() - self.start_time) / 60
        if elapsed_minutes > self.print_counter:
            print(f"\n--- Drowsiness Metrics after {elapsed_minutes:.2f} minutes ---")
            print(f"Blink Frequency: {self.blink_frequency} per minute")
            print(f"Yawn Frequency: {self.yawn_frequency} per minute")
            print(f"Maximum Eye Closure Duration: {self.maximum_closure_duration:.2f} seconds")
            print(f"PERCLOS: {perclos:.2f}%")
            print(f"Drowsiness Level Assessment: {self.drowsy_lvl}")
            print(f"--- End of Metrics ---\n")
            self.print_counter += 1
            if self.print_counter == self.mcd_reset: #reset maximum closure duration every 5 minutes
                self.maximum_closure_duration = 0 # reset max closure duration for next interval
                self.mcd_reset += 5 # increment reset timer by another 5 minutes


        return

    def set_eye_metrics(self, ear):
        if ear < self.EAR_THRESHOLD:
            self.eye_closed_counter += 1
            if self.eye_closed_counter >= self.CONSEC_FRAMES:
                if self.eye_closed_print:
                    print("Warning: Eyes closed!")
                    self.buzzer.frequency = 600
                    self.buzzer.value = 0.5
                    self.eye_closed_print = False
                    log_change("Buzzer active", "ON (Eyes closed)")
                    self.buzzer_active = True

            if ear < self.BLINK_THRESHOLD and self.blink_reset:
                self.blink_counter += 1
                self.blink_reset = False

            if ear >= self.BLINK_RESET_THRESHOLD:
                self.blink_reset = True
                self.buzzer.off()
                if self.buzzer_active:
                    log_change("Buzzer deactivated", "OFF (Blink reset)")
                    self.buzzer_active = False
        else:
            if self.eye_closed_counter / 30 > self.maximum_closure_duration:
                self.maximum_closure_duration = self.eye_closed_counter / 30
                print(f"New max eye closure duration: {self.maximum_closure_duration:.2f} seconds")

            self.eye_closed_counter = 0
            self.blink_reset = True
            self.eye_closed_print = True

            if self.drowsy_lvl < 4:
                self.buzzer.off()
                if self.buzzer_active:
                    log_change("Buzzer deactivated", "OFF (Blink reset)")
                    self.buzzer_active = False

        elapsed_minutes = (time.time() - self.start_time) / 60
        if elapsed_minutes > 0:
            self.blink_frequency = self.blink_counter / elapsed_minutes
        return

    def set_yawn_frequency(self, mar):
        if mar > self.MAR_THRESHOLD:
            self.yawn_frame_counter += 1
            if self.yawn_frame_counter >= self.YAWN_CONSEC_FRAMES:
                if self.yawn_reset:
                    self.yawn_counter += 1
                    print(f"Yawn detected! Total yawns: {self.yawn_counter}")
                    self.yawn_reset = False
        else:
            self.yawn_frame_counter = 0
            self.yawn_reset = True

        elapsed_minutes = (time.time() - self.start_time) / 60
        if elapsed_minutes > 0:
            self.yawn_frequency = self.yawn_counter / elapsed_minutes
        return

    def get_blink_count(self):
        return self.blink_counter

    def get_max_closure_duration(self):
        return self.maximum_closure_duration

    def get_yawn_count(self):
        return self.yawn_counter

    def get_drowsy_level(self):
        """Return current drowsiness level (1–5)."""
        return self.drowsy_lvl
