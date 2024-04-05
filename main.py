import PIL.Image
import google.generativeai as genai

# Set the API key for the generative AI
GENERATIVEAI_API_KEY = 'AIzaSyDl6MHrxXPqXc5gfVArkdlgX9Nf0b9zzZ4'
genai.configure(api_key=(GENERATIVEAI_API_KEY))

# Lists the modes of AI we can access
for m in genai.list_models():
  if 'generateContent' in m.supported_generation_methods:
    print(m.name)

# Select the model to use, needs to be one of the models listed above
SELECTED_MODEL = 'gemini-pro'
model = genai.GenerativeModel(SELECTED_MODEL)
print('\n' + "UESING: " + SELECTED_MODEL)

# Generate content, sending the prompt to the AI
response = model.generate_content("Hello")

# Get the text of the response
print(response.text)
print('\n')

# Get the prompt feedback, which is the AI's interpretation of the prompt
print(response.prompt_feedback)
print('\n')

# Get the list of candidates, which are the possible completions of the prompt
##print(response.candidates)
##print('\n')

# generate content, sending the prompt to the AI, and streaming the response, this is useful for large responses as it will stream the response in chunks
##response = model.generate_content("What is the meaning of life?", stream=True)
##for chunk in response:
##  print(chunk.text, end='', flush=True)

# using the vision model to interpret an image, this will return the text interpretation of the image
SELECTED_MODEL = 'gemini-pro-vision'
model = genai.GenerativeModel(SELECTED_MODEL)
print('\n' + "UESING: " + SELECTED_MODEL)

img = PIL.Image.open('hello_image.png')
response = model.generate_content(["what is witen in the image?", img])
print(response.text)


SELECTED_MODEL = 'gemini-pro'
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