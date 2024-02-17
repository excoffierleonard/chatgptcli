import json
import os
import re
import sys

from datetime import datetime
from openai import OpenAI
from pathlib import Path
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from rich.console import Console
from rich.markdown import Markdown

# Global variables
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
settings = {}
chat_history = []
console = Console()

# Loads chat configuration from a .chatgpt/settings.json file or creates one with default settings if it doesn't exist.
def load_settings():
    global settings
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
        settings = default_settings
    else:
        with open(config_path, 'r') as config_file:
            settings = json.load(config_file)
    return settings

# Sanitizes the message to remove any characters that are illegal in filenames.
def sanitize_message(message):
    illegal_char_replacement = "_"
    illegal_chars_pattern = r"[ <>:\"/\\|?*\n\r\t]"

    lower_message = message.lower()

    sanitized_message = re.sub(illegal_chars_pattern, illegal_char_replacement, lower_message)
    return sanitized_message

# Saves the chat history to a timestamped file in the .chatgpt/log directory.
def save_chat_history():
    global chat_history

    first_user_message = next((message["content"] for message in chat_history if message.get("role") == "user"), None)

    if first_user_message:
        sanitized_message = sanitize_message(first_user_message)[:64]
        timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        filename = f"{timestamp}-{sanitized_message}.json"
        log_folder = Path.home() / '.chatgpt' / 'log'
        if not log_folder.exists():
            print(f"\033[94\nmLog folder not found, creating: \033[92m{log_folder}\033[0m")
            log_folder.mkdir(parents=True)
        save_path = log_folder / filename
        with open(save_path, 'w') as file:
            json.dump(chat_history, file, indent=4)
        print(f"\033[94m\nChat history saved to: \033[92m{save_path}\033[0m")
    else:
        print("\033[94m\nChat history empty. Nothing to save.\033[0m")

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

# Command to quit the program.
def quit_program():
    print("\033[91m\nSession ended by user.\033[0m")
    sys.exit()

def clear_screen():
    global console
    console.clear()

# Command to interact with the settings.
def change_settings():
    global settings

    print("\033[94m\nCurrent settings:\033[0m")
    for key, value in settings.items():
        print(f"\033[93m{key}:\033[0m ", end="")
        if value is not None:
            print(f"\033[92m{value}\033[0m")
        else:
            print(value)

    setting_to_change = input("\033[94m\nEnter the setting you want to change (or 'exit' to cancel):\033[0m ")
    if setting_to_change.lower() == 'exit':
        print("\033[94mSettings change cancelled.\033[0m")
        return
    
    if setting_to_change not in settings:
        print(f"\033[91mSetting \033[93m{setting_to_change}\033[91m not found.\033[0m")
        return

    new_value = input(f"\033[94mEnter the new value for \033[93m{setting_to_change}\033[94m:\033[0m ")

    if new_value.lower() in ['true', 'false']:
        new_value_converted = new_value.lower() == 'true'
    else:
        try:
            new_value_converted = int(new_value)
        except ValueError:
            try:
                new_value_converted = float(new_value)
            except ValueError:
                new_value_converted = new_value

    settings[setting_to_change] = new_value_converted
    print(f"\033[94mSetting \033[93m{setting_to_change}\033[94m updated to \033[92m{new_value_converted}\033[94m. \033[0m")

    config_path = Path.home() / '.chatgpt' / 'settings.json'
    with open(config_path, 'w') as config_file:
        json.dump(settings, config_file, indent=4)

# Reprints the chat history.
def reprint_chat_history(chat_history):

    print("\033[93m\nRestored Chat Session:\033[0m")

    for message in chat_history:
        if message["role"] == "user":
            print("\033[96m\nYou:\033[0m")
            print(f"{message['content']}")
        elif message["role"] == "system":
            print("\033[94m\nChatGPT:\033[0m")
            print(f"{message['content']}")
            print("\033[91m----Mardown Rendering Begining---\033[0m")
            console.print(Markdown(f"{message['content']}"))

# Restores chat history.
def restore_chat_history():
    global chat_history
    log_folder = Path.home() / '.chatgpt' / 'log'

    if log_folder.exists() and any(log_folder.iterdir()):
        chat_files = sorted(log_folder.iterdir(), key=os.path.getctime, reverse=True)[:16]

        if chat_files:
            print("\033[94m\nSelect a chat history to restore:\033[0m")
            for index, file in enumerate(chat_files, start=1):
                filename = os.path.basename(file)
                print(f"\033[93m{index}: \033[92m{filename}\033[0m")

            selected_index = input("\033[94m\nEnter the number of the chat history to restore (or 'exit' to cancel):\033[0m ")
            if selected_index.lower() == 'exit':
                print("\033[94m\nRestoration cancelled.\033[0m")
                return

            try:
                selected_index = int(selected_index) - 1
                if 0 <= selected_index < len(chat_files):
                    with open(chat_files[selected_index], 'r') as file:
                        chat_history = json.load(file)
                    reprint_chat_history(chat_history)
                    print("\033[94m\nChat history restored successfully.\033[0m")
                else:
                    print("\033[91m\nInvalid selection. Please select a number listed above.\033[0m")
            except ValueError:
                print("\033[91m\nPlease enter a valid number.\033[0m")
        else:
            print("\033[91m\nNo chat history files available to restore.\033[0m")
    else:
        print("\033[91m\nNo chat history folder found.\033[0m")

# Command to display on unknow commands.
def unknown_command(cmd):
    print(f"Unknown command: {cmd}")

# Handles commands from the user
def handle_command(cmd):
    commands = {
    "/q": quit_program,
    "/quit": quit_program,
    "/c": clear_screen,
    "/clear": clear_screen,
    "/s" : change_settings,
    "/settings": change_settings,
    "/r": restore_chat_history,
    "/restore": restore_chat_history,
    }

    if cmd in commands:
        commands[cmd]()
    else:
        unknown_command(cmd)

# Handles user interaction with ChatGPT, sending inputs and showing responses based on specified settings.
def chat_with_gpt():
    global client
    global console
    global chat_history
    global settings

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
        chat_with_gpt()
    except KeyboardInterrupt:
        quit_program()
    except Exception as e:
        print(f"\033[91m\nAn unexpected error occurred: {e}\033[0m")
        input("\033[94mPress Enter to exit...\033[0m")
    finally:
        save_chat_history()
        print("\033[94m\nGoodbye!\033[0m")

if __name__ == "__main__":
    main()
