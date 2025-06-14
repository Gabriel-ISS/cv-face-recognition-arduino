from typing import Tuple

import cv2


class Face:
    id = -1
    x: int
    y: int
    width: int
    height: int
    center_x: int
    center_y: int

    rectangle_color: Tuple[int, int, int] = (0, 255, 0)  # Green

    def __init__(self, detection, frame_size: Tuple[int, int]):
        bbox = detection.location_data.relative_bounding_box
        w, h = frame_size
        x = int(bbox.xmin * w)
        y = int(bbox.ymin * h)
        width = int(bbox.width * w)
        height = int(bbox.height * h)

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.center_x = x + width // 2
        self.center_y = y + height // 2

    def mark(self, frame):
        """Dibuja el rostro detectado en el fotograma."""
        x = self.x
        y = self.y
        width = self.width
        height = self.height

        # BGR colors for rectangle and center point
        green = (0, 255, 0)
        red = (0, 0, 255)

        cv2.rectangle(frame, (x, y), (x + width, y + height), green, 2)

        center = (self.center_x, self.center_y)
        cv2.circle(frame, center, 5, red, -1)

    def mark_from_center(
        self,
        frame,
        rectangle_color: Tuple[int, int, int] = (0, 255, 0),
    ):
        """Dibuja el rostro detectado en el fotograma desde un centro dado."""
        x = self.center_x - self.width // 2
        y = self.center_y - self.height // 2

        # BGR colors for rectangle and center point
        red = (0, 0, 255)

        cv2.rectangle(
            frame, (x, y), (x + self.width, y + self.height), rectangle_color, 2
        )

        cv2.circle(frame, (self.center_x, self.center_y), 5, red, -1)

        if self.id is not None:
            top = self.center_x - (self.width // 2)
            left = self.center_y - (self.height // 2)

            cv2.putText(
                frame,
                f"ID: {self.id}",
                (top, left),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                1,
            )
