import numpy as np
import time

class FaceTracker:
    def __init__(self, distance_threshold=50.0, timeout=5.0):
        self.distance_threshold = distance_threshold  # Radio para identificar la misma cara
        self.timeout = timeout  # Tiempo en segundos para eliminar caras no detectadas
        self.faces = {}  # Diccionario para almacenar las caras

    def identify(self, point):
        current_time = time.time()
        point = np.array(point)

        # Verificar si hay caras existentes
        for face_id, (last_position, last_time) in list(self.faces.items()):
            # Calcular la distancia entre el punto actual y la última posición
            distance = np.linalg.norm(point - last_position)

            # Si la distancia es menor que el umbral, se considera la misma cara
            if distance < self.distance_threshold:
                # Actualizar la posición y el tiempo de la cara
                self.faces[face_id] = (point, current_time)
                return face_id  # Retornar el ID de la cara existente

            # Si la cara no ha sido detectada en el tiempo de espera, eliminarla
            if current_time - last_time > self.timeout:
                if hasattr(self, 'face_removed_callback'):
                    self.face_removed_callback(face_id)
                del self.faces[face_id]

        # Si no se encontró una cara existente, asignar un nuevo ID
        new_face_id = len(self.faces)
        self.faces[new_face_id] = (point, current_time)
        return new_face_id  # Retornar el ID de la nueva cara
    
    def on_face_removed(self, function):
        """
        Permite registrar una función que se llamará cuando una cara sea eliminada.
        La función recibirá el ID de la cara eliminada como argumento.
        """
        self.face_removed_callback = function
