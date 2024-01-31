import argparse
import tkinter as tk
from tkinter import messagebox
import webbrowser
import os
from openai import OpenAI

# Function to generate the image using the OpenAI API
def api(prompt, model, n, quality, response_format, size, style, user):
    try:
        # Initialize OpenAI client
        OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
        client = OpenAI(api_key=OPENAI_API_KEY)

        # Call the OpenAI API with the provided arguments
        response = client.images.generate(
            prompt=prompt,
            model=model,
            n=n,
            quality=quality,
            response_format=response_format,
            size=size,
            style=style,
            user=user
        )

        image_url = response.data[0].url
        return image_url
    except Exception as e:
        return f"Error: {str(e)}"

# GUI Function
def gui():
    result = api(
        prompt_entry.get(),
        model_var.get(),
        int(n_entry.get()),
        quality_var.get(),
        response_format_var.get(),
        size_var.get(),
        style_var.get(),
        user_entry.get()
    )
    if result.startswith("http"):
        messagebox.showinfo("Success", "Image generated successfully.")
        webbrowser.open(result)
    else:
        messagebox.showerror("Error", result)

# Function for CLI
def cli(args):
    result = api(
        args.prompt,
        args.model,
        args.n,
        args.quality,
        args.response_format,
        args.size,
        args.style,
        args.user
    )
    if result.startswith("http"):
        print("Success: Image URL:", result)
    else:
        print(result)

# Parse CLI Arguments
parser = argparse.ArgumentParser(description='Generate images using OpenAI.')
parser.add_argument('-p', '--prompt', type=str, help='A text description of the desired image.')
parser.add_argument('-m', '--model', type=str, default='dall-e-2', choices=['dall-e-2', 'dall-e-3'], help='The model to use for image generation.')
parser.add_argument('-n', type=int, default=1, choices=range(1, 11), help='The number of images to generate.')
parser.add_argument('-q', '--quality', type=str, default='standard', choices=['standard', 'hd'], help='The quality of the image.')
parser.add_argument('-rf', '--response_format', type=str, default='url', choices=['url', 'b64_json'], help='The format in which the images are returned.')
parser.add_argument('-s', '--size', type=str, default='1024x1024', choices=['256x256', '512x512', '1024x1024', '1792x1024', '1024x1792'], help='The size of the generated images.')
parser.add_argument('-st', '--style', type=str, default='vivid', choices=['vivid', 'natural'], help='The style of the generated images.')
parser.add_argument('-u', '--user', type=str, default='', help='A unique identifier representing your end-user.')

args = parser.parse_args()

# Check if any CLI argument is provided and different from default
cli_mode = False
for arg in vars(args):
    if getattr(args, arg) is not None and getattr(args, arg) != parser.get_default(arg):
        cli_mode = True
        break

# Check if any arguments were provided for CLI mode
if cli_mode:
    cli(args)
else:
    # Initialize Tkinter for GUI mode
    root = tk.Tk()
    root.title("OpenAI Image Generator")

    # Prompt
    tk.Label(root, text="Prompt:").pack()
    prompt_entry = tk.Entry(root)
    prompt_entry.pack()

    # Model
    tk.Label(root, text="Model:").pack()
    model_var = tk.StringVar(value="dall-e-2")
    tk.OptionMenu(root, model_var, "dall-e-2", "dall-e-3").pack()

    # Number of Images
    tk.Label(root, text="Number of Images:").pack()
    n_entry = tk.Entry(root)
    n_entry.pack()

    # Quality
    tk.Label(root, text="Quality:").pack()
    quality_var = tk.StringVar(value="standard")
    tk.OptionMenu(root, quality_var, "standard", "hd").pack()

    # Response Format
    tk.Label(root, text="Response Format:").pack()
    response_format_var = tk.StringVar(value="url")
    tk.OptionMenu(root, response_format_var, "url", "b64_json").pack()

    # Size
    tk.Label(root, text="Size:").pack()
    size_var = tk.StringVar(value="1024x1024")
    tk.OptionMenu(root, size_var, "256x256", "512x512", "1024x1024", "1792x1024", "1024x1792").pack()

    # Style
    tk.Label(root, text="Style:").pack()
    style_var = tk.StringVar(value="vivid")
    tk.OptionMenu(root, style_var, "vivid", "natural").pack()

    # User
    tk.Label(root, text="User:").pack()
    user_entry = tk.Entry(root)
    user_entry.pack()

    # Generate Button for GUI
    generate_button = tk.Button(root, text="Generate Image", command=gui)
    generate_button.pack()

    # Run the GUI application
    root.mainloop()