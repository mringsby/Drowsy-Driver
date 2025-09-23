from scipy.spatial import distance as dist

def mouth_aspect_ratio(mouth_points):
    """
    mouth_points: list of 8 (x, y) tuples in order:
    [p1, p2, p3, p4, p5, p6, p7, p8]
    Typically corresponds to outer mouth landmarks.
    """
    x = dist.euclidean(mouth_points[1], mouth_points[7])  # vertical
    y = dist.euclidean(mouth_points[2], mouth_points[6])  # vertical
    z = dist.euclidean(mouth_points[3], mouth_points[5])  # vertical
    w = dist.euclidean(mouth_points[0], mouth_points[4])  # horizontal
    mar = (x + y + z) / (2.0 * w)
    return mar

def compute_mar(landmarks, width, height, mouth_idx):
    mouth = [(int(landmarks[i].x * width), int(landmarks[i].y * height)) for i in mouth_idx]
    return mouth_aspect_ratio(mouth)