import os
import json

from openai import OpenAI
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings

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

def print_colored(text, color, end="\n"):
    colors = {
        "white": "\033[97m",
        "red": "\033[91m",
        "green": "\033[92m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "yellow": "\033[93m",
        "cyan": "\033[96m",
    }
    end_color = "\033[0m"
    if color in colors:
        print(f"{colors[color]}{text}{end_color}", end=end)
    else:
        print(text, end=end)

def multiline_input(prompt_text='\nYou:'):
    session = PromptSession()
    bindings = KeyBindings()

    @bindings.add('c-p')
    def _(event):
        event.app.exit(result=session.default_buffer.document.text)

    print_colored(prompt_text, "cyan")
    text = session.prompt('', multiline=True, key_bindings=bindings)
    return text

def chat_with_gpt(settings):
    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
    chat_history = []

    while True:
        user_input = multiline_input()

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
                        print_colored("\nChatGPT:", "blue")
                        first_chunk = False
                    print(content, end="")
                    streamed_response_content += content
            if streamed_response_content:
                chat_history.append({"role": "system", "content": streamed_response_content})
            print()
        else:
            print_colored("\nChatGPT:", "blue")
            chat_response = response.choices[0].message.content
            print(chat_response)
            chat_history.append({"role": "system", "content": chat_response})

def main():
    try:
        settings = load_settings()
        print_colored("Welcome to ChatGPT, How can I help you today? \n\nCurrent settings:", "blue")
        for key, value in settings.items():
            print_colored(f"{key}: ", "yellow", end="")
            if value is not None:
                print_colored(value, "green")
            else:
                print(value)
        print("\n(Ctrl+P to send prompt.)")
        chat_with_gpt(settings)
    except KeyboardInterrupt:
        print_colored("\nExiting program. Goodbye!", "red")
    except Exception as e:
        print_colored(f"\nAn unexpected error occurred: {e}", "red")

if __name__ == "__main__":
    main()
