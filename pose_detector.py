
import cv2
import mediapipe as mp

class PoseDetector:
    """
    A class to detect human poses in an image or video stream using MediaPipe.
    """

    def __init__(self, mode=False, complexity=1, smooth=True, detection_con=0.5, track_con=0.5):
        """
        Initializes the PoseDetector with MediaPipe Pose.
        """
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(static_image_mode=mode,
                                      model_complexity=complexity,
                                      smooth_landmarks=smooth,
                                      min_detection_confidence=detection_con,
                                      min_tracking_confidence=track_con)
        self.mp_draw = mp.solutions.drawing_utils

    def find_pose(self, img, draw=True):
        """
        Finds the pose in an image and draws the landmarks and connections.
        """
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(img_rgb)

        if self.results.pose_landmarks and draw:
            self.mp_draw.draw_landmarks(img, self.results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS,
                                        landmark_drawing_spec=self.mp_draw.DrawingSpec(color=(0, 255, 0), thickness=6, circle_radius=3),
                                        connection_drawing_spec=self.mp_draw.DrawingSpec(color=(0, 255, 0), thickness=6))
        
        return img

    def find_landmarks(self, img):
        """
        Finds the pose landmarks in an image without drawing.
        Returns the list of landmarks.
        """
        if not hasattr(self, 'results') or self.results is None:
            # Process the image if landmarks haven't been found yet
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            self.results = self.pose.process(img_rgb)

        landmarks = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                landmarks.append([id, cx, cy])
        
        return landmarks
