# --------------------------------PYTHON IMPORTS--------------------------------#
import cv2
import numpy as np

# ------------------------------ LOCAL IMPORTS ------------------------------ #
from .image_resolution_handler import resize_image
from .image_filter_handler import (
    apply_saturation_filter,
    apply_sharpen_filter,
    apply_brightness_filter,
)


def process_image(
    image: np.array,
    width: int = 1000,
    height: int = 1000,
    saturation: int = 5,
    brightness: int = 10,
) -> bytes:
    """
    Processes the input image by resizing and applying filters.

    Args:
        image (np.array): The input image in BGR format.
        width (int, optional): The desired width of the resized image. Defaults to 1000.
        height (int, optional): The desired height of the resized image. Defaults to 1000.
        saturation (int, optional): The saturation level to apply. Defaults to 5.
        brightness (int, optional): The brightness level to apply. Defaults to 10.

    Returns:
        bytes: The processed image encoded as JPEG in byte format.
    """
    # Resize the image
    image = resize_image(image, width, height)

    # Apply the filters
    image = apply_saturation_filter(image, saturation)
    image = apply_brightness_filter(image, brightness)
    image = apply_sharpen_filter(image)

    # Encode the image
    _, image = cv2.imencode(".jpg", image)

    return image.tobytes()
