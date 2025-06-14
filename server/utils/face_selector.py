import time
from typing import List, Union
from server.utils.face import Face

class FaceSelector:
    min_time_to_change = 0.5  # Minimum time in seconds to change the face being tracked
    last_selected_face: int = 0
    last_selected_time: float = 0.0


    def select_face(self, faces: List[Face]) -> Union[Face, None]:
        """
        Selects the face to track based on the largest area.
        If no faces are detected, returns None.
        """
        if not faces:
            return None

        # Find the face with the largest area
        largest_face = max(faces, key=lambda face: face.width * face.height)

        if self.last_selected_face == largest_face.id:
            return largest_face
        
        self.last_selected_face = largest_face.id
        current_time = time.time()
        if current_time - self.last_selected_time < self.min_time_to_change:
            for face in faces:
                if face.id == self.last_selected_face:
                    # If the last selected face is still present, return it
                    self.last_selected_time = current_time
                    return face
            
        self.last_selected_time = current_time
        return largest_face