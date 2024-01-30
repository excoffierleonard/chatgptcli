import os
from pathlib import Path
from openai import OpenAI

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

client = OpenAI(api_key=OPENAI_API_KEY)

speech_file_path = Path(__file__).parent / "speech.mp3"

response = client.audio.speech.create(
  model="tts-1",
  input="Today is a wonderful day to build something people love!",
  voice="alloy",
  response_format="mp3",
  speed=1.0
)

response.write_to_file(speech_file_path)
