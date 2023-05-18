"""
Project 1: Optical Character Recognition
"""

from PIL import Image
from MAC.interaction import fetch_ocr_task, submit_ocr_result
import cv2 as cv
import numpy as np
import easyocr

# Get OCR image
ocr_image = fetch_ocr_task()

# Show image using CV library
cv.imshow("OCR Image", ocr_image)
cv.waitKey(0)

# Determine text using OCR
reader = easyocr.Reader(['en'])
detected = reader.readtext(ocr_image, detail=0)

# Print and submit OCR result
result = " ".join(detected)
print(f"Detected: {result}")
submit_ocr_result(result)
