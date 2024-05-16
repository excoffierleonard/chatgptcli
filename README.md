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

- **Save**: The chat history is automatically saved to a file in the `.chatgptcli/log` directory with a timestamp.

- **Restore**: Use the `/r` or `/restore` command to restore a previous chat history.

### Error Handling

The program handles interruptions and unexpected errors gracefully, ensuring that the chat history is saved before exiting.

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

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributing

Feel free to fork the repository, make changes, and submit a pull request.

## Support

For any issues or feature requests, please open an issue on the GitHub repository.

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

---

Feel free to reach out for more assistance or questions. Enjoy your experience with ChatGPT CLI!
