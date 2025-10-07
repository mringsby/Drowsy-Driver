import cv2 as cv
import time

class DrowsinessDetector:
    def __init__(self, ear_threshold=0.20, consec_frames=15, blink_threshold=0.17, blink_reset_threshold=0.19, mar_threshold=0.60, yawn_consec_frames=30):

        #Thresholds
        self.EAR_THRESHOLD = ear_threshold
        self.CONSEC_FRAMES = consec_frames
        self.BLINK_THRESHOLD = blink_threshold
        self.BLINK_RESET_THRESHOLD = blink_reset_threshold
        self.MAR_THRESHOLD = mar_threshold
        self.YAWN_CONSEC_FRAMES = yawn_consec_frames

        # Counters and helper variables
        self.eye_closed_counter = 0
        self.blink_reset = True
        self.start_time = time.time()
        self.print_counter = 0
        self.yawn_frame_counter = 0
        self.yawn_reset = True
        self.eye_closed_print = True

        # Metrics
        self.maximum_closure_duration = 0 # max times eyes were closed in seconds
        self.blink_frequency = 0 # blinks per minute
        self.yawn_frequency = 0 # yawns per minute
        self.yawn_counter = 0 # total yawns
        self.blink_counter = 0 # total blinks

    def calculate_drowsy_lvl(self, ear, mar, perclos):

        self.set_eye_metrics(ear)
        self.set_yawn_frequency(mar)

        elapsed_minutes = (time.time() - self.start_time) / 60
        if elapsed_minutes > self.print_counter:
            print(f"\n--- Drowsiness Metrics after {elapsed_minutes:.2f} minutes ---")
            print(f"Blink Frequency: {self.blink_frequency} per minute")
            print(f"Yawn Frequency: {self.yawn_frequency} per minute")
            print(f"Maximum Eye Closure Duration: {self.maximum_closure_duration:.2f} seconds")
            print(f"PERCLOS: {perclos:.2f}%")
            print(f"--- End of Metrics ---\n")
            self.print_counter += 1

        return

    def set_eye_metrics(self, ear):
        if ear < self.EAR_THRESHOLD:
            self.eye_closed_counter += 1
            if self.eye_closed_counter >= self.CONSEC_FRAMES:
                if self.eye_closed_print:
                    print("Warning: Eyes closed!")
                    self.eye_closed_print = False

            if ear < self.BLINK_THRESHOLD and self.blink_reset:
                self.blink_counter += 1
                self.blink_reset = False

            if ear >= self.BLINK_RESET_THRESHOLD:
                self.blink_reset = True
        else:
            if self.eye_closed_counter / 30 > self.maximum_closure_duration:
                self.maximum_closure_duration = self.eye_closed_counter / 30
                print(f"New max eye closure duration: {self.maximum_closure_duration:.2f} seconds")

            self.eye_closed_counter = 0
            self.blink_reset = True
            self.eye_closed_print = True

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
