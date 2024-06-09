# --------------------------------PYTHON IMPORTS--------------------------------#
import cv2
import numpy as np


def apply_saturation_filter(image: np.array, saturation: int):
    """
    Applies a saturation filter to the image.

    Args:
        image (np.array): The input image in BGR format.
        saturation (int): The saturation level to apply.

    Returns:
        np.array: The image with the saturation filter applied.
    """
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv = np.array(hsv, dtype=np.float64)
    hsv[:, :, 1] = hsv[:, :, 1] * saturation
    hsv[:, :, 1][hsv[:, :, 1] > 255] = 255
    hsv = np.array(hsv, dtype=np.uint8)
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)


def apply_sharpen_filter(image: np.array):
    """
    Applies a sharpen filter to the image.

    Args:
        image (np.array): The input image in BGR format.

    Returns:
        np.array: The image with the sharpen filter applied.
    """
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    return cv2.filter2D(image, -1, kernel)


def apply_brightness_filter(image: np.array, brightness: int = 20):
    """
    Applies a brightness filter to the image.

    Args:
        image (np.array): The input image in BGR format.
        brightness (int, optional): The brightness level to apply. Defaults to 20.

    Returns:
        np.array: The image with the brightness filter applied.
    """
    return cv2.convertScaleAbs(image, beta=brightness)
