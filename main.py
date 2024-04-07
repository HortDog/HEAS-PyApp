import os#, PIL.Image
import google.generativeai as genai
from google.cloud import speech
# from pathlib import Path
import speech_recognition as sr
# from IPython.display import Audio
import requests, time
from pydub import AudioSegment
from pydub.playback import play

# Set the API key for the generative AI
GENERATIVEAI_API_KEY = 'AIzaSyDl6MHrxXPqXc5gfVArkdlgX9Nf0b9zzZ4'
genai.configure(api_key=(GENERATIVEAI_API_KEY))
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'application_default_credentials.json'

SELECTED_MODEL = 'gemini-pro'
model = genai.GenerativeModel(SELECTED_MODEL)
print('\n' + "USING: " + SELECTED_MODEL)

#Wav URL information
wav_url = 'http://192.168.137.252:81/mic'
wav_output_file = 'audio_stream.wav'
recording_confirmation_file = 'Record_condition.txt'
recording = False


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

    # print(f'Stream saved to {output_file}')


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


def summarise_chat(chat: list) -> str:
    '''
        Summarises the contents of the chat session/class.

        Parameters:

            chat: The history of the conversation between the students and the AI. (List)

        Returns: (str)

            The summary of the conversation.
    '''
    summary = "Summarise the following conversation", str(chat.history)
    response = model.generate_content(summary)

    return response.text


chat = model.start_chat()
with open('audio_transcript.txt', 'w') as file:
    file.write('')
    file.close()
while True:
    # with sr.Microphone() as source2:
    #     ear.adjust_for_ambient_noise(source2, duration=0.5)
    #     content = ear.listen(source2).get_raw_data()

    recording = check_recording()
    while not recording:
        recording = check_recording()
    record_wav()

    with open(wav_output_file, 'rb') as audio_file: content = audio_file.read()

    user_input = generate_question(content) # Replace content with the Audio data from the web

    # if user_input.lower() == 'end loop': break
    if user_input:
        try:
            transcript = 'User:' + '\n' + user_input + '\n' + '\n'
            print("User:", user_input)

            response = chat.send_message(user_input, stream=True)

            transcript += 'Gemini:' + '\n'
            print("Gemini: ")
            for chunk in response:
                if chunk.text:
                    transcript += chunk.text
                    print(chunk.text, end='', flush=True)

            transcript += '\n' + '\n'
            print('\n')
            with open('audio_transcript.txt', 'a') as file:
                file.write(transcript)
                file.close()
        except:
            print('Error, please try again.')
        play_wav()


# ear = sr.Recognizer()
# ear.pause_threshold = 0.6

# chat with the AI, it will keep responding to the user input and remember the context of the conversation

# print(summarise_chat(chat.history))


### Horton's Old Preview Code ###

# Select the model to use, needs to be one of the models listed above
# SELECTED_MODEL = 'gemini-pro'
# model = genai.GenerativeModel(SELECTED_MODEL)
# print('\n' + "USING: " + SELECTED_MODEL)

# Generate content, sending the prompt to the AI
# response = model.generate_content("Hello")

# Get the text of the response
# print(response.text)
# print('\n')

# Get the prompt feedback, which is the AI's interpretation of the prompt
# print(response.prompt_feedback)
# print('\n')

# Get the list of candidates, which are the possible completions of the prompt
# print(response.candidates)
# print('\n')

# generate content, sending the prompt to the AI, and streaming the response, this is useful for large responses as it will stream the response in chunks
# response = model.generate_content("What is the meaning of life?", stream=True)
# for chunk in response:
#     print(chunk.text, end='', flush=True)

# using the vision model to interpret an image, this will return the text interpretation of the image
# SELECTED_MODEL = 'gemini-pro-vision'
# model = genai.GenerativeModel(SELECTED_MODEL)
# print('\n' + "USING: " + SELECTED_MODEL)

# Load the image and send it to the AI
# img = PIL.Image.open('hello_image.png')
# response = model.generate_content(["what is written in the image?", img])
# print(response.text)


# SELECTED_MODEL = 'gemini-pro'
# model = genai.GenerativeModel(SELECTED_MODEL)
# print('\n' + "USING: " + SELECTED_MODEL)

# chat with the AI, it will keep responding to the user input and remember the context of the conversation
# chat = model.start_chat()
# while True:
#     user_input = input("You: ")
  
#     response = chat.send_message(user_input, stream=True)
#     print("Gemini: ")
#     for chunk in response:
#         print(chunk.text, end='', flush=True)
  
#     print('\n')


## Speech to Text ##

# def speech_to_text(
#     config: speech.RecognitionConfig,
#     audio: speech.RecognitionAudio,
# ) -> speech.RecognizeResponse:
#     client = speech.SpeechClient()

#     # Synchronous speech recognition request
#     response = client.recognize(config=config, audio=audio)

#     return response


# def print_response(response: speech.RecognizeResponse):
#     for result in response.results:
#         print_result(result)


# def print_result(result: speech.SpeechRecognitionResult):
#     best_alternative = result.alternatives[0]
#     print("-" * 80)
#     print(f"language_code: {result.language_code}")
#     print(f"transcript:    {best_alternative.transcript}")
#     print(f"confidence:    {best_alternative.confidence:.0%}")


# with open('hello_audio.mp3', 'rb') as audio_file:
#     content = audio_file.read()

# config = speech.RecognitionConfig(
#     encoding = speech.RecognitionConfig.AudioEncoding.MP3,
#     sample_rate_hertz=16000,
#     language_code="en",
# )
# audio = speech.RecognitionAudio(content=content)

# response = speech_to_text(config, audio)
# print_response(response)


## Alternative Speech to Text ##

# import speech_recognition as sr

# # initialize the recognizer
# ear = sr.Recognizer()

# with sr.AudioFile('hello_audio.wav') as source:
#     # listen for the data (load audio to memory)
#     audio_data = ear.record(source)
#     # recognize (convert from speech to text)
#     text = ear.recognize_google_cloud(audio_data)
#     print(text)


### CODE GRAVEYARD ###

# import speech_recognition as sr
# from IPython.display import Audio

# ear = sr.Recognizer()

# while(1):    
     
#     # Exception handling to handle
#     # exceptions at the runtime
#     try:
         
#         # use the microphone as source for input.
#         with sr.Microphone() as source2:
#             ear.adjust_for_ambient_noise(source2, duration=0.2)
#             audio2 = ear.listen(source2)

#             print(ear.recognize_google_cloud(audio2, GOOGLE_APPLICATION_CREDENTIALS))
             
#     except sr.RequestError as e:
#         print("Could not request results; {0}".format(e))
         
#     except sr.UnknownValueError:
#         print("unknown error occurred")


# import vertexai

# from vertexai.generative_models import GenerativeModel, Part

# # Initialize Vertex AI
# vertexai.init(project='heas-419409', location='australia-southeast1')
# # Load the model
# vision_model = GenerativeModel("gemini-1.0-pro-vision")
# # Generate text
# response = vision_model.generate_content(
#     [
#         Part.from_uri(
#             "gs://cloud-samples-data/video/animals.mp4", mime_type="video/mp4"
#         ),
#         "What is in the video?",
#     ]
# )
# print(response.text)
