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


def record_wav():
    # Duration to capture the stream (in seconds)
    duration = 10

    # Open a file to write the stream data
    with open(wav_output_file, 'wb') as f:
        # Send a request to get the stream
        with requests.get(wav_url, stream=True) as r:
            start_time = time.time()
            # Read chunks of the stream and write to the file
            for chunk in r.iter_content(chunk_size=1024):
                # Check if the duration has been reached
                if time.time() - start_time > duration:
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


ear = sr.Recognizer()
ear.pause_threshold = 0.6

chat = model.start_chat()
with open('audio_transcript.txt', 'w') as file:
    file.write('')
    file.close()
while True:

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