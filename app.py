from flask import Flask, render_template, Response, request, jsonify
import cv2
import csv
from datetime import datetime

import cv2
import mediapipe as mp
import numpy as np
import csv
from datetime import datetime
from flask import Flask, render_template, Response, request

from pose_detector import PoseDetector
from angle_calculator import (
    calculate_left_shoulder_flexion_angle,
    calculate_right_shoulder_flexion_angle,
    calculate_left_shoulder_abduction_angle,
    calculate_right_shoulder_abduction_angle,
    calculate_left_elbow_angle,
    calculate_right_elbow_angle,
    calculate_left_hip_angle,
    calculate_right_hip_angle,
    calculate_left_knee_angle,
    calculate_right_knee_angle,
    calculate_left_ankle_angle,
    calculate_right_ankle_angle
)

app = Flask(__name__)

# Define a mapping from joint identifiers to MediaPipe landmark indices
# This map is used to determine which landmarks are associated with each joint
# and will be crucial for conditional drawing and angle calculation.
JOINT_LANDMARK_MAP = {
    "left_shoulder_flexion": [mp.solutions.pose.PoseLandmark.LEFT_HIP.value, mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value, mp.solutions.pose.PoseLandmark.LEFT_ELBOW.value],
    "right_shoulder_flexion": [mp.solutions.pose.PoseLandmark.RIGHT_HIP.value, mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value, mp.solutions.pose.PoseLandmark.RIGHT_ELBOW.value],
    "left_shoulder_abduction": [mp.solutions.pose.PoseLandmark.LEFT_EAR.value, mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value, mp.solutions.pose.PoseLandmark.LEFT_ELBOW.value],
    "right_shoulder_abduction": [mp.solutions.pose.PoseLandmark.RIGHT_EAR.value, mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value, mp.solutions.pose.PoseLandmark.RIGHT_ELBOW.value],
    "left_elbow": [mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value, mp.solutions.pose.PoseLandmark.LEFT_ELBOW.value, mp.solutions.pose.PoseLandmark.LEFT_WRIST.value],
    "right_elbow": [mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value, mp.solutions.pose.PoseLandmark.RIGHT_ELBOW.value, mp.solutions.pose.PoseLandmark.RIGHT_WRIST.value],
    "left_hip": [mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value, mp.solutions.pose.PoseLandmark.LEFT_HIP.value, mp.solutions.pose.PoseLandmark.LEFT_KNEE.value],
    "right_hip": [mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value, mp.solutions.pose.PoseLandmark.RIGHT_HIP.value, mp.solutions.pose.PoseLandmark.RIGHT_KNEE.value],
    "left_knee": [mp.solutions.pose.PoseLandmark.LEFT_HIP.value, mp.solutions.pose.PoseLandmark.LEFT_KNEE.value, mp.solutions.pose.PoseLandmark.LEFT_ANKLE.value],
    "right_knee": [mp.solutions.pose.PoseLandmark.RIGHT_HIP.value, mp.solutions.pose.PoseLandmark.RIGHT_KNEE.value, mp.solutions.pose.PoseLandmark.RIGHT_ANKLE.value],
    "left_ankle": [mp.solutions.pose.PoseLandmark.LEFT_KNEE.value, mp.solutions.pose.PoseLandmark.LEFT_ANKLE.value, mp.solutions.pose.PoseLandmark.LEFT_FOOT_INDEX.value],
    "right_ankle": [mp.solutions.pose.PoseLandmark.RIGHT_KNEE.value, mp.solutions.pose.PoseLandmark.RIGHT_ANKLE.value, mp.solutions.pose.PoseLandmark.RIGHT_FOOT_INDEX.value]
}

# Initialize PoseDetector
detector = PoseDetector()

# Global variables for video feed and angle tracking
last_frame = None
last_angles = {}
max_angles = {} # Global dictionary to store max angles
active_joints = list(JOINT_LANDMARK_MAP.keys()) # Initialize with all joints active

# Constants
VISIBILITY_THRESHOLD = 0.7
VIEW_THRESHOLD = 0.1 # Threshold for determining frontal vs. sagittal body view (shoulder x-difference)

# Function to check if all required landmarks are visible
def are_landmarks_visible(landmarks, indices):
    for index in indices:
        if landmarks[index].visibility < VISIBILITY_THRESHOLD:
            return False
    return True

