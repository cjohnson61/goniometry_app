
import unittest
import cv2
import numpy as np
from pose_detector import PoseDetector

class TestPoseDetector(unittest.TestCase):

    def test_find_landmarks_on_blank_image(self):
        """Test that the pose detector runs on a blank image without errors."""
        # Create a dummy black image
        blank_image = np.zeros((480, 640, 3), dtype=np.uint8)

        # Initialize the pose detector
        detector = PoseDetector()

        # Find landmarks in the blank image
        landmarks = detector.find_landmarks(blank_image)

        # On a blank image, we expect no landmarks to be found
        self.assertEqual(len(landmarks), 0)

if __name__ == '__main__':
    unittest.main()
