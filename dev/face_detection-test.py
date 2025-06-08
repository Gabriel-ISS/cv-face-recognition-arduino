import cv2
import time
import mediapipe as mp
import tensorflow as tf

import config
import frame_rate_drawer
import face_marker

# Verifica si hay GPUs disponibles
gpus = tf.config.list_physical_devices("GPU")
if gpus:
    print("GPU(s) disponible(s):", gpus)
else:
    print("No se encontró ninguna GPU.")


screen_capture = cv2.VideoCapture(0)
screen_capture.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAPTURE_WIDTH)
screen_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAPTURE_HEIGHT)

face_detector = mp.solutions.face_detection.FaceDetection(  # type: ignore
    model_selection=0, min_detection_confidence=0.5
)

frame_rate_drawer = frame_rate_drawer.FrameRateDrawer()
wait_time = 1 / config.TARGET_FPS

while True:
    frame_exist, frame = screen_capture.read()

    if not frame_exist:
        break

    frame = cv2.flip(frame, 1)

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = face_detector.process(frame_rgb)

    if result.detections:
        for detection in result.detections:
            face_marker.mark_face(detection, frame)

    frame_rate_drawer.update(frame)
    cv2.imshow("frame", frame)

    if cv2.waitKey(1) == ord("q"):
        break

    time.sleep(wait_time)

screen_capture.release()

cv2.destroyAllWindows()
