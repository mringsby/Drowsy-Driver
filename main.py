import cv2 as cv
import numpy as np
import mediapipe as mp
from eye_detection import compute_ear, PERCLOS
from yawn_detection import compute_mar
from drowsiness import DrowsinessDetector
import collections


# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

# Landmark indices
LEFT_EYE = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33, 160, 158, 133, 153, 144]
MOUTH = [61, 81, 13, 311, 308, 402, 14, 178]

# EAR thresholds
EAR_THRESHOLD = 0.20
CONSEC_FRAMES = 15

EAR_HISTORY_SIZE = 1800  # Number of frames to keep in history for PERCLOS 60 seconds at 30 FPS
ear_history = collections.deque(maxlen=EAR_HISTORY_SIZE)

# Blink threshold
BLINK_THRESHOLD = 0.17
BLINK_RESET_THRESHOLD = 0.19

# MAR thresholds
MAR_THRESHOLD = 0.60
YAWN_CONSEC_FRAMES = 30

if __name__ == '__main__':
    cap = cv.VideoCapture(0)
    cap.set(cv.CAP_PROP_FPS, 30)

    drowsiness_detector = DrowsinessDetector(EAR_THRESHOLD, CONSEC_FRAMES, BLINK_THRESHOLD, BLINK_RESET_THRESHOLD, MAR_THRESHOLD, YAWN_CONSEC_FRAMES)

    with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as face_mesh:

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            results = face_mesh.process(rgb_frame)

            if results.multi_face_landmarks:
                landmarks = results.multi_face_landmarks[0].landmark
                h, w, _ = frame.shape

                # Draw eye points
                for idx in LEFT_EYE + RIGHT_EYE:
                    x = int(landmarks[idx].x * w)
                    y = int(landmarks[idx].y * h)
                    cv.circle(frame, (x, y), 2, (0, 255, 0), -1)

                # Draw mouth points
                for idx in MOUTH:
                    x = int(landmarks[idx].x * w)
                    y = int(landmarks[idx].y * h)
                    cv.circle(frame, (x, y), 2, (255, 0, 0), -1)

                # EAR from imported function
                ear = compute_ear(landmarks, w, h, LEFT_EYE, RIGHT_EYE)

                # MAR calculation
                mar = compute_mar(landmarks, w, h, MOUTH)

                ear_history.append(ear)

                # Calculate PERCLOS
                perclos = 0
                if len(ear_history) == EAR_HISTORY_SIZE:
                    perclos = PERCLOS(ear_history, EAR_HISTORY_SIZE)

                # Drowsiness logic
                drowsiness_detector.calculate_drowsy_lvl(ear, mar, perclos)

                # Show EAR value
                cv.putText(frame, f"EAR: {ear:.2f}", (30, 30),
                           cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

                # show blink count
                cv.putText(frame, f"Blinks: {drowsiness_detector.get_blink_count()}", (30, 70),
                           cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

                # Warning for yawning
                if mar > MAR_THRESHOLD:
                    cv.putText(frame, "YAWN DETECTED!", (200, 30),
                               cv.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), 3)

                # Show MAR value
                cv.putText(frame, f"MAR: {mar:.2f}", (30, 110),
                           cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

                # show yawn count
                cv.putText(frame, f"Yawns: {drowsiness_detector.get_yawn_count()}", (30, 150),
                           cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

                # show PERCLOS only if we have enough history
                if len(ear_history) == EAR_HISTORY_SIZE:
                    cv.putText(frame, f"PERCLOS: {perclos:.2f}%", (30, 190),
                               cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

            # only ONE imshow + waitKey
            cv.imshow("Camera", frame)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv.destroyAllWindows()
