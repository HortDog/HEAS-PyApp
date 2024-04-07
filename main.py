import random
import tkinter as tk
import os
import time
import json
import urllib.request
import PIL.Image
import google.generativeai as genai
from google.cloud import speech
import speech_recognition as sr
import requests
from pydub import AudioSegment
from pydub.playback import play
import keyboard

existing_photo_files = os.listdir('Class_Photos')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'application_default_credentials.json'

#Wav URL information
wav_url = 'http://192.168.137.196:81/mic'
wav_output_file = 'audio_stream.wav'

recording_confirmation_file = 'Record_condition.txt'
capture_confirmation_file = 'Capture.txt'
recording = False

# Set the API key for the generative AI
GENERATIVEAI_API_KEY = 'AIzaSyDl6MHrxXPqXc5gfVArkdlgX9Nf0b9zzZ4'
genai.configure(api_key=(GENERATIVEAI_API_KEY))

# using the vision model to interpret an image, this will return the text interpretation of the image
SELECTED_MODEL = 'gemini-pro-vision'
model_vis = genai.GenerativeModel(SELECTED_MODEL)
print('\n' + "USING: " + SELECTED_MODEL)

SELECTED_MODEL = 'gemini-pro'
model_text = genai.GenerativeModel(SELECTED_MODEL)
print('\n' + "USING: " + SELECTED_MODEL)


def take_photo():
  capta = urllib.request.urlopen('http://192.168.137.196/capture')
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


def play_wav():
    song = AudioSegment.from_wav(wav_output_file)
    play(song)


def speech_to_text(audio_data: bytes) -> str:
    '''
        A function which converts an audio input into the text spoken within it.

        Parameters:

            audio_data: The audio input. (bytes)

        Returns: (str)

            The words spoken in the audio.
    '''
    config = speech.RecognitionConfig(
        encoding = speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code="en",
    )
    audio = speech.RecognitionAudio(content=audio_data)

    client = speech.SpeechClient()

    text_translation = client.recognize(config=config, audio=audio)

    return text_translation


def generate_question(audio_data: bytes) -> str:
    '''
        A control function which sends an audio input to speech to text and combines the text translations from it.

        Parameters:

            audio_data: The audio input. (bytes)

        Returns: (str)

            The combined text translation spoken across the full audio.
    '''
    print('translation started')
    text_translation = speech_to_text(audio_data)
    print('translation complete')

    full_question = ''

    for result in text_translation.results:
        full_question += result.alternatives[0].transcript
    
    return full_question


def check_recording():
    with open(recording_confirmation_file, 'r') as file:
        if file.read() == 'True': return True
    return False


def record_wav():
    # Open a file to write the stream data
    with open(wav_output_file, 'wb') as f:
        # Send a request to get the stream
        with requests.get(wav_url, stream=True) as r:
            start_time = time.time()
            # Read chunks of the stream and write to the file
            for chunk in r.iter_content(chunk_size=1024):
                recording = check_recording()
                # Check if the duration has been reached
                if not recording:
                    break
                f.write(chunk)


while True:
  # replace with ui
  # check = input("Do you want to take a photo? (y/n): ")
  # if check == 'y':
  #   take_photo()

  with open(capture_confirmation_file, 'r') as file:
    if file.read() == 'a': take_photo()

  with open(capture_confirmation_file, 'w') as file:
    file.write('')
    file.close()

  new_files = check_new_files(existing_photo_files)
  existing_photo_files = os.listdir('Class_Photos')
#  print(str(new_files) + '\n')

  if new_files != []:
    for filename in new_files:
      img = PIL.Image.open(os.path.join('Class_Photos', filename))
      # Mirror the image horizontally
      img = img.transpose(PIL.Image.FLIP_LEFT_RIGHT)

      try:
        response = model_vis.generate_content(["what is written in the image?, and give a short summary", img])
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

  recording = check_recording()
  if recording:
    record_wav()

    with open(wav_output_file, 'rb') as audio_file: content = audio_file.read()

    user_input = generate_question(content) # Replace content with the Audio data from the web

    # if user_input.lower() == 'end loop': break
    if user_input:
      try:
        transcript = 'User:' + '\n' + user_input + '\n' + '\n'
        print("User:", user_input)

        response = model_text.generate_content(user_input)

        transcript += 'Gemini:' + '\n' + response.text + '\n'
        print("Gemini: ")
        print(response.text)
        
        with open('data.json', 'r') as f:
          data = json.load(f)
          print(data)
          data['conversation'].append({
            user_input : response.text
          })
        with open('data.json', 'w') as f:
          json.dump(data, f, indent=2)

        print('\n')
        with open('audio_transcript.txt', 'a') as file:
            file.write(transcript)
            file.close()
      except:
        print('Error, please try again.')
      play_wav()

  if keyboard.is_pressed('space'):
    print("Spacebar is pressed!")
    break

    # Load the image and send it to the AI
    # Read data.json as a text file
with open('data.json', 'r') as file:
  data = file.read()
  # Send the data to the AI
  response = model_text.generate_content('Summerize this as class notes, give a 200 word summery of info' + str(data))
  # Print the response
print(response.text)
# Save the response to a text file called "SUMMARY.txt"
with open('SUMMARY.txt', 'w') as file:
  file.write(response.text)