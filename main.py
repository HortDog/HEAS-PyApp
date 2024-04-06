import random
import tkinter as tk
import os
import time
import json
import urllib.request
import PIL.Image
import google.generativeai as genai

existing_photo_files = os.listdir('Class_Photos')

# Set the API key for the generative AI
GENERATIVEAI_API_KEY = 'AIzaSyDl6MHrxXPqXc5gfVArkdlgX9Nf0b9zzZ4'
genai.configure(api_key=(GENERATIVEAI_API_KEY))

# using the vision model to interpret an image, this will return the text interpretation of the image
SELECTED_MODEL = 'gemini-pro-vision'
model = genai.GenerativeModel(SELECTED_MODEL)
print('\n' + "UESING: " + SELECTED_MODEL)


def take_photo():
  capta = urllib.request.urlopen('http://192.168.137.214/capture')
# extract image from request
  img = PIL.Image.open(capta)
# display image
  img.show()
# Save the image to Class_Photos directory in the current directory
  current_directory = os.getcwd()
  name = 'Photo_' + str(random.randint(1, 1000000)) + '.jpg'
  print(name)
  img.save(os.path.join(current_directory, 'Class_Photos', name))

  # Check if a new file was added to Class_Photos directory

def check_new_files(existing_photo_files):
  new_files = []
  for filename in os.listdir('Class_Photos'):
    if filename.endswith('.jpg') and filename not in existing_photo_files:
      new_files.append(filename)
  if new_files:
    print("New files added to Class_Photos directory:")
    return new_files
  else:
    return []
  #  print("No new files added to Class_Photos directory.")
  #print('Live Check complete' + '\n')

while True:
  check = input("Do you want to take a photo? (y/n): ")
  if check == 'y':
    take_photo()

  new_files = check_new_files(existing_photo_files)
  existing_photo_files = os.listdir('Class_Photos')
#  print(str(new_files) + '\n')

  if new_files != []:
    for filename in new_files:
      img = PIL.Image.open(os.path.join('Class_Photos', filename))
      # Mirror the image horizontally
      img = img.transpose(PIL.Image.FLIP_LEFT_RIGHT)

      try:
        response = model.generate_content(["what is written in the image?, and give a short summary", img])
        print(response.text)
        print('\n')
      except:
        print("An error occurred while processing the image.")
        continue

      with open('data.json', 'r') as f:
        data = json.load(f)
      print(data)
      data['Photo_Descriptions'].append({
        filename : response.text
        })
      with open('data.json', 'w') as f:
        json.dump(data, f, indent=2)

  # Delay for 2 seconds
  time.sleep(2)






# # Load the image and send it to the AI
# response = model.generate_content(["what is written in the image?, and give a short summary", img])

# # Loop through Class_Photos directory
# for filename in os.listdir('Class_Photos'):
#   if filename.endswith('.jpg'):
#     # Load the image and send it to the AI
#     img = PIL.Image.open(os.path.join('Class_Photos', filename))
#     response = model.generate_content(["what is written in the image?", img])
#     print(response.text)



# # chat with the AI, it will keep responding to the user input and remember the context of the conversation
# chat = model.start_chat()
# while True:
#   user_input = input("You: ")
  
#   response = chat.send_message(user_input, stream=True)
#   print("Gemini: ")
#   for chunk in response:
#     print(chunk.text, end='', flush=True)
  
#   print('\n')