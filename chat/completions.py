import json
import os
import sys

from datetime import datetime
from openai import OpenAI
from pathlib import Path
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from rich.console import Console
from rich.markdown import Markdown

# Global chat_history variable
chat_history = []

# Loads chat configuration from a .chatgpt/settings.json file or creates one with default settings if it doesn't exist.
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

# Saves the chat history to a timestamped file in the .chatgpt/log directory.
def save_chat_history():
    global chat_history
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

# Allows multi-line user input, ending with Ctrl+P.
def multiline_input(prompt_text='\033[96m\nYou:\033[0m'):
    session = PromptSession()
    bindings = KeyBindings()

    @bindings.add('c-p')
    def _(event):
        event.app.exit(result=session.default_buffer.document.text)

    print(prompt_text)
    text = session.prompt('', multiline=True, key_bindings=bindings)
    return text

# Processes and displays a streamed response from ChatGPT, updating the chat history.
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

# Processes and displays a normal (non-streamed) response from ChatGPT, updating the chat history.
def process_normal_response(response, chat_history, console):
    content = response.choices[0].message.content
    chat_history.append({"role": "system", "content": content})
    console.print(Markdown(content.replace(" \n"," \n")))

# Manages the display of ChatGPT's response (streamed or not) and updates chat history.
def handle_response(response, chat_history, settings, console):
    if settings.get("stream", False):
        process_streamed_response(response, chat_history, console)
    else:
        process_normal_response(response, chat_history, console)

# Function to load system_prompt from sytem_prompt.json or create an empty one if it doesn't exist
def load_system_prompt(chat_history):
    system_prompt_path = Path.home() / '.chatgpt' / 'system_prompt.json'
    if system_prompt_path.exists():
        with open(system_prompt_path, 'r') as system_prompt_file:
            system_prompt = json.load(system_prompt_file)
    else:
        system_prompt = ""
        with open(system_prompt_path, 'w') as system_prompt_file:
            json.dump(system_prompt, system_prompt_file)
    
    if system_prompt:
        if len(system_prompt) > 64:
            truncated_prompt = system_prompt[:61] + "..."
        else:
            truncated_prompt = system_prompt
        chat_history.append({"role": "system", "content": system_prompt})
        print(f"\033[94m\nSystem: \033[92m\n{truncated_prompt}\033[0m") 
    else:
        print(f"\033[94m\nNo System Prompt Loaded.\033[0m")
    return chat_history

def quit_program():
    print("\033[91m\nSession ended by user.\033[0m")
    sys.exit()

def settings():
    print("Settings placeholder")

def unknown_command(cmd):
    print(f"Unknown command: {cmd}")

# Handles commands from the user
def handle_command(cmd):
    commands = {
    "/q": quit_program,
    "/quit": quit_program,
    "/s" : settings,
    "/settings": settings,
    }
    
    if cmd in commands:
        commands[cmd]()
    else:
        unknown_command(cmd)

# Handles user interaction with ChatGPT, sending inputs and showing responses based on specified settings.
def chat_with_gpt(settings):
    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
    console = Console()
    global chat_history

    load_system_prompt(chat_history)

    while True:
        user_input = multiline_input()

        if user_input.startswith("/"):
            handle_command(user_input)
        else:
            chat_history.append({"role": "user", "content": user_input})
            messages = chat_history
            response = client.chat.completions.create(messages=messages, **settings)
            print("\033[94m\nChatGPT:\033[0m")
            handle_response(response, chat_history, settings, console)

# Displays a welcome message and current settings at the program start.
def default_start_screen(settings):
        print("\033[94mWelcome to ChatGPT, How can I help you today? \n\nCurrent settings:\033[0m")
        for key, value in settings.items():
            print(f"\033[93m{key}:\033[0m ", end="")
            if value is not None:
                print(f"\033[92m{value}\033[0m")
            else:
                print(value)
        print("\033[94m\n(Ctrl+P to send prompt.)\033[0m")

# Entry point of the script; handles the chat session setup, execution, and graceful termination.
def main():
    try:
        settings = load_settings()
        default_start_screen(settings)
        chat_with_gpt(settings)
    except KeyboardInterrupt:
        quit_program()
    except Exception as e:
        print(f"\033[91m\nAn unexpected error occurred: {e}\033[0m")
    finally:
        save_chat_history()
        print("\033[94mGoodbye!\033[0m")

if __name__ == "__main__":
    main()
