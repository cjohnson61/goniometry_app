# Digital Goniometry Application

## Project Overview

A computer vision-based web application that provides real-time joint angle measurements for physical therapy assessments. The application uses MediaPipe pose detection to automatically identify body landmarks and calculate goniometric measurements from live camera feed, eliminating the need for manual goniometer measurements.

## Objectives

### Primary Goals
- **Automated Joint Measurement**: Replace manual goniometer measurements with computer vision-based angle detection
- **Real-time Analysis**: Provide immediate feedback during patient assessments
- **Clinical Accuracy**: Achieve measurements within ±5° of manual goniometer readings
- **Ease of Use**: Simple web interface that physical therapists can use without technical expertise

### Target Measurements
The application measures angles for five key joints:
1. **Shoulder** - Abduction/flexion angles
2. **Elbow** - Flexion/extension angles
3. **Hip** - Flexion/extension angles
4. **Knee** - Flexion/extension angles
5. **Ankle** - Dorsiflexion/plantarflexion angles

## Technical Specifications

### Technology Stack
- **Backend**: Python with Flask web framework
- **Computer Vision**: OpenCV + MediaPipe Pose
- **Frontend**: HTML/CSS/JavaScript
- **Camera**: Built-in MacBook camera via OpenCV
- **Platform**: macOS (Apple Silicon optimized)
- **Package Management**: Homebrew + pip

### Development Environment
- **Target Platform**: MacBook Pro with Apple Silicon
- **Python Version**: 3.9+
- **Installation Method**: Homebrew for system dependencies
- **Architecture**: Web-based application running locally

## Implementation Plan

### Phase 1: Environment Setup
**Objective**: Establish development environment and test basic functionality

**Tasks**:
1. Install Homebrew dependencies:
   - Python 3.9+
   - OpenCV with camera support
   - Required Python packages
2. Create virtual environment
3. Test camera access and MediaPipe pose detection
4. Validate setup with test image

**Success Criteria**:
- Camera accessible via OpenCV
- MediaPipe pose detection working
- Basic angle calculation functioning

### Phase 2: Core Computer Vision Engine
**Objective**: Build robust pose detection and angle calculation system

**Tasks**:
1. Build pose detection module:
   - Initialize MediaPipe Pose
   - Process video frames
   - Extract joint landmarks
   - Handle detection confidence scoring
2. Create angle calculation functions:
   - Implement 3-point angle geometry
   - One function per joint type
   - Handle edge cases (missing landmarks)
   - Return confidence scores

**Success Criteria**:
- Accurate pose detection in various lighting conditions
- Precise angle calculations validated against known measurements
- Robust error handling for missing landmarks

### Phase 3: Flask Web Application
**Objective**: Create web interface for real-time camera processing

**Tasks**:
1. Backend Flask routes:
   - `/` - Main interface
   - `/video_feed` - Camera stream endpoint
   - `/process_frame` - Real-time angle calculation
   - `/capture` - Save current frame and measurements
2. Frontend interface:
   - Live camera preview
   - Real-time angle display overlay
   - Capture button for measurements
   - Joint selector (focus on specific joints)

**Success Criteria**:
- Smooth video streaming in web browser
- Real-time angle calculations displayed
- Responsive user interface

### Phase 4: Real-time Visualization
**Objective**: Implement visual feedback and measurement overlays

**Tasks**:
1. Overlay graphics on video stream:
   - Draw pose skeleton
   - Highlight measured joints
   - Display angle values as text
   - Color-code angles (green=normal, yellow=caution, red=extreme)
2. User interface controls:
   - Start/stop measurement
   - Select which joints to measure
   - Calibration/positioning guidance

**Success Criteria**:
- Clear visual feedback on video stream
- Intuitive color coding for angle ranges
- Smooth real-time performance (15-30 FPS)

### Phase 5: Testing and Validation
**Objective**: Ensure accuracy and reliability of measurements

**Tasks**:
1. Test with reference images
2. Validate measurements against known angles
3. Test real-time performance
4. Optimize for Apple Silicon
5. Clinical accuracy assessment

