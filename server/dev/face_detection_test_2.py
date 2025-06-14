import time
from typing import List

import cv2
import mediapipe as mp
import tensorflow as tf

from server import config
from server.utils.command_selector import get_commands
from server.utils.connection_bridge import ConnectionBridge
from server.utils.face import Face
from server.utils.face_selector import select_face
from server.utils.face_tracker import FaceTracker
from server.utils.frame_rate_drawer import FrameRateDrawer
from server.utils.kalman_filter import MultiKalmanFilter

bridge = ConnectionBridge(config.COM_PORT, config.BAUD_RATE, debug=True)

# Verifica si hay GPUs disponibles
gpus = tf.config.list_physical_devices("GPU")
if gpus:
    print("GPU(s) disponible(s):", gpus)
else:
    print("No se encontró ninguna GPU.")


screen_capture = cv2.VideoCapture(config.CAMERA)
screen_capture.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAPTURE_WIDTH)
screen_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAPTURE_HEIGHT)

face_detector = mp.solutions.face_detection.FaceDetection(  # type: ignore
    model_selection=0, min_detection_confidence=0.5
)

frame_rate_drawer = FrameRateDrawer()
faces_identifier = FaceTracker(100)
position_kalman = MultiKalmanFilter()
size_kalman = MultiKalmanFilter()
faces_identifier.on_face_removed(
    lambda face_id: position_kalman.kalmans.pop(face_id, None)
)  # Elimina el KalmanFilter asociado a la cara eliminada
wait_time = 1 / config.TARGET_FPS

while True:
    frame_exist, frame = screen_capture.read()

    if not frame_exist:
        break

    frame = cv2.flip(frame, 1)

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = face_detector.process(frame_rgb)

    if result.detections:
        faces: List[Face] = []
        for detection in result.detections:
            h, w, _ = frame.shape
            face = Face(detection, (w, h))
            face_id = faces_identifier.identify((face.center_x, face.center_y))
            cx, cy = position_kalman.predict(face_id, face.center_x, face.center_y)
            w, h = size_kalman.predict(
                face_id, face.width, face.height
            )

            # Actualizamos las coordenadas y dimensiones del rostro
            face.id = face_id
            face.center_x = int(cx)
            face.center_y = int(cy)
            face.width = int(w)
            face.height = int(h)

            face.mark_from_center(frame)
            faces.append(face)

        if faces:
            # Si hay caras detectadas, tomamos la más grande
            largest_face = select_face(faces)

            # Determina comandos según la posición del rostro
            h_position, v_position = get_commands(
                largest_face.center_x,  # type: ignore
                largest_face.center_y,  # type: ignore
            )

            # Enviamos las posiciones en X e Y
            bridge.enviar(h_position, cache_key="horizontal_position")
            bridge.enviar(v_position, cache_key="vertical_position")

    frame_rate_drawer.update(frame)
    cv2.imshow("frame", frame)

    if cv2.waitKey(1) == ord("q"):
        break

    time.sleep(wait_time)

screen_capture.release()

cv2.destroyAllWindows()
