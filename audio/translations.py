import os
from openai import OpenAI

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

client = OpenAI(api_key=OPENAI_API_KEY)

audio_file = open("speech.mp3", "rb")

transcript = client.audio.translations.create(
  file=audio_file,
  model="whisper-1",
  prompt="",
  response_format="json",
  temperature=0.0
)

print(transcript)