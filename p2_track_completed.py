"""
Project 2: Object Tracking
"""

import cv2 as cv
import numpy as np
from MAC.helpers import key_is_pressed, filter_stray_pixels, keyboard_hsv_mod

HSV_LOWER = [100, 128, 60]
HSV_UPPER = [112, 140, 100]

"""
https://docs.opencv.org/4.x/df/d9d/tutorial_py_colorspaces.html#:~:text=For%20HSV%2C%20hue%20range%20is%20%5B0%2C179%5D
"""


def get_mask_better(camera_frame: np.ndarray, lower_bound: list, upper_bound: list) -> np.ndarray:
    """
    Calculates a binary mask from a camera frame, given a lower and upper bound.
    Allows for an upper bound with a lesser hue (i.e., wrap-around).
    """
    # Convert to hue-saturation-value
    hsv_frame = cv.cvtColor(camera_frame, cv.COLOR_BGR2HSV)

    # If upper bound wraps around
    if lower_bound[0] > upper_bound[0]:
        first_range = lower_bound, [180, upper_bound[1], upper_bound[2]]
        second_range = [0, lower_bound[1], lower_bound[2]], upper_bound

        # Create two masks...
        lower1, upper1 = np.array(first_range[0]), np.array(first_range[1])
        lower2, upper2 = np.array(second_range[0]), np.array(second_range[1])
        mask1, mask2 = cv.inRange(hsv_frame, lower1, upper1), cv.inRange(
            hsv_frame, lower2, upper2)

        # ... and bitwise or them together
        return cv.bitwise_or(mask1, mask2)

    else:
        # Continue as normal
        lower, upper = np.array(lower_bound), np.array(upper_bound)

        mask = cv.inRange(hsv_frame, lower, upper)

        return mask


def get_mask_simple(camera_frame: np.ndarray, lower_bound: tuple, upper_bound: tuple) -> np.ndarray:
    """
    Calculates a binary mask from a camera frame, given a lower and upper bound.
    """
    # Convert to hue-saturation-value
    hsv_frame = cv.cvtColor(camera_frame, cv.COLOR_BGR2HSV)

    # Convert the bounds to np arrays
    lower, upper = np.array(lower_bound), np.array(upper_bound)

    # Determines mask using inRange
    mask = cv.inRange(hsv_frame, lower, upper)

    return mask


def get_centroid(mask: np.ndarray) -> np.ndarray:
    """
    Given a binary mask, calculates the central position.
    """
    shape = mask.shape
    total_white = 0
    sum_x, sum_y = 0, 0
    for i in range(shape[0]):
        for j in range(shape[1]):
            if mask[i][j]:
                total_white += 1
                sum_x += j
                sum_y += i

    if total_white <= 0:
        return None
    centroid = np.array((sum_x // total_white, sum_y // total_white))
    return centroid


def create_color_preview() -> np.ndarray:
    preview_hsv = np.concatenate(
        (np.full((50, 250, 3), tuple(HSV_LOWER), dtype=np.uint8),
         np.full((50, 250, 3), tuple(HSV_UPPER), dtype=np.uint8)),
        axis=1,
        dtype=np.uint8
    )

    return cv.cvtColor(preview_hsv, cv.COLOR_HSV2BGR)

cam = cv.VideoCapture(0)

col_preview = create_color_preview()

pixel_threshold: int = 200

while True:
    success, frame = cam.read()
    if success:
        mask = get_mask_better(frame, HSV_LOWER, HSV_UPPER)

        filter_stray_pixels(mask, pixel_threshold)

        coloured_mask = cv.cvtColor(mask, cv.COLOR_GRAY2BGR)

        # Get centroid
        c = get_centroid(mask)

        # Draw circle at centroid
        if c is not None:
            cv.circle(coloured_mask, c, 20, (200, 0, 230), 5)
            cv.circle(frame, c, 20, (200, 0, 230), 5)

        cv.imshow("Normal", frame)
        cv.imshow("Mask", coloured_mask)
        cv.imshow("Color Preview", col_preview)

    changed = keyboard_hsv_mod((HSV_LOWER, HSV_UPPER))

    if changed:
        col_preview = create_color_preview()
        print(f"Lower bound: {HSV_LOWER} | Upper bound: {HSV_UPPER}")

    if key_is_pressed('escape'):
        break
