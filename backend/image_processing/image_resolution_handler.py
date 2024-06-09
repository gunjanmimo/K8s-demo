import cv2
import numpy as np


def resize_image(image: np.array, width: int, height: int):
    return cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)
