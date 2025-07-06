# Digital Goniometry Application - Current Design

This document outlines the current design and implemented features of the Digital Goniometry Application prototype.

## 1. Project Overview

A computer vision-based web application that provides real-time joint angle measurements for physical therapy assessments. The application uses MediaPipe pose detection to automatically identify body landmarks and calculate goniometric measurements from a live camera feed.

## 2. Implemented Features

### 2.1. Core Functionality
- **Real-time Video Stream:** The application successfully streams live video from the user's webcam to a web browser.
- **Pose Detection:** Utilizes MediaPipe Pose to detect human body landmarks in real-time from the video feed.
- **Joint Angle Calculation (Left & Right):** Accurately calculates angles for both left and right sides of the following key joints:
    - **Shoulder:** Differentiated into Flexion/Extension (using Hip-Shoulder-Elbow landmarks) and Abduction/Adduction (using Ear-Shoulder-Elbow landmarks).
    - **Elbow:** Flexion/Extension (0 degrees for full extension).
    - **Hip:** Flexion/Extension (0 degrees for full extension).
    - **Knee:** Flexion/Extension (0 degrees for full extension).
    - **Ankle:** Dorsiflexion/Plantarflexion (0 degrees for full extension).
- **Real-time Overlay:** Overlays a green pose skeleton and displays the calculated joint angles directly on the video stream. Display labels for left/right joints are mirrored to match the camera view.
- **Angle Color-Coding:** Joint angles are color-coded (green, yellow, red) based on predefined ranges to provide immediate visual feedback on the measurement status.
- **Visibility-Based Display:** Angles are only displayed and saved if all necessary landmarks for that calculation are visible above a defined confidence threshold.
- **Capture and Save Measurements:** A "Capture Measurement" button allows users to save the current video frame (as a JPEG image) and all calculated joint angles (to a CSV file) with a timestamp.

### 2.2. Technical Details
- **Backend:** Python with Flask web framework (`app.py`).
- **Computer Vision:** OpenCV for camera access and MediaPipe Pose for pose estimation (`pose_detector.py`).
- **Angle Calculation Logic:** Custom Python module for geometric angle calculations (`angle_calculator.py`).
- **Frontend:** Basic HTML (`templates/index.html`) for displaying the video feed and CSS (`static/css/style.css`) for basic styling. JavaScript (`static/js/app.js`) handles the capture button functionality.
- **Development Environment:** Managed with a Python virtual environment and `requirements.txt` for dependencies.

## 3. Project Structure

```
goniometry_app/
├── README.md             # Project overview and initial plan
├── app.py                # Main Flask application
├── pose_detector.py      # MediaPipe pose detection module
├── angle_calculator.py   # Joint angle calculation functions
├── templates/
│   └── index.html       # Web interface template
├── static/
│   ├── css/
│   │   └── style.css    # Application styling
│   ├── js/
│   │   └── app.js       # Frontend JavaScript
│   └── images/
│       └── test_images/ # Placeholder for test images (captured images saved here)
├── requirements.txt      # Python dependencies
├── tests/
│   ├── test_angles.py   # Unit tests for angle calculations
│   └── test_pose.py     # Tests for pose detection
├── measurements.csv      # Saved angle measurements (created on first capture)
└── design.md             # This document
```

## 4. Usage Instructions

To run the application:
1.  Ensure all Python dependencies are installed in your virtual environment (`venv/bin/pip install -r requirements.txt`).
2.  Run the Flask application from the project root directory:
    ```bash
    venv/bin/python app.py
    ```
3.  Open your web browser and navigate to `http://127.0.0.1:5000/`.

To stop the application, press `Ctrl + C` in the terminal where the Flask server is running.

## 5. Next Steps / Future Enhancements

Based on the `README.md` and current progress, potential next steps include:

### 5.1. Dynamic Joint Selection (Detailed Plan)

**Objective:** Allow users to select which joints to display measurements for, reducing visual clutter and focusing on relevant data, by dynamically controlling the visibility of the pose skeleton.

**Implementation Approach:**

Instead of attempting to modify MediaPipe's drawing directly, which proved problematic, the revised approach focuses on controlling the *visibility* of drawn elements (landmarks and connections) by setting their color and thickness to transparent/zero when they are not part of an actively selected joint.

**Implementation Steps:**

1.  **Frontend (`templates/index.html` & `static/js/app.js`):**
    *   Add a control panel (e.g., a series of checkboxes or a multi-select dropdown) to `index.html` for each measurable joint (e.g., "Left Shoulder Flexion", "Right Elbow", "Left Ankle").
    *   Implement JavaScript in `app.js` to:
        *   Read the state of these checkboxes/selections.
        *   Send an AJAX request (e.g., `POST` or `PUT`) to a new Flask endpoint whenever the selections change. This request will send a list of currently selected joint identifiers.
        *   Potentially store the user's preferences in local storage for persistence across sessions.

2.  **Backend (`app.py`):**
    *   Create a new Flask endpoint (e.g., `/update_active_joints`) that receives the list of selected joint identifiers from the frontend.
    *   Store this list in a global variable (e.g., `active_joints`) or a session variable on the server-side.
    *   Define a `JOINT_LANDMARK_MAP` dictionary that maps each joint identifier (e.g., "left_shoulder_flexion") to a list of MediaPipe landmark indices involved in that joint's calculation. This map will be crucial for determining which landmarks and connections belong to which joint.
    *   Modify the `generate_frames` function:
        *   Pass the `active_joints` list and the `JOINT_LANDMARK_MAP` to the `detector.find_pose()` method.
        *   Before calculating and displaying any joint angle, check if that specific joint's identifier is present in the `active_joints` list. If it's not, skip its calculation and display.
    *   Modify the `capture_measurement` function:
        *   When saving to `measurements.csv`, only include columns and values for joints that are currently in the `active_joints` list. For unselected joints, their corresponding CSV cells should remain empty.

3.  **Pose Detector (`pose_detector.py`):**
    *   Update `find_pose` method signature to accept `active_joints` and `joint_landmark_map`.
    *   Inside `find_pose`, create a set of `visible_landmarks_indices` by iterating through `active_joints` and looking up their corresponding landmark indices in `joint_landmark_map`.
    *   When drawing landmarks:
        *   Iterate through all detected `pose_landmarks`.
        *   For each landmark, if its index is *not* in `visible_landmarks_indices`, set its `DrawingSpec` color to black (or transparent) and thickness/radius to 0. Otherwise, use the default green drawing spec.
    *   When drawing connections:
        *   Iterate through all `mp_pose.POSE_CONNECTIONS`.
        *   For each connection, if *either* of its constituent landmark indices is *not* in `visible_landmarks_indices`, set its `DrawingSpec` color to black (or transparent) and thickness to 0. Otherwise, use the default green drawing spec.

**Joint Identifiers (Examples):**
*   `left_shoulder_flexion`
*   `right_shoulder_flexion`
*   `left_shoulder_abduction`
*   `right_shoulder_abduction`
*   `left_elbow`
*   `right_elbow`
*   `left_hip`
*   `right_hip`
*   `left_knee`
*   `right_knee`
*   `left_ankle`
*   `right_ankle`

**Success Criteria:**
*   Users can select/deselect individual joints from the web interface.
*   Only selected joint angles are displayed on the video feed.
*   Only the pose skeleton segments and landmarks corresponding to selected joints are visible on the video feed.
*   Only selected joint angles are saved to `measurements.csv`.
*   The application remains responsive and performs well with dynamic selection.