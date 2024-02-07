import os
from openai import OpenAI

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

client = OpenAI(api_key=OPENAI_API_KEY)

completion = client.chat.completions.create(
  messages=[{"role": "user", "content": "Hello!"}],
  model="gpt-4",
  frequency_penalty=None,
  logit_bias=None,
  logprobs=None,
  top_logprobs=None,
  max_tokens=None,
  n=None,
  presence_penalty=None,
  response_format=None,
  seed=None,
  stop=None,
  stream=None,
  temperature=None,
  top_p=None,  
  tools=None,
  tool_choice=None,
  user=None
)

'''
messages=messages,
model=model,
frequency_penalty=frequency_penalty,
logit_bias=logit_bias,
logprobs=logprobs,
top_logprobs=top_logprobs,
max_tokens=max_tokens,
n=n,
presence_penalty=presence_penalty,
response_format=response_format,
seed=seed,
stop=stop,
stream=stream,
temperature=temperature,
top_p=top_p,
tools=tools,
tool_choice=tool_choice,
user=user
'''

print(completion.choices[0].message.content)