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
- Adding a joint selector to focus on specific joints.
- Refining the UI/UX for clinical usability.
- Implementing more robust data management (e.g., patient sessions, database integration).
- Displaying measurement history and progress tracking.
- Addressing the removal of facial feature points more robustly.
- Improving angle calculation accuracy for specific movements or challenging lighting conditions.