import os,binascii
import cv2 as cv, numpy as np

clamp = lambda x, l, u: max(l, min(u, x))

def get_key_pressed() -> str:
    res = cv.waitKey(1) & 0xFF
    if res == 49: return "space"
    elif res == 13: return "enter"
    elif res == 27: return "escape"
    return chr(res)

def key_is_pressed(key) -> bool:
    if key == "space": key = 49
    elif key == "enter": key = 13
    elif key == "escape": key = 27 
    elif type(key) is str: key = ord(key)
    return cv.waitKey(1) & 0xFF == key


def random_str(len: int):
    """Produce a random string of *approximately* `len` characters."""
    return binascii.b2a_hex(os.urandom(len // 2)).decode('ascii')


def filter_stray_pixels(mask: np.ndarray, pixel_threshold: int):
    """Removes pixel blobs that don't satisfy the threshold."""
    # Convert mask to binary image
    binary_image = np.uint8(mask)

    # Perform connected component analysis
    num_labels, labels, stats, _ = cv.connectedComponentsWithStats(binary_image, connectivity=8)

    # Iterate over the components (excluding background component)
    for label in range(1, num_labels):
        # Filter out components based on pixel count
        if stats[label, cv.CC_STAT_AREA] < pixel_threshold:
            # Set pixels of the stray component to black (0)
            mask[labels == label] = 0

KEYBOARD_HSV_MAPPING = {
    't': (0, 0, -3, 0, 180),
    'y': (0, 0, 3, 0, 180),
    'u': (0, 1, -3, 0, 255),
    'i': (0, 1, 3, 0, 255),
    'o': (0, 2, -3, 0, 255),
    'p': (0, 2, 3, 0, 255),
    'f': (1, 0, -3, 0, 180),
    'g': (1, 0, 3, 0, 180),
    'h': (1, 1, -3, 0, 255),
    'j': (1, 1, 3, 0, 255),
    'k': (1, 2, -3, 0, 255),
    'l': (1, 2, 3, 0, 255)
}

def keyboard_hsv_mod(collection):
    k = chr(cv.waitKey(1) & 0xFF)
    if k in KEYBOARD_HSV_MAPPING:
        polarity, idx, incr, lwr, upr = KEYBOARD_HSV_MAPPING[k]
        collection[polarity][idx] = clamp(round(collection[polarity][idx] + incr, 3), lwr, upr)
        return True
    
    return False

COLOURS = [("red", (0,0,255)),("blue", (255,0,0)),("green", (0,255,0)),("yellow", (0,255,255)),("purple", (255,0,255))]
colour_idx = 0

def colour_picker(nxt: bool) -> tuple:
    global colour_idx
    """Returns True if colour changed"""
    if nxt:
        colour_idx = (colour_idx + 1) % len(COLOURS)
        print(f"Colour picked: {COLOURS[colour_idx][0]}")
    
    return COLOURS[colour_idx][1]
