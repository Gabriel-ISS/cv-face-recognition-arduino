import cv2
import serial
import time
import mediapipe as mp


class PuenteDeConexion:
    """Utilidad para administrar la comunicación con el Arduino. Actualmente utiliza una conexio serial.

    Comunicacion serial: facilita el envío y recepción de datos en forma de señales eléctricas a través de cables,
    lo que es útil en aplicaciones donde se requiere una comunicación simple y directa. Se le dice serial porque 
    los datos se envían de un bit a la vez, en una secuencia continua.
    """

    ultimo_comando = ""

    ser: serial.Serial | None = None

    def __init__(self, COM: int, BAUD: int):
        # Configuración del puerto serial
        self.ser = serial.Serial("COM" + str(COM), BAUD)

    def enviar(self, comando: str):
        if self.ser is None:
            return

        if comando == self.ultimo_comando:
            return

        print(f"Enviando: {comando}")
        self.ser.write((comando + "\n").encode())
        self.ultimo_comando = comando

    def cerrar(self):
        if self.ser is not None:
            self.ser.close()
            self.ultimo_comando = ""


def marcar_rostro(deteccion, fotograma: cv2.typing.MatLike):
    """Dibuja el rostro detectado en el fotograma

    Argumentos:
        deteccion (_type_): Objeto con los datos de posicion y tamaño del rrostro detectado
        fotograma (cv2.typing.MatLike): Imagen actual a marcar

    Returns:
        (int, int): posicion en x e y del centro
    """
    
    # extraemos los datos de posicion y tamaño
    # bbox contiene los datos que necesitamos pero en rangos de 0 al 1
    # por eso multiplicamos los valores por el tamaño del fotograma
    # de esa forma convertimos los datos de 0-1 a el tamaño en pixeles.
    bbox = deteccion.location_data.relative_bounding_box
    h, w, _ = fotograma.shape
    x = int(bbox.xmin * w)
    y = int(bbox.ymin * h)
    ancho = int(bbox.width * w)
    alto = int(bbox.height * h)

    # Colores en RGB
    verde = (0, 255, 0)
    azul = (0, 0, 255) # TODO: o verde

    # Dibuja el recuadro del rostro con una linea 2 pixeles de grosor
    cv2.rectangle(fotograma, (x, y), (x + ancho, y + alto), verde, 2)

    # dibuja el centro del rostro como un circulo de 5 pixeles de radio
    cx = x + ancho // 2
    cy = y + alto // 2
    centro = (cx, cy)
    # -1 indica que el circulo se debe rellenar
    cv2.circle(fotograma, centro, 5, azul, -1)

    return centro


# Cremos el puente de comunicación
# Estableciendo el puerto COM de la computadora
# y los bauidios (cantidad de intercambio de datos por segundo)
puente = PuenteDeConexion(6, 9600)

# Preparamos la captura de pantall
capture_width = 640
capture_height = 480
captura_de_pantalla = cv2.VideoCapture(0)
captura_de_pantalla.set(cv2.CAP_PROP_FRAME_WIDTH, capture_width)
captura_de_pantalla.set(cv2.CAP_PROP_FRAME_HEIGHT, capture_height)

# Preparamos la deteccion de rostros con MediaPipe Face Detection
detector_de_rostros = mp.solutions.face_detection.FaceDetection(
    model_selection=0, min_detection_confidence=0.5
)

# Iniciamos el programa
while True:
    # obtenemos el fotograma actual
    # un fotograma es una imagen de un video
    fotograma_existe, fotograma = captura_de_pantalla.read()

    # si no se esta obteniendo ningun fotograma detenemos el bucle
    if not fotograma_existe:
        break

    # invertimos la imagen para que los ojos del arduino no se muevan en la deirección contraria
    fotograma = cv2.flip(fotograma, 1)

    # conbvertimos de BGR2RGB (RGB a BGR) para mediapipe
    # OpenCV utiliza BGR por defecto, mientras que MediaPipe utiliza RGB
    frame_rgb = cv2.cvtColor(fotograma, cv2.COLOR_BGR2RGB)

    # obtenemos la hubicacion del rostro en la imagen
    resultados = detector_de_rostros.process(frame_rgb)

    # Detección de rostro
    if resultados.detections:
        for deteccion in resultados.detections:
            cx, cy = marcar_rostro(deteccion, fotograma)

            # Determina comandos según la posición del rostro
            # En este caso el comando es
            seccion_h = int(capture_width / 6)
            if cx < seccion_h:
                posicion_x = "izq1"
            elif seccion_h <= cx < seccion_h * 2:
                posicion_x = "izq2"
            elif seccion_h * 2 <= cx < seccion_h * 3:
                posicion_x = "izq3"
            elif seccion_h * 3 <= cx < seccion_h * 4:
                posicion_x = "ctr"
            elif seccion_h * 4 <= cx < seccion_h * 5:
                posicion_x = "der3"
            elif seccion_h * 5 <= cx < seccion_h * 6:
                posicion_x = "der2"
            else:
                posicion_x = "der1"

            seccion_v = int(capture_height / 2)
            if cy < seccion_v:
                posicion_y = "arriba"
            else:
                posicion_y = "abajo"

            # Enviamos las posiciones en X e Y
            # Lo ideal seria enviarlo asi f"posicion{posicion_x:posicion_y}"
            # y luego separarlo en el codigo del arduino
            puente.enviar(posicion_x)
            puente.enviar(posicion_y)

    # Mostramos el fotograma
    cv2.imshow("frame", fotograma)

    # verificamos si se esta precionando la s para finalizar el programa
    if cv2.waitKey(1) & 0xFF == ord("s"):
        break

    # esperamos una infima cantidad de segundos para que el procesador no se sature
    time.sleep(0.05)

# cerramos la conexion
puente.cerrar()

# detenemos la captura de pantalla
captura_de_pantalla.release()

# cerramos cualquier ventana generada por cv2
cv2.destroyAllWindows()
