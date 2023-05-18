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

# Determine text using OCR

# Print and submit OCR result using submit_ocr_result
