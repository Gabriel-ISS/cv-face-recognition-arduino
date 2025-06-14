from typing import Tuple

from server import config


def get_commands(face_center_x: int, face_center_y: int):
    cx, cy = face_center_x, face_center_y
    # Determina comandos según la posición del rostro
    h_section = int(config.CAPTURE_WIDTH / 7)
    if cx < h_section:
        h_position = "v1"
    elif h_section <= cx < h_section * 2:
        h_position = "v2"
    elif h_section * 2 <= cx < h_section * 3:
        h_position = "v2"
    elif h_section * 3 <= cx < h_section * 4:
        h_position = "v4"
    elif h_section * 4 <= cx < h_section * 5:
        h_position = "v5"
    elif h_section * 5 <= cx < h_section * 6:
        h_position = "v6"
    else:
        h_position = "v7"

    v_section = int(config.CAPTURE_HEIGHT / 3)
    if cy < v_section:
        v_position = "h1"
    elif h_section <= cy < v_section * 2:
        v_position = "h2"
    else:
        v_position = "h3"

    return h_position, v_position