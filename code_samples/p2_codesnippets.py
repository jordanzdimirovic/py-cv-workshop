import cv2 as cv
import numpy as np

# This frame could come from the camera...
frame: np.array(...)

# Create a binary mask based on boundaries
# cv.inRange will set each pixel to 1 if the values are
# within the specified range, and 0 otherwise

# Note that you need to match the colour model
# that is used in the frame!
lower_boundary = np.array([0, 0, 0])
upper_boundary = np.array([255, 255, 255])

binary_mask = cv.inRange(frame, lower_boundary, upper_boundary)

################################################################

# Convert an image using a certain model to another model
# Example: convert binary (grayscale) to blue-green-red
coloured_mask = cv.cvtColor(binary_mask, cv.COLOR_GRAY2BGR)

################################################################

# Draw a circle on an image
# Note: color must be in same color model as the frame
# Thickness is neasured in pixels
cv.circle(coloured_mask, center=(20, 20), radius=10, color=(200, 0, 230), thickness=5)
