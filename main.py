import tkinter as tk
import os
import urllib.request
import PIL.Image
import google.generativeai as genai

# reqest = urllib.request.urlopen('http://192.168.16.214/capture')
# # extract image from request
# img = PIL.Image.open(reqest)
# # display image
# img.show()
# # Save the image to Class_Photos directory in the current directory
# current_directory = os.getcwd()
# img.save(os.path.join(current_directory, 'Class_Photos', 'image2.jpg'))

# Set the API key for the generative AI
GENERATIVEAI_API_KEY = 'AIzaSyDl6MHrxXPqXc5gfVArkdlgX9Nf0b9zzZ4'
genai.configure(api_key=(GENERATIVEAI_API_KEY))

SELECTED_MODEL = 'gemini-pro-vision'
model = genai.GenerativeModel(SELECTED_MODEL)
print('\n' + "UESING: " + SELECTED_MODEL)

# chat with the AI, it will keep responding to the user input and remember the context of the conversation
chat = model.start_chat()
while True:
  user_input = input("You: ")
  
  response = chat.send_message(user_input, stream=True)
  print("Gemini: ")
  for chunk in response:
    print(chunk.text, end='', flush=True)
  
  print('\n')
