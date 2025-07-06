
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
        # Define drawing specs once to avoid creating them on every frame
        self.visible_spec = self.mp_draw.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2)
        self.invisible_spec = self.mp_draw.DrawingSpec(color=(0, 0, 0), thickness=0, circle_radius=0)


    def find_pose(self, img, active_joints, joint_landmark_map, draw=True):
        """
        Finds the pose in an image and draws the landmarks and connections.
        Conditionally draws based on active_joints.
        """
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(img_rgb)

        if self.results.pose_landmarks and draw:
            # Determine which landmarks and connections should be visible
            visible_landmarks_indices = set()
            for joint_id in active_joints:
                if joint_id in joint_landmark_map:
                    visible_landmarks_indices.update(joint_landmark_map[joint_id])

            # Create a filtered list of connections to draw
            visible_connections = [
                connection for connection in self.mp_pose.POSE_CONNECTIONS
                if connection[0] in visible_landmarks_indices and connection[1] in visible_landmarks_indices
            ]
            
            # Draw only the visible landmarks by iterating and drawing one by one
            # This is necessary because draw_landmarks doesn't support hiding individual landmarks easily
            for idx, landmark in enumerate(self.results.pose_landmarks.landmark):
                if idx in visible_landmarks_indices:
                    cv2.circle(img, (int(landmark.x * img.shape[1]), int(landmark.y * img.shape[0])),
                               radius=3, color=(0, 255, 0), thickness=-1)

            # Draw only the visible connections
            self.mp_draw.draw_landmarks(
                img,
                self.results.pose_landmarks,
                connections=visible_connections,
                # landmark_drawing_spec is None because we drew them manually
                connection_drawing_spec=self.visible_spec
            )
        
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
