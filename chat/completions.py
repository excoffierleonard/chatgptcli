import os
import json
from openai import OpenAI

def load_settings():
    config_path = os.path.join(os.path.expanduser('~'), '.gpt', 'settings.json')
    if not os.path.exists(config_path):
        print("Settings file not found, creating a default settings file.")
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        default_settings = {
          "model": "gpt-4",
          "frequency_penalty": None,
          "logit_bias": None,
          "logprobs": None,
          "top_logprobs": None,
          "max_tokens": None,
          "n": None,
          "presence_penalty": None,
          "response_format": None,
          "seed": None,
          "stop": None,
          "stream": None,
          "temperature": None,
          "top_p": None,
          "tools": None,
          "tool_choice": None,
          "user": None
        }
        with open(config_path, 'w') as config_file:
            json.dump(default_settings, config_file, indent=4)
        return default_settings
    else:
        with open(config_path, 'r') as config_file:
            settings = json.load(config_file)
        return settings

def chat_with_gpt(settings):
    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
    chat_history = []

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break

        messages = chat_history + [{"role": "user", "content": user_input}]
        response = client.chat.completions.create(
            messages=messages,
            **settings  # Unpack settings as additional keyword arguments
        )

        chat_history.append({"role": "user", "content": user_input})
        chat_response = response.choices[0].message.content
        print("GPT: ", chat_response)
        chat_history.append({"role": "system", "content": chat_response})

if __name__ == "__main__":
    settings = load_settings()
    chat_with_gpt(settings)
