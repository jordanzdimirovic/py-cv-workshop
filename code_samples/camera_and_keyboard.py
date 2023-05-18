import cv2 as cv
from MAC.helpers import get_key_pressed
import numpy as np
# Open video feed. Parameter '0' -> use webcam.
# Pro tip: you can also use a video file by providing a path
cam = cv.VideoCapture(0)

# Loop until we press 'q'
while True:
    key_pressed = get_key_pressed()
    success, frame = cam.read()
    # Only show video if retrieval was successful
    if success: 
        # Show image in window
        cv.imshow("Camera feed", frame)
        if key_pressed == 'q': # Keyboard input
            break # Exit program

import cv2 as cv
from MAC.helpers import get_key_pressed
import numpy as np
# Open video feed. Parameter '0' -> use webcam.
# Pro tip: you can also use a video file by providing a path
cam = cv.VideoCapture(0)

while True:
    success, frame = cam.read()
    
    # ... do something with the frame

    cv.imshow("Camera feed", frame)
