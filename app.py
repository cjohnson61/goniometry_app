from flask import Flask, render_template, Response, request, jsonify
import cv2
import csv
from datetime import datetime

last_frame = None
last_angles = {}
max_angles = {} # Global dictionary to store max angles

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
    calculate_right_ankle_angle,
    get_angle_color
)

app = Flask(__name__)
detector = PoseDetector()

VISIBILITY_THRESHOLD = 0.7 # Minimum visibility score for a landmark to be considered present
VIEW_THRESHOLD = 0.1 # Threshold for determining frontal vs sagittal view (based on shoulder x-diff)

def are_landmarks_visible(landmarks, indices, threshold=VISIBILITY_THRESHOLD):
    """
    Checks if all specified landmarks are visible above a certain threshold.
    """
    for idx in indices:
        if landmarks[idx].visibility < threshold:
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

        # Find pose and draw landmarks
        frame = detector.find_pose(frame)
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
            if is_frontal_view:
                # Display Abduction/Adduction in frontal view
                if are_landmarks_visible(landmarks.landmark, [8, 12, 14]): # Ear, Shoulder, Elbow
                    current_angles["left_shoulder_abduction"] = calculate_left_shoulder_abduction_angle(landmarks.landmark)
                else:
                    current_angles["left_shoulder_abduction"] = None

                if are_landmarks_visible(landmarks.landmark, [7, 11, 13]): # Ear, Shoulder, Elbow
                    current_angles["right_shoulder_abduction"] = calculate_right_shoulder_abduction_angle(landmarks.landmark)
                else:
                    current_angles["right_shoulder_abduction"] = None
            else:
                # Display Flexion/Extension in sagittal view
                if are_landmarks_visible(landmarks.landmark, [24, 12, 14]): # Hip, Shoulder, Elbow
                    current_angles["left_shoulder_flexion"] = calculate_left_shoulder_flexion_angle(landmarks.landmark)
                else:
                    current_angles["left_shoulder_flexion"] = None

                if are_landmarks_visible(landmarks.landmark, [23, 11, 13]): # Hip, Shoulder, Elbow
                    current_angles["right_shoulder_flexion"] = calculate_right_shoulder_flexion_angle(landmarks.landmark)
                else:
                    current_angles["right_shoulder_flexion"] = None

            # Elbow (Left)
            # Only calculate if in frontal view (shoulder and elbow x-coordinates are NOT close)
            if are_landmarks_visible(landmarks.landmark, [12, 14, 16]) and abs(landmarks.landmark[12].x - landmarks.landmark[14].x) > VIEW_THRESHOLD:
                current_angles["left_elbow"] = calculate_left_elbow_angle(landmarks.landmark)
                if current_angles["left_elbow"] > 155:
                    current_angles["left_elbow"] = None
            else:
                current_angles["left_elbow"] = None

            # Elbow (Right)
            # Only calculate if in frontal view (shoulder and elbow x-coordinates are NOT close)
            if are_landmarks_visible(landmarks.landmark, [11, 13, 15]) and abs(landmarks.landmark[11].x - landmarks.landmark[13].x) > VIEW_THRESHOLD:
                current_angles["right_elbow"] = calculate_right_elbow_angle(landmarks.landmark)
                if current_angles["right_elbow"] > 155:
                    current_angles["right_elbow"] = None
            else:
                current_angles["right_elbow"] = None

            # Hip (Left)
            if are_landmarks_visible(landmarks.landmark, [12, 24, 26]): # Shoulder, Hip, Knee
                current_angles["left_hip"] = calculate_left_hip_angle(landmarks.landmark)
            else:
                current_angles["left_hip"] = None

            # Hip (Right)
            if are_landmarks_visible(landmarks.landmark, [11, 23, 25]): # Shoulder, Hip, Knee
                current_angles["right_hip"] = calculate_right_hip_angle(landmarks.landmark)
            else:
                current_angles["right_hip"] = None

            # Knee (Left)
            if are_landmarks_visible(landmarks.landmark, [24, 26, 28]): # Hip, Knee, Ankle
                current_angles["left_knee"] = calculate_left_knee_angle(landmarks.landmark)
            else:
                current_angles["left_knee"] = None

            # Knee (Right)
            if are_landmarks_visible(landmarks.landmark, [23, 25, 27]): # Hip, Knee, Ankle
                current_angles["right_knee"] = calculate_right_knee_angle(landmarks.landmark)
            else:
                current_angles["right_knee"] = None

            # Ankle (Left)
            if are_landmarks_visible(landmarks.landmark, [26, 28, 30]): # Knee, Ankle, Heel
                current_angles["left_ankle"] = calculate_left_ankle_angle(landmarks.landmark)
            else:
                current_angles["left_ankle"] = None

            # Ankle (Right)
            if are_landmarks_visible(landmarks.landmark, [25, 27, 29]): # Knee, Ankle, Heel
                current_angles["right_ankle"] = calculate_right_ankle_angle(landmarks.landmark)
            else:
                current_angles["right_ankle"] = None

            # Update max angles
            for joint, angle in current_angles.items():
                if angle is not None:
                    if joint not in max_angles or angle > max_angles[joint]:
                        max_angles[joint] = angle

            # Display angles on the frame
            y_offset = 30
            for joint, angle in current_angles.items():
                if angle is not None:
                    display_joint_name = joint.replace("left_", "Right ").replace("right_", "Left ").replace("_flexion", " Flexion").replace("_abduction", " Abduction").title()
                    
                    # Display current angle in white
                    cv2.putText(frame, f"{display_joint_name}: {int(angle)}", 
                                (10, y_offset), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                    y_offset += 30

                    # Display max angle in green, next to current angle
                    if joint in max_angles:
                        cv2.putText(frame, f"Max: {int(max_angles[joint])}", 
                                    (10, y_offset), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA) # Green color
                        y_offset += 30

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

@app.route('/video_feed')
def video_feed():
    """Video streaming route."""
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
        fieldnames = ['timestamp', 'image_file',
                      'left_shoulder_flexion_angle', 'right_shoulder_flexion_angle',
                      'left_shoulder_abduction_angle', 'right_shoulder_abduction_angle',
                      'left_elbow_angle', 'right_elbow_angle',
                      'left_hip_angle', 'right_hip_angle',
                      'left_knee_angle', 'right_knee_angle',
                      'left_ankle_angle', 'right_ankle_angle',
                      'max_left_shoulder_flexion_angle', 'max_right_shoulder_flexion_angle',
                      'max_left_shoulder_abduction_angle', 'max_right_shoulder_abduction_angle',
                      'max_left_elbow_angle', 'max_right_elbow_angle',
                      'max_left_hip_angle', 'max_right_hip_angle',
                      'max_left_knee_angle', 'max_right_knee_angle',
                      'max_left_ankle_angle', 'max_right_ankle_angle']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        row_data = {
            'timestamp': timestamp,
            'image_file': image_filename,
        }
        for joint_name in [
            'left_shoulder_flexion', 'right_shoulder_flexion',
            'left_shoulder_abduction', 'right_shoulder_abduction',
            'left_elbow', 'right_elbow',
            'left_hip', 'right_hip',
            'left_knee', 'right_knee',
            'left_ankle', 'right_ankle'
        ]:
            row_data[joint_name + '_angle'] = (int(last_angles.get(joint_name, 0)) if last_angles.get(joint_name) is not None else '')
            row_data['max_' + joint_name + '_angle'] = (int(max_angles.get(joint_name, 0)) if max_angles.get(joint_name) is not None else '')
        
        writer.writerow(row_data)
    
    return jsonify({"status": "success", "message": "Measurement captured successfully."})

if __name__ == '__main__':
    app.run(debug=True)