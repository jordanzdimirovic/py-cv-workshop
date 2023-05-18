"""
Project 2: Object Tracking
"""

import cv2 as cv
import numpy as np
from MAC.helpers import key_is_pressed, filter_stray_pixels, keyboard_hsv_mod

HSV_LOWER = [0, 0, 0] # Min HSV value for masking
HSV_UPPER = [180, 255, 255] # Max HSV value for masking

"""
https://docs.opencv.org/4.x/df/d9d/tutorial_py_colorspaces.html#:~:text=For%20HSV%2C%20hue%20range%20is%20%5B0%2C179%5D
"""


def get_mask(camera_frame: np.ndarray, lower_bound: tuple, upper_bound: tuple) -> np.ndarray:
    """
    Calculates a binary mask from a camera frame, given a lower and upper bound.
    """
    raise NotImplementedError()


def get_centroid(mask: np.ndarray, pixel_threshold: int = 200) -> np.ndarray:
    """
    Given a binary mask, calculates the central position.
    """
    # Use this if you get lots of noise
    # filter_stray_pixels(mask, pixel_threshold)
    raise NotImplementedError()

def create_color_preview() -> np.ndarray:
    preview_hsv = np.concatenate(
        (np.full((50, 250, 3), tuple(HSV_LOWER), dtype=np.uint8),
         np.full((50, 250, 3), tuple(HSV_UPPER), dtype=np.uint8)),
        axis=1,
        dtype=np.uint8
    )

    return cv.cvtColor(preview_hsv, cv.COLOR_HSV2BGR)

###########
# Cam loop
###########

cam = cv.VideoCapture(0)
col_preview = create_color_preview()

while True:
    success, frame = cam.read()
    if success:
        mask = get_mask(frame, HSV_LOWER, HSV_UPPER)

        coloured_mask = cv.cvtColor(mask, cv.COLOR_GRAY2BGR)

        # Get centroid
        center = get_centroid(mask)

        # Draw circle at centroid TODO

        cv.imshow("Normal", frame)
        cv.imshow("Mask", coloured_mask)
        cv.imshow("Color Preview", col_preview)

    ##############################################################

    # Color change using keyboard
    changed = keyboard_hsv_mod((HSV_LOWER, HSV_UPPER))

    if changed:
        col_preview = create_color_preview()
        print(f"Lower bound: {HSV_LOWER} | Upper bound: {HSV_UPPER}")

    if key_is_pressed('escape'):
        break
