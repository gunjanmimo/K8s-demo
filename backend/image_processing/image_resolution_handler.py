# --------------------------------PYTHON IMPORTS--------------------------------#
import cv2
import numpy as np


def resize_image(image: np.array, width: int, height: int):
    """
    Resizes the input image to the specified width and height.

    Args:
        image (np.array): The input image in BGR format.
        width (int): The desired width of the resized image.
        height (int): The desired height of the resized image.

    Returns:
        np.array: The resized image.
    """
    return cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)
