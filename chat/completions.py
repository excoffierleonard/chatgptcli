import json
import os

from datetime import datetime
from openai import OpenAI
from pathlib import Path
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from rich.console import Console
from rich.markdown import Markdown

def load_settings():
    config_path = Path.home() / '.chatgpt' / 'settings.json'
    if not config_path.exists():
        print("\033[94mSettings file not found, creating default settings file...\033[0m")
        config_path.parent.mkdir(parents=True, exist_ok=True)
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

def save_chat_history(chat_history):
    timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    filename = f"chat_history_{timestamp}.json"
    log_folder = Path.home() / '.chatgpt' / 'log'
    if not log_folder.exists():
        print("\033[94\nmLog folder not found, creating a log folder...\033[0m")
        log_folder.mkdir(parents=True)
    save_path = log_folder / filename
    with open(save_path, 'w') as file:
        json.dump(chat_history, file, indent=4)
    print(f"\033[94m\nChat history saved to: \033[92m{save_path}\033[0m")

def multiline_input(prompt_text='\033[96m\nYou:\033[0m'):
    session = PromptSession()
    bindings = KeyBindings()

    @bindings.add('c-p')
    def _(event):
        event.app.exit(result=session.default_buffer.document.text)

    print(prompt_text)
    text = session.prompt('', multiline=True, key_bindings=bindings)
    return text

def process_streamed_response(response, chat_history, console):
    streamed_response_content = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            streamed_response_content += content
            print(content, end="", flush=True)
    if streamed_response_content:
        chat_history.append({"role": "system", "content": streamed_response_content})
        print("\033[91m\n----Mardown Rendering Begining---\033[0m")
        console.clear()
        console.print(Markdown(streamed_response_content))

def handle_response(response, chat_history, settings, console):
    if settings.get("stream", False):
        process_streamed_response(response, chat_history, console)
    else:
        content = response.choices[0].message.content
        console.print(Markdown(content))
        chat_history.append({"role": "system", "content": content})

def chat_with_gpt(settings):
    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
    console = Console()
    chat_history = []

    try:
        while True:
            user_input = multiline_input()
            chat_history.append({"role": "user", "content": user_input})
            messages = chat_history
            response = client.chat.completions.create(messages=messages, **settings)
            print("\033[94m\nChatGPT:\033[0m")
            handle_response(response, chat_history, settings, console)
    finally:
        if chat_history:
            save_chat_history(chat_history)

def start_screen(settings):
        print("\033[94mWelcome to ChatGPT, How can I help you today? \n\nCurrent settings:\033[0m")
        for key, value in settings.items():
            print(f"\033[93m{key}:\033[0m ", end="")
            if value is not None:
                print(f"\033[92m{value}\033[0m")
            else:
                print(value)
        print("\033[94m\n(Ctrl+P to send prompt.)\033[0m")

def main():
    try:
        settings = load_settings()
        start_screen(settings)
        chat_with_gpt(settings)
    except KeyboardInterrupt:
        print("\033[91m\nSession ended by user.\033[0m")
    except Exception as e:
        print(f"\033[91m\nAn unexpected error occurred: {e}\033[0m")
    finally:
        print("\033[94mGoodbye!\033[0m")

if __name__ == "__main__":
    main()
