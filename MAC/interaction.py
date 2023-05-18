"""
Code to interact with the backend.
"""

import io
import json

import numpy as np
from .common import Team
import requests
import cv2 as cv

SERVER_URL = f"http://codabyte.com.au:8085"

endpoint = lambda e: f'{SERVER_URL}/{e}'

def fetch_ocr_task() -> np.array:
    # Get the team
    team: dict = Team.load().to_dict()

    # Write request to server
    resp = requests.post(endpoint("t1/retrieve"), json=team)

    # resp_bio = io.BytesIO(resp.content)

    resp_np = np.frombuffer(resp.content, np.uint8)

    # Create numpy array for grayscale image
    return cv.imdecode(resp_np, cv.IMREAD_GRAYSCALE)

def submit_ocr_result(result: str) -> None:
    # Get the team
    payload: dict = Team.load().to_dict()

    # Include submission in payload
    payload['submission'] = result

    # Send it off to the server
    resp = requests.post(endpoint("t1/submit"), json=payload)

def submit_drawing(image: np.array) -> None:
    # Get the team
    payload: dict = Team.load().to_dict()

    jpg_bytes = np.array(cv.imencode(".jpg", image)[1]).tobytes()
    
    #requests.post(endpoint("t3/submit"), json=payload)

    files = {
         'json': ("json", json.dumps(payload), 'application/json'),
         'file': ("file", jpg_bytes, 'application/octet-stream')
    }

    requests.post(endpoint("t3/submit"), files=files, json=payload)
