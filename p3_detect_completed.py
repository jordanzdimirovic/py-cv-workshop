"""
Project 3: Object Detection
"""

import cv2 as cv
import numpy as np

from MAC.helpers import get_key_pressed, key_is_pressed, colour_picker

import mediapipe as mp

from MAC.mediapipe import draw_landmarks_on_image, get_landmark
from MAC.interaction import submit_drawing

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode

BRUSH_SIZE = 20  # px

DRAWING_BG = (23, 17, 14)

# Define hand landmarker options
options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path='models/hand_landmarker.task'),
    running_mode=VisionRunningMode.IMAGE
)

# Create landmarker instance
landmarker = HandLandmarker.create_from_options(options)

cam = cv.VideoCapture(0)
cam_resolution = cam.read()[1].shape
drawn = np.full(cam_resolution, DRAWING_BG, dtype=np.uint8)
while True:
    key_pressed = get_key_pressed()

    success, frame = cam.read()

    # Get paint colour
    paint_colour = colour_picker(nxt=(key_pressed == 'p'))

    # Flip the frame if needed
    frame = cv.flip(frame, 1)

    if success:
        # Format image for MP
        im = mp.Image(image_format=mp.ImageFormat.SRGB,
                      data=cv.cvtColor(frame, cv.COLOR_BGR2RGB))
        det_result = landmarker.detect(im)
        preview = draw_landmarks_on_image(im.numpy_view(), det_result)

        pixel, is_close = get_landmark(
            det_result, 8, cam_resolution, closeness_offset=0)  # Change offset if needed

        # If there was a landmark extracted
        if pixel and is_close:
            # Draw gray reticle where the pixel is
            cv.circle(preview, pixel, BRUSH_SIZE, (100, 100, 100), 4)
            cv.circle(drawn, pixel, BRUSH_SIZE, paint_colour, cv.FILLED)

        cv.imshow("Preview", preview)
        cv.imshow("Drawing", drawn)

    if key_pressed == 'c':
        # Clear drawing
        drawn = np.full(cam_resolution, DRAWING_BG, dtype=np.uint8)

    elif key_pressed == 'enter':
        # Send image to server
        submit_drawing(drawn)
        print("Submitted")

    elif key_pressed == 'escape':
        break
