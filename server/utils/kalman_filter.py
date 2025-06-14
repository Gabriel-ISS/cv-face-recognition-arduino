from typing import Tuple
import cv2
import numpy as np
from server import config

class KalmanFilter:
    kalman: cv2.KalmanFilter

    def __init__(self) -> None:
        self.kalman = cv2.KalmanFilter(4, 2)
        self.kalman.measurementMatrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0]], np.float32)
        self.kalman.transitionMatrix = np.array(
            [[1, 0, 1, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], np.float32
        )
        self.kalman.processNoiseCov = np.array(
                    [[1, 0, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]], np.float32) * 0.03
        
        cx, cy = config.CAPTURE_WIDTH // 2, config.CAPTURE_HEIGHT // 2
        self.kalman.statePre = np.array([[cx], [cy], [0], [0]], np.float32)
        self.kalman.statePost = np.array([[cx], [cy], [0], [0]], np.float32)
    
    def predict(self, center_x: float, center_y: float) -> Tuple[float, float]:
        """
        Predicts the next position of the object using the Kalman filter.
        
        :param center_x: The x-coordinate of the current position.
        :param center_y: The y-coordinate of the current position.
        :return: A tuple containing the predicted x and y coordinates.
        """
        self.kalman.correct(np.array([[np.float32(center_x)], [np.float32(center_y)]]))
        prediction = self.kalman.predict()
        return (prediction[0][0], prediction[1][0])

class MultiKalmanFilter:
    kalmans: dict[int, KalmanFilter]

    measurements = []

    def __init__(self) -> None:
        self.kalmans = {}

    def predict(self, face_id: int, center_x: float, center_y: float) -> Tuple[float, float]:
        """
        Predicts the next position of the object using the Kalman filter for a specific face ID.
        
        :param face_id: The ID of the face to track.
        :param center_x: The x-coordinate of the current position.
        :param center_y: The y-coordinate of the current position.
        :return: A tuple containing the predicted x and y coordinates.
        """
        if face_id not in self.kalmans:
            self.kalmans[face_id] = KalmanFilter()
        
        return self.kalmans[face_id].predict(center_x, center_y)