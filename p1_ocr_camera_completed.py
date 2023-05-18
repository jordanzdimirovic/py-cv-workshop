"""
Project 1: Optical Character Recognition (using camera)
"""

from PIL import Image
from MAC.interaction import fetch_ocr_task
import cv2 as cv
import numpy as np
import pytesseract
import easyocr
import pyttsx3 as tts
from MAC.helpers import key_is_pressed

# Open camera capture
cam = cv.VideoCapture(0)
reader = easyocr.Reader(['en'])
engine = tts.init()

# Make the speech slower
engine.setProperty('rate',145)

while True:
    success, frame = cam.read()
    if success:
        cv.imshow("Camera feed", frame)
        if key_is_pressed('enter'):
            detected = reader.readtext(frame, detail=0)
            # for d in detected:
            #     engine.say(d)
            #     engine.runAndWait()
            to_say = ' '.join(detected)
            print(to_say)
            engine.say(to_say)
            engine.runAndWait()

        elif key_is_pressed('q'):
            break
