import numpy as np

def calculate_angle(a, b, c):
    """
    Calculates the angle between three points (a, b, c), where b is the vertex.
    Uses the dot product of the vectors to calculate the angle.
    """
    a = np.array(a)  # First point
    b = np.array(b)  # Mid point (vertex)
    c = np.array(c)  # End point

    # Calculate vectors from the vertex
    ba = a - b
    bc = c - b

    # Calculate the dot product and magnitudes of the vectors
    dot_product = np.dot(ba, bc)
    norm_ba = np.linalg.norm(ba)
    norm_bc = np.linalg.norm(bc)

    # Calculate the cosine of the angle
    cosine_angle = dot_product / (norm_ba * norm_bc)

    # Calculate the angle in radians and then convert to degrees
    angle = np.arccos(cosine_angle)
    angle_degrees = np.degrees(angle)

    return angle_degrees

def get_angle_color(angle, joint_type):
    """
    Determines the color-coding for an angle based on its value and joint type.
    Returns 'green' for normal, 'yellow' for caution, and 'red' for extreme angles.
    """
    # Define angle ranges for each joint type. These are examples and can be adjusted.
    ranges = {
        "shoulder": {"normal": (0, 180), "caution": (-10, 190), "extreme": (-20, 200)},
        "elbow": {"normal": (0, 180), "caution": (-10, 190), "extreme": (-20, 200)},
        "hip": {"normal": (0, 130), "caution": (-10, 140), "extreme": (-20, 150)},
        "knee": {"normal": (0, 140), "caution": (-10, 150), "extreme": (-20, 160)},
        "ankle": {"normal": (70, 110), "caution": (60, 120), "extreme": (50, 130)}
    }

    if joint_type not in ranges:
        return "white"  # Default color if joint type is unknown

    r = ranges[joint_type]
    if r["normal"][0] <= angle <= r["normal"][1]:
        return "green"
    elif r["caution"][0] <= angle <= r["caution"][1]:
        return "yellow"
    else:
        return "red"

def calculate_left_shoulder_flexion_angle(landmarks):
    """Calculates the left shoulder flexion/extension angle."""
    shoulder = [landmarks[12].x, landmarks[12].y]
    elbow = [landmarks[14].x, landmarks[14].y]
    hip = [landmarks[24].x, landmarks[24].y]
    return calculate_angle(hip, shoulder, elbow)

def calculate_right_shoulder_flexion_angle(landmarks):
    """Calculates the right shoulder flexion/extension angle."""
    shoulder = [landmarks[11].x, landmarks[11].y]
    elbow = [landmarks[13].x, landmarks[13].y]
    hip = [landmarks[23].x, landmarks[23].y]
    return calculate_angle(hip, shoulder, elbow)

def calculate_left_shoulder_abduction_angle(landmarks):
    """Calculates the left shoulder abduction/adduction angle."""
    shoulder = [landmarks[11].x, landmarks[11].y]
    elbow = [landmarks[13].x, landmarks[13].y]
    ear = [landmarks[7].x, landmarks[7].y] # Left ear
    return 180 - calculate_angle(ear, shoulder, elbow)

def calculate_right_shoulder_abduction_angle(landmarks):
    """Calculates the right shoulder abduction/adduction angle."""
    shoulder = [landmarks[12].x, landmarks[12].y]
    elbow = [landmarks[14].x, landmarks[14].y]
    ear = [landmarks[8].x, landmarks[8].y] # Right ear
    return 180 - calculate_angle(ear, shoulder, elbow)

def calculate_left_elbow_angle(landmarks):
    """Calculates the left elbow flexion/extension angle."""
    shoulder = [landmarks[11].x, landmarks[11].y]
    elbow = [landmarks[13].x, landmarks[13].y]
    wrist = [landmarks[15].x, landmarks[15].y]
    return 180 - calculate_angle(shoulder, elbow, wrist)

def calculate_right_elbow_angle(landmarks):
    """Calculates the right elbow flexion/extension angle."""
    shoulder = [landmarks[12].x, landmarks[12].y]
    elbow = [landmarks[14].x, landmarks[14].y]
    wrist = [landmarks[16].x, landmarks[16].y]
    return 180 - calculate_angle(shoulder, elbow, wrist)

def calculate_left_hip_angle(landmarks):
    """Calculates the left hip flexion/extension angle."""
    shoulder = [landmarks[12].x, landmarks[12].y]
    hip = [landmarks[24].x, landmarks[24].y]
    knee = [landmarks[26].x, landmarks[26].y]
    return 180 - calculate_angle(shoulder, hip, knee)

def calculate_right_hip_angle(landmarks):
    """Calculates the right hip flexion/extension angle."""
    shoulder = [landmarks[11].x, landmarks[11].y]
    hip = [landmarks[23].x, landmarks[23].y]
    knee = [landmarks[25].x, landmarks[25].y]
    return 180 - calculate_angle(shoulder, hip, knee)

def calculate_left_knee_angle(landmarks):
    """Calculates the left knee flexion/extension angle."""
    hip = [landmarks[24].x, landmarks[24].y]
    knee = [landmarks[26].x, landmarks[26].y]
    ankle = [landmarks[28].x, landmarks[28].y]
    return 180 - calculate_angle(hip, knee, ankle)

def calculate_right_knee_angle(landmarks):
    """Calculates the right knee flexion/extension angle."""
    hip = [landmarks[23].x, landmarks[23].y]
    knee = [landmarks[25].x, landmarks[25].y]
    ankle = [landmarks[27].x, landmarks[27].y]
    return 180 - calculate_angle(hip, knee, ankle)

def calculate_left_ankle_angle(landmarks):
    """Calculates the left ankle dorsiflexion/plantarflexion angle."""
    knee = [landmarks[26].x, landmarks[26].y]
    ankle = [landmarks[28].x, landmarks[28].y]
    foot_index = [landmarks[32].x, landmarks[32].y] # Left foot index
    return calculate_angle(knee, ankle, foot_index) - 90

def calculate_right_ankle_angle(landmarks):
    """Calculates the right ankle dorsiflexion/plantarflexion angle."""
    knee = [landmarks[25].x, landmarks[25].y]
    ankle = [landmarks[27].x, landmarks[27].y]
    foot_index = [landmarks[31].x, landmarks[31].y] # Right foot index
    return calculate_angle(knee, ankle, foot_index) - 90