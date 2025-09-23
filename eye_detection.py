from scipy.spatial import distance as dist

def eye_aspect_ratio(eye_points):
    """
    eye_points: list of 6 (x, y) tuples in order:
    [p1, p2, p3, p4, p5, p6]
    """
    x = dist.euclidean(eye_points[1], eye_points[5])  # vertical
    y = dist.euclidean(eye_points[2], eye_points[4])  # vertical
    z = dist.euclidean(eye_points[0], eye_points[3])  # horizontal
    ear = (x + y) / (2.0 * z)
    return ear

# Wrapper to calculate EAR given landmarks + indices
def compute_ear(landmarks, width, height, left_eye_idx, right_eye_idx):
    left_eye = [(int(landmarks[i].x * width), int(landmarks[i].y * height)) for i in left_eye_idx]
    right_eye = [(int(landmarks[i].x * width), int(landmarks[i].y * height)) for i in right_eye_idx]

    leftEAR = eye_aspect_ratio(left_eye)
    rightEAR = eye_aspect_ratio(right_eye)
    return (leftEAR + rightEAR) / 2.0