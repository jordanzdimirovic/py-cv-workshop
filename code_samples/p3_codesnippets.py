import cv2 as cv
import numpy as np
from MAC.mediapipe import draw_landmarks_on_image, get_landmark

# Get the pixel position of a landmark, given by an ID
# You can find the landmark positions here:
# https://developers.google.com/mediapipe/solutions/vision/hand_landmarker
# The is_close value is a boolean indicating if the landmark is close (enough) to the camera
# Use the closeness offset to tweak this to whatever you'd like

detection_results = ...
cam_resolution = 480, 640

pixel, is_close = get_landmark(detection_results, 8, cam_resolution, closeness_offset=0)

# Draw the landmarks (using Google's provided visualisation approach)
frame_from_camera = ...
frame_with_landmarks = draw_landmarks_on_image(frame_from_camera, detection_results)
