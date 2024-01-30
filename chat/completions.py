import os
from openai import OpenAI

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

client = OpenAI(api_key=OPENAI_API_KEY)

completion = client.chat.completions.create(
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
  ],  
  model="gpt-4",
  frequency_penalty=0.0,
  logit_bias={},
  logprobs=False,
  top_logprobs=None,
  max_tokens=None,
  n=1,
  presence_penalty=0.0,
  response_format={"type": "text"},
  seed=0,
  stop=None,
  stream=False,
  temperature=1.0,
  top_p=1.0,  
  tools=[{"type": "function", "function": {"description": "description", "name": "name", "parameters": {}}}],
  tool_choice="none",
  user=""
)

print(completion.choices[0].message)