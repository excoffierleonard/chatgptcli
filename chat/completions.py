import os
import json

from openai import OpenAI
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from rich.console import Console
from rich.markdown import Markdown

console = Console()

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

def print_markdown(text, style=None, end=None):
    """Prints text with Markdown styling."""
    if style:
        console.print(Markdown(text), style=style, end=end)
    else:
        console.print(Markdown(text))

def multiline_input(prompt_text='\nYou:'):
    session = PromptSession()
    bindings = KeyBindings()

    @bindings.add('c-p')
    def _(event):
        event.app.exit(result=session.default_buffer.document.text)

    print_markdown(prompt_text, style="cyan")
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
                        print_markdown("\nChatGPT:", style="blue")
                        first_chunk = False
                    console.print(content, end="")
                    streamed_response_content += content
            if streamed_response_content:
                chat_history.append({"role": "system", "content": streamed_response_content})
            print()
        else:
            print_markdown("\nChatGPT:", style="blue")
            chat_response = response.choices[0].message.content
            console.print(chat_response)  # Directly print to handle non-Markdown
            chat_history.append({"role": "system", "content": chat_response})

def main():
    try:
        settings = load_settings()
        print_markdown("Welcome to ChatGPT, How can I help you today? \n\nCurrent settings:", style="blue")
        for key, value in settings.items():
            print_markdown(f"{key}: ", style="yellow", end="")
            if value is not None:
                print_markdown(str(value), style="green")
            else:
                print(value)
        print("\n(Ctrl+P to send prompt.)")
        chat_with_gpt(settings)
    except KeyboardInterrupt:
        print_markdown("\nExiting program. Goodbye!", style="red")
    except Exception as e:
        print_markdown(f"\nAn unexpected error occurred: {e}", style="red")

if __name__ == "__main__":
    main()