def generate_frames():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    global last_frame, last_angles, max_angles

    while True:
        success, frame = cap.read()
        if not success:
            break

        # Find pose and draw landmarks, conditionally based on active_joints
        frame = detector.find_pose(frame, active_joints, JOINT_LANDMARK_MAP)
        landmarks = detector.results.pose_landmarks

        current_angles = {}
        if landmarks and len(landmarks.landmark) > 30: # Ensure all necessary landmarks are present
            # Determine view (frontal or sagittal)
            left_shoulder_x = landmarks.landmark[12].x
            right_shoulder_x = landmarks.landmark[11].x
            
            # Calculate the absolute difference in x-coordinates of shoulders
            shoulder_x_diff = abs(left_shoulder_x - right_shoulder_x)

            is_frontal_view = shoulder_x_diff > VIEW_THRESHOLD

            # Shoulder Flexion/Abduction (Conditional based on view)
            if not is_frontal_view: # If not frontal, it's sagittal
                # Display Flexion/Extension in sagittal view
                if "right_shoulder_flexion" in active_joints and are_landmarks_visible(landmarks.landmark, [23, 11, 13]): # Anatomical RIGHT landmarks
                    current_angles["right_shoulder_flexion"] = calculate_right_shoulder_flexion_angle(landmarks.landmark) # Assign to internal 'left' for display as 'Right'
                else:
                    current_angles["right_shoulder_flexion"] = None

                if "left_shoulder_flexion" in active_joints and are_landmarks_visible(landmarks.landmark, [24, 12, 14]): # Anatomical LEFT landmarks
                    current_angles["left_shoulder_flexion"] = calculate_left_shoulder_flexion_angle(landmarks.landmark) # Assign to internal 'right' for display as 'Left'
                else:
                    current_angles["left_shoulder_flexion"] = None
            else: # If frontal
                # Display Abduction/Adduction in frontal view
                if "left_shoulder_abduction" in active_joints and are_landmarks_visible(landmarks.landmark, [8, 12, 14]): # Ear, Shoulder, Elbow
                    current_angles["left_shoulder_abduction"] = calculate_left_shoulder_abduction_angle(landmarks.landmark)
                else:
                    current_angles["left_shoulder_abduction"] = None

                if "right_shoulder_abduction" in active_joints and are_landmarks_visible(landmarks.landmark, [7, 11, 13]): # Ear, Shoulder, Elbow
                    current_angles["right_shoulder_abduction"] = calculate_right_shoulder_abduction_angle(landmarks.landmark)
                else:
                    current_angles["right_shoulder_abduction"] = None

            # Elbow (Left)
            if "left_elbow" in active_joints and are_landmarks_visible(landmarks.landmark, [12, 14, 16]):
                current_angles["left_elbow"] = calculate_left_elbow_angle(landmarks.landmark)
                if current_angles["left_elbow"] > 155:
                    current_angles["left_elbow"] = None
            else:
                current_angles["left_elbow"] = None

            # Elbow (Right)
            if "right_elbow" in active_joints and are_landmarks_visible(landmarks.landmark, [11, 13, 15]):
                current_angles["right_elbow"] = calculate_right_elbow_angle(landmarks.landmark)
                if current_angles["right_elbow"] > 155:
                    current_angles["right_elbow"] = None
            else:
                current_angles["right_elbow"] = None

            # Hip (Left) - Anatomical Left (appears on right of mirrored screen)
            if "left_hip" in active_joints and are_landmarks_visible(landmarks.landmark, [12, 24, 26]): # Shoulder, Hip, Knee
                current_angles["right_hip"] = calculate_left_hip_angle(landmarks.landmark) # Assign to 'right_hip' for display as 'Left Hip'
            else:
                current_angles["right_hip"] = None

            # Hip (Right) - Anatomical Right (appears on left of mirrored screen)
            if "right_hip" in active_joints and are_landmarks_visible(landmarks.landmark, [11, 23, 25]): # Shoulder, Hip, Knee
                current_angles["left_hip"] = calculate_right_hip_angle(landmarks.landmark) # Assign to 'left_hip' for display as 'Right Hip'
            else:
                current_angles["left_hip"] = None

            # Knee (Left) - Anatomical Left (appears on right of mirrored screen)
            if "left_knee" in active_joints and are_landmarks_visible(landmarks.landmark, [24, 26, 28]): # Hip, Knee, Ankle
                current_angles["right_knee"] = calculate_left_knee_angle(landmarks.landmark) # Assign to 'right_knee' for display as 'Left Knee'
            else:
                current_angles["right_knee"] = None

            # Knee (Right) - Anatomical Right (appears on left of mirrored screen)
            if "right_knee" in active_joints and are_landmarks_visible(landmarks.landmark, [23, 25, 27]): # Hip, Knee, Ankle
                current_angles["left_knee"] = calculate_right_knee_angle(landmarks.landmark) # Assign to 'left_knee' for display as 'Right Knee'
            else:
                current_angles["left_knee"] = None

            # Ankle (Left) - Anatomical Left (appears on right of mirrored screen)
            if "left_ankle" in active_joints and are_landmarks_visible(landmarks.landmark, [26, 28, 30]): # Knee, Ankle, Heel
                current_angles["right_ankle"] = calculate_left_ankle_angle(landmarks.landmark) # Assign to 'right_ankle' for display as 'Left Ankle'
            else:
                current_angles["right_ankle"] = None

            # Ankle (Right) - Anatomical Right (appears on left of mirrored screen)
            if "right_ankle" in active_joints and are_landmarks_visible(landmarks.landmark, [25, 27, 29]): # Knee, Ankle, Heel
                current_angles["left_ankle"] = calculate_right_ankle_angle(landmarks.landmark) # Assign to 'left_ankle' for display as 'Right Ankle'
            else:
                current_angles["left_ankle"] = None

            # Update max angles
            for joint, angle in current_angles.items():
                if angle is not None:
                    if joint not in max_angles or angle > max_angles[joint]:
                        max_angles[joint] = angle

            # Display angles on the frame
            y_offset = 30
            for joint in active_joints:
                display_joint_name = joint.replace("left_", "Left ").replace("right_", "Right ").replace("_flexion", " Flexion").replace("_abduction", " Abduction").title()
                
                # Display current angle in white if available
                if current_angles.get(joint) is not None:
                    cv2.putText(frame, f"{display_joint_name}: {int(current_angles[joint])}", 
                                (10, y_offset), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3, cv2.LINE_AA)
                    y_offset += 40
                
                # Display max angle in green if available
                if joint in max_angles:
                    cv2.putText(frame, f"Max {display_joint_name}: {int(max_angles[joint])}", 
                                (10, y_offset), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3, cv2.LINE_AA) # Green color
                    y_offset += 40

        # Store the last processed frame and angles
        last_frame = frame.copy()
        last_angles = current_angles

        # Encode the frame in JPEG format
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Yield the frame in the response
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