**Success Criteria**:
- Measurements within ±5° of manual goniometer
- Consistent performance across different poses
- Stable real-time processing

## Project Structure

```
goniometry_app/
├── README.md             # This file
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
│       └── test_images/ # Test images for validation
├── requirements.txt      # Python dependencies
└── tests/
    ├── test_angles.py   # Unit tests for angle calculations
    └── test_pose.py     # Tests for pose detection
```

## Key Technical Challenges

### 1. Camera Permission Handling
- macOS camera permission requirements
- Browser security restrictions
- Fallback mechanisms for permission failures

### 2. Real-time Processing Performance
- Target: 15-30 FPS for smooth user experience
- Apple Silicon optimization
- Efficient video processing pipeline

### 3. Pose Detection Accuracy
- Varying lighting conditions
- Different body types and clothing
- Partial occlusion handling

### 4. Angle Calculation Precision
- 3-point geometry accuracy
- Confidence score implementation
- Edge case handling (missing landmarks)

### 5. Web Browser Camera Streaming
- Cross-browser compatibility
- Video stream encoding/decoding
- Real-time data transmission

## Development Workflow

### Recommended Development Sequence
1. **Start with static image processing** (validate with reference images)
2. **Add camera capture** (test basic video streaming)
3. **Implement real-time processing** (optimize performance)
4. **Add web interface** (user experience focus)
5. **Polish visualization and UX** (clinical usability)

### Testing Strategy
- Unit tests for angle calculation functions
- Integration tests for pose detection pipeline
- Performance benchmarks for real-time processing
- Clinical validation against manual measurements

## Future Enhancements

### Phase 6: Data Management (Future)
- Local SQLite database for measurements
- Patient session tracking
- Export measurements to CSV/PDF
- Measurement history and progress tracking

### Phase 7: Advanced Features (Future)
- Multiple camera angles
- 3D pose estimation
- Machine learning-based pose refinement
- Integration with electronic health records

### Phase 8: Clinical Integration (Future)
- FDA compliance considerations
- HIPAA compliance for patient data
- Clinical workflow integration
- Multi-user support for PT clinics

## Estimated Timeline

- **Day 1**: Environment setup and basic pose detection
- **Day 2**: Angle calculations and testing with static images
- **Day 3**: Flask app and camera integration
- **Day 4**: Real-time processing and visualization
- **Day 5**: Polish, testing, and validation

## Success Metrics

### Technical Metrics
- **Accuracy**: Measurements within ±5° of manual goniometer
- **Performance**: Consistent 15-30 FPS real-time processing
- **Reliability**: 95%+ pose detection success rate
- **Usability**: <30 seconds per measurement

### Clinical Metrics
- **Precision**: Consistent measurements across multiple captures
- **Inter-rater Reliability**: Consistent results between different users
- **Clinical Acceptance**: Positive feedback from PT professionals

## Installation Prerequisites

### System Requirements
- macOS (Apple Silicon preferred)
- Homebrew package manager
- Built-in camera or external webcam
- Python 3.9+

### Required Packages (to be installed)
```
flask
opencv-python
mediapipe
numpy
```

## Getting Started

1. **Clone or create project directory**
2. **Follow Phase 1 implementation steps**
3. **Test with provided reference images**
4. **Validate accuracy against known measurements**
5. **Iterate based on testing results**

## Notes for LLM Code Assistant

### Code Generation Guidelines
- **Prioritize accuracy over speed** in angle calculations
- **Implement robust error handling** for missing landmarks
- **Use clear, well-documented functions** for each component
- **Include comprehensive testing** for all calculations
- **Optimize for Apple Silicon** where possible

### Development Priorities
1. **Accuracy first** - Validate every calculation
2. **User experience** - Simple, intuitive interface
3. **Performance** - Smooth real-time operation
4. **Extensibility** - Easy to add new joints or features

### Testing Requirements
- Include unit tests for all angle calculation functions
- Provide test images with known angle measurements
- Implement confidence scoring for pose detection
- Add performance benchmarks for real-time processing

This README serves as the complete specification for building the Digital Goniometry Application prototype.
