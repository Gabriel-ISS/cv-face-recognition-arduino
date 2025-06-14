import cv2
import mediapipe as mp
import numpy as np

from server import config
from server.utils.face import Face
from server.utils.kalman_filter import KalmanFilter

# Inicializa MediaPipe
mp_face_detection = mp.solutions.face_detection  # type: ignore
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.2)

kalman = KalmanFilter()

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAPTURE_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAPTURE_HEIGHT)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Detección de rostros
    results = face_detection.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    if results.detections:
        for detection in results.detections:
            bboxC = detection.location_data.relative_bounding_box
            face = Face(detection, (frame.shape[1], frame.shape[0]))
            #face.mark(frame)

            x = face.x
            y = face.y
            width = face.width
            height = face.height
            center_x = face.center_x
            center_y = face.center_y

            #kalman.statePost = np.array([[np.float32(center_x)], [np.float32(center_y)], [0], [0]])

            # Actualiza el filtro de Kalman
            cx, cy = kalman.predict(center_x, center_y)

            # Dibuja el rectángulo estabilizado
            new_x = int(cx - width / 2)
            new_y = int(cy - height / 2)
            cv2.rectangle(
                frame, (new_x, new_y), (new_x + width, new_y + height), (0, 255, 0), 2
            )

    cv2.imshow("Face Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
