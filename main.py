import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import Image, Audio

GOOGLE_API_KEY='AIzaSyDl6MHrxXPqXc5gfVArkdlgX9Nf0b9zzZ4'

genai.configure(api_key=GOOGLE_API_KEY)


## Lists the modes of AI we can access ##
# for m in genai.list_models():
#   if 'generateContent' in m.supported_generation_methods:
#     print(m.name)


## Code that can successfully receive responses from the AI ##
# model = genai.GenerativeModel('gemini-pro')
# response = model.generate_content("What is the meaning of life?")
# print(response.text)


## Code that can successfully receive text interpretations of images from the AI ##
# model = genai.GenerativeModel("gemini-pro-vision")
# img = Image(filename='hello_image.png')
# response = model.generate_content(["What is this image?", img])
# print(response.text)


## Code to try and receive text interpretations of audio from the AI ##
from vertexai.generative_models import Part

model = genai.GenerativeModel("gemini-pro")
response = model.generate_content([Part.from_uri("hello_audio.mp3", mime_type="video/mp3"),"What is being said in this audio?",])
print(response.text)