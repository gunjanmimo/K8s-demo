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

    # resize the image
    image = resize_image(image, width, height)

    # apply the filters
    image = apply_saturation_filter(image, saturation)
    image = apply_brightness_filter(image, brightness)
    image = apply_sharpen_filter(image)

    # encode the image
    _, image = cv2.imencode(".jpg", image)

    return image.tobytes()
