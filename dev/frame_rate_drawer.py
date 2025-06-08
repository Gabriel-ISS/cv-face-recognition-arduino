import time
import cv2


class FrameRateDrawer:
    """Clase para mostrar el fotograma por segundo (FPS) en la ventana de video"""

    frames_count = 0

    def __init__(
        self,
        position: tuple[int, int] = (10, 30),
        color: tuple[int, int, int] = (0, 255, 0),
    ):
        self.position = position
        self.color = color
        self.fps = 0
        self.start_time = time.time()

    def update(self, frame):
        """Actualiza el FPS y lo muestra en el fotograma"""
        self.frames_count += 1
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        if elapsed_time >= 1.0:  # Actualiza cada segundo
            self.fps = self.frames_count
            self.start_time = current_time
            self.frames_count = 0

        cv2.putText(
            frame,
            f"FPS: {self.fps:.2f}",
            self.position,
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            self.color,
            2,
        )
