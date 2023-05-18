import pyttsx3 as tts
import easyocr

################################################################
# Create an easyocr reader for English text
reader = easyocr.Reader(['en'])

# Detect text in image
image = ...
detected: list = reader.readtext(image, detail=0)

################################################################

# Initialise speech engine
engine = tts.init()

# Make the speech slower
engine.setProperty('rate',145)

# Tell engine to say some text
engine.say("Hello world!")

# Start playing (blocking call)
engine.runAndWait()