@app.route('/')
def index():
    """Main route that renders the index.html template."""
    return render_template('index.html')

@app.route('/get_all_joints')
def get_all_joints():
    return jsonify(list(JOINT_LANDMARK_MAP.keys()))

@app.route('/update_active_joints', methods=['POST'])
def update_active_joints():
    global active_joints
    data = request.get_json()
    active_joints = data.get('active_joints', [])
    print(f"Active joints updated to: {active_joints}") # For debugging
    return jsonify(status='success')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture_measurement', methods=['POST'])
def capture_measurement():
    global last_frame, last_angles, max_angles
    if last_frame is None or not last_angles:
        return jsonify({"status": "error", "message": "No frame or angle data available to capture."}), 400

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save image
    image_filename = f"captured_image_{timestamp}.jpg"
    cv2.imwrite(f"static/images/{image_filename}", last_frame)

    # Save angles to CSV
    csv_filename = "measurements.csv"
    file_exists = False
    try:
        with open(csv_filename, 'r') as f:
            file_exists = True
    except FileNotFoundError:
        pass

    with open(csv_filename, 'a', newline='') as csvfile:
        # Dynamically create fieldnames based on active_joints
        fieldnames = ['timestamp', 'image_file']
        for joint_name in active_joints:
            fieldnames.append(joint_name + '_angle')
            fieldnames.append('max_' + joint_name + '_angle')

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        row_data = {
            'timestamp': timestamp,
            'image_file': image_filename,
        }
        for joint_name in active_joints:
            row_data[joint_name + '_angle'] = (int(last_angles.get(joint_name, 0)) if last_angles.get(joint_name) is not None else '')
            row_data['max_' + joint_name + '_angle'] = (int(max_angles.get(joint_name, 0)) if max_angles.get(joint_name) is not None else '')

        writer.writerow(row_data)

    return jsonify({"status": "success", "message": "Measurement captured and saved!"})

if __name__ == '__main__':
    app.run(debug=True)
