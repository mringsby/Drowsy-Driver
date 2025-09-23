import cv2 as cv
import numpy as np
import mediapipe as mp

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

# Landmark indices
LEFT_EYE = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33, 160, 158, 133, 153, 144]
MOUTH = [61, 81, 13, 311, 308, 402, 14, 178]

if __name__ == '__main__':
    cap = cv.VideoCapture(0)

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

            cv.imshow('Camera', frame)

            if cv.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv.destroyAllWindows()