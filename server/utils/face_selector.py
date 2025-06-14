from typing import List, Union
from server.utils.face import Face


def select_face(faces: List[Face]) -> Union[Face, None]:
    """
    Selects the face to track based on the largest area.
    If no faces are detected, returns None.
    """
    if not faces:
        return None

    # Find the face with the largest area
    largest_face = max(faces, key=lambda face: face.width * face.height)
    
    return largest_face