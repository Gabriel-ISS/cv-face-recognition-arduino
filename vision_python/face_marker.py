import cv2


def mark_face(detection, frame):
    """Dibuja el rostro detectado en el fotograma

    Argumentos:
        deteccion (_type_): Objeto con los datos de posición y tamaño del rostro detectado
        fotograma (cv2.typing.MatLike): Imagen actual a marcar

    Returns:
        (int, int): posición en x e y del centro
    """

    bbox = detection.location_data.relative_bounding_box
    h, w, _ = frame.shape
    x = int(bbox.xmin * w)
    y = int(bbox.ymin * h)
    width = int(bbox.width * w)
    height = int(bbox.height * h)

    green = (0, 255, 0)
    red = (0, 0, 255)

    cv2.rectangle(frame, (x, y), (x + width, y + height), green, 2)

    cx = x + width // 2
    cy = y + height // 2
    center = (cx, cy)
    cv2.circle(frame, center, 5, red, -1)

    return center
