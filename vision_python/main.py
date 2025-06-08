import time
import config
import connection_bridge as cb
import cv2
import face_marker as fm
import frame_rate_drawer as frd
import mediapipe as mp

bridge = cb.ConnectionBridge(config.COM_PORT, config.BAUD_RATE)
frame_rate_drawer = frd.FrameRateDrawer()

screen_capture = cv2.VideoCapture(0)
screen_capture.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAPTURE_WIDTH)
screen_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAPTURE_HEIGHT)

face_detector = mp.solutions.face_detection.FaceDetection( # type: ignore
    model_selection=0, min_detection_confidence=0.5
)

while True:
    frame_exist, frame = screen_capture.read()

    if not frame_exist:
        break

    # invertimos la imagen para que los ojos del Arduino no se muevan en la dirección contraria
    frame = cv2.flip(frame, 1)

    # convertimos de BGR2RGB (BGR a RGB) para mediapipe
    # OpenCV utiliza BGR por defecto, mientras que MediaPipe utiliza RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # obtenemos la ubicación del rostro en la imagen
    result = face_detector.process(frame_rgb)

    if result.detections:
        for detection in result.detections:
            cx, cy = fm.mark_face(detection, frame)

            # Determina comandos según la posición del rostro
            h_section = int(config.CAPTURE_WIDTH / 6)
            if cx < h_section:
                h_position = "izq1"
            elif h_section <= cx < h_section * 2:
                h_position = "izq2"
            elif h_section * 2 <= cx < h_section * 3:
                h_position = "izq3"
            elif h_section * 3 <= cx < h_section * 4:
                h_position = "ctr"
            elif h_section * 4 <= cx < h_section * 5:
                h_position = "der3"
            elif h_section * 5 <= cx < h_section * 6:
                h_position = "der2"
            else:
                h_position = "der1"

            v_section = int(config.CAPTURE_HEIGHT / 2)
            if cy < v_section:
                v_position = "arriba"
            else:
                v_position = "abajo"

            # Enviamos las posiciones en X e Y
            bridge.enviar(h_position, cache_key="horizontal_position")
            bridge.enviar(v_position, cache_key="vertical_position")

    frame_rate_drawer.update(frame)

    # Mostramos el fotograma
    cv2.imshow("frame", frame)

    # verificamos si se esta precionando la s para finalizar el programa
    if cv2.waitKey(1) == ord("q"):
        break

    # esperamos una infima cantidad de segundos para que el procesador no se sature
    time.sleep(0.01)

# cerramos la conexión
bridge.cerrar()

# detenemos la captura de pantalla
screen_capture.release()

# cerramos cualquier ventana generada por cv2
cv2.destroyAllWindows()
