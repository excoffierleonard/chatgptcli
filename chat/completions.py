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
        print("\nYou (press Enter twice to submit): ")
        print()
        user_input_lines = []
        while True:
            line = input()
            if line == "":
                if user_input_lines:
                    break
                else:
                    continue
            user_input_lines.append(line)
        user_input = "\n".join(user_input_lines)
        print()

        if user_input.lower() == 'exit':
            break

        messages = chat_history + [{"role": "user", "content": user_input}]
        response = client.chat.completions.create(
            messages=messages,
            **settings
        )

        if settings.get("stream", False):
            streamed_response_content = ""
            first_chunk = True
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    if first_chunk:
                        print("GPT: ", end="")
                        first_chunk = False
                    print(content, end="")
                    streamed_response_content += content
            if streamed_response_content:
                chat_history.append({"role": "system", "content": streamed_response_content})
            print() 
        else:
            print("GPT: ", end="")
            chat_response = response.choices[0].message.content
            print(chat_response)
            chat_history.append({"role": "system", "content": chat_response})
            print()

def main():
    settings = load_settings()
    print()
    print("Current settings:")
    for key, value in settings.items():
        print(f"{key}: {value}")
    chat_with_gpt(settings)

if __name__ == "__main__":
    main()
