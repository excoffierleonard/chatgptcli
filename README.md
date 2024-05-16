# ChatGPT CLI

ChatGPT CLI is a command-line interface for interacting with OpenAI's latest text models using customizable settings and streamlined multi-line input. It allows for saving and restoring chat history, modifying settings, and handling different user commands seamlessly.

## Features

- Multi-line input with `Ctrl+P` to send the message
- Streamed and non-streamed responses from ChatGPT
- Save chat history to timestamped files
- Restore and reprint previous chat histories
- Modify and save settings dynamically
- Customizable system prompt (preprompt)
- Built-in help and command handling

## Requirements

- Python 3.x
- Openai
- Prompt Toolkit
- Rich

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/excoffierleonard/chatgptcli.git
   cd chatgptcli
   ```

2. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

### Environment Variables

Set up the OpenAI API key in your environment variables:

```bash
export OPENAI_API_KEY='your-openai-api-key'
```

## Usage

### Running the Program

Run the Program:

```bash
python main.py
```

When the program starts, it will display a welcome message along with the current settings.

### Basic Commands

Here are the available commands:

- `/h` or `/help`: Display the help message
- `/q` or `/quit`: Quit the program
- `/c` or `/clear`: Clear the screen
- `/s` or `/settings`: Open settings to view or modify them
- `/r` or `/restore`: Restore chat history from a file
- `/p` or `/preprompt`: Modify the system prompt

### Multi-line Input

To enter a multi-line input, start typing and press `Ctrl+P` to send the message.

### Customizing Settings

To modify the settings, use the `/s` or `/settings` command, and follow the prompts to change the settings.

### Changing System Prompt

To change the system prompt, use the `/p` or `/preprompt` command and enter the new prompt.

### Chat History

- **Save**: The chat history is automatically saved to a file in the `~/.chatgptcli/log` directory with a timestamp.

- **Restore**: Use the `/r` or `/restore` command to restore a previous chat history.

### Error Handling

The program handles interruptions and unexpected errors gracefully, ensuring that the chat history is saved before exiting.

## Example

```
Welcome to ChatGPT, How can I help you today?

Current settings:
model: gpt-4
frequency_penalty: None
logit_bias: None
logprobs: None
top_logprobs: None
max_tokens: None
n: None
presence_penalty: None
response_format: None
seed: None
stop: None
stream: None
temperature: None
top_p: None
tools: None
tool_choice: None
user: None

/h, /help: Displays the available commands.

Ctrl+P to send a prompt.

No System Prompt Loaded.

You:
Hello, how are you?

ChatGPT:
As an artificial intelligence, I do not have feelings, but thank you for asking! How can I assist you today?

You:


Session ended by user.

Chat history saved to: /Users/el/.chatgptcli/log/2024-05-16-17-49-46-hello,_how_are_you_.json

Goodbye!
```

## How It Works

ChatGPT CLI is designed to provide an easy-to-use command-line interface for interacting with OpenAI's model. Here's a brief explanation of its workflow:

### Initialization

- **Loading Settings**: When the application starts, it loads settings from `~/.chatgptcli/settings.json`. If the file doesn't exist, it creates one with default settings.
- **Loading System Prompt**: The system prompt, if available, is loaded from `~/.chatgptcli/system_prompt.json` and added to the chat history.

### User Interaction

- **Multi-line Input**: The CLI allows multi-line input, letting users compose their query over multiple lines. The input is sent when the user presses `Ctrl+P`.
- **Commands**: Users can issue commands by starting their input with a `/`. For example, `/help` to display available commands.

### Generating Responses

- **Sending Messages**: User inputs are sent to the OpenAI's model using the loaded settings. The program can handle both streamed and non-streamed responses.
- **Displaying Responses**: Responses from OpenAI's model are displayed in the console with support for Markdown rendering, providing a rich text experience.

### Saving and Restoring

- **Saving Chat History**: Chat history is automatically saved to a timestamped JSON file in `~/.chatgptcli/log` when the session ends.
- **Restoring Chat History**: Users can restore previous chat sessions using the `/restore` command. The saved chat history can be reprinted and continued.

### Customization

- **Settings**: Users can view and modify the application's settings in real-time using the `/settings` command.
- **System Prompt**: The system prompt can be changed using the `/preprompt` command, allowing users to set a new precondition for the model.

This basic workflow ensures a smooth and user-friendly interaction with the powerful model directly from your terminal.

## Possible Improvements

### 1. Fix Save on Close Not Ctrl+C

Improve the program to ensure chat history is saved even when the script is closed normally, not just when interrupted with Ctrl+C.

### 2. Dynamic Markdown Formatting

Enhance the Markdown rendering to adjust dynamically with window resize and handle copy-pasting properly.

### 3. Stop Prompt Generation Midway

Introduce a function that allows users to stop the prompt generation in the middle of the process.

### 4. Description for Settings

Add detailed descriptions for each setting, making it easier for users to understand and modify them.

### 5. Improved User Command and Preprompt Formatting

Improve formatting to make prompt texts clearer when the user is asked for commands or preprompt entries.

### 6. Enhanced `reprint_chat_history` Function

Update the `reprint_chat_history` function to ensure that system prompts are correctly rendered.

### 7. Enhanced `change_settings` Function

Enhance the `change_settings` function by adding checks and validations to ensure new settings values are valid and sensible.

### 8. Correct Handling of `\n\n`

Ensure that double newlines (`\n\n`) are correctly handled in user inputs and system responses.

### 9. Validate Settings and OpenAI API Key

Implement validation checks for both settings and the OpenAI API key to make sure they meet requirements before proceeding with their usage.

### 10. Early Stream Break Shortcut

Add a shortcut to allow users to break the streaming of responses early without exiting the program.

## Contribution

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/excoffierleonard/chatgptcli/issues).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgements

This project uses the following libraries:

- `openai`
- `prompt_toolkit`
- `rich`
- `datetime`
- `json`
- `re`
- `pathlib`
- `os`
- `sys`

---

**Note**: Replace `'your-openai-api-key'` with your actual OpenAI API key.
