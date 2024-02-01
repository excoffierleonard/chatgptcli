import argparse
import tkinter as tk
from tkinter import messagebox
import webbrowser
import os
import openai
from openai import OpenAI

# Function to generate the image using the OpenAI API
def api(prompt, model, n, quality, response_format, size, style, user):
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    client = OpenAI(api_key=OPENAI_API_KEY)

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
    return response

# GUI Function
def gui():
    try:
        result = api(
            prompt_text.get("1.0", "end-1c"),
            model_var.get(),
            int(n_spinbox.get()),
            quality_var.get(),
            response_format_var.get(),
            size_var.get(),
            style_var.get(),
            user_entry.get()
        )

        urls = []
        revised_prompts = []

        for item in result.data:
            urls.append(item.url)
            if hasattr(item, 'revised_prompt') and item.revised_prompt:
                revised_prompts.append(item.revised_prompt)

        for url in urls:
            webbrowser.open(url)

        if revised_prompts:
            all_revised_prompts = "\n\n".join(revised_prompts)
            messagebox.showinfo("Success", f"Image(s) generated successfully. \n\nRevised prompt(s):\n\n{all_revised_prompts}")
        else:
            prompt = prompt_text.get("1.0", "end-1c")
            messagebox.showinfo("Success", f"Image(s) generated successfully.\n\nPrompt:\n\n{prompt}")

    except Exception as e:
        messagebox.showerror("Error", e)

# CLI Function
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
    root = tk.Tk()
    root.title("OpenAI Image Generator")

    tk.Label(root, text="Prompt:").pack()
    prompt_text = tk.Text(root)
    prompt_text.pack()

    tk.Label(root, text="Model:").pack()
    model_var = tk.StringVar(value="dall-e-2")
    tk.OptionMenu(root, model_var, "dall-e-2", "dall-e-3").pack()

    tk.Label(root, text="Number of Images:").pack()
    n_spinbox = tk.Spinbox(root, from_=1, to=10)
    n_spinbox.pack()

    tk.Label(root, text="Quality:").pack()
    quality_var = tk.StringVar(value="standard")
    tk.OptionMenu(root, quality_var, "standard", "hd").pack()

    tk.Label(root, text="Response Format:").pack()
    response_format_var = tk.StringVar(value="url")
    tk.OptionMenu(root, response_format_var, "url", "b64_json").pack()

    tk.Label(root, text="Size:").pack()
    size_var = tk.StringVar(value="1024x1024")
    tk.OptionMenu(root, size_var, "256x256", "512x512", "1024x1024", "1792x1024", "1024x1792").pack()

    tk.Label(root, text="Style:").pack()
    style_var = tk.StringVar(value="vivid")
    tk.OptionMenu(root, style_var, "vivid", "natural").pack()

    tk.Label(root, text="User:").pack()
    user_entry = tk.Entry(root)
    user_entry.pack()

    generate_button = tk.Button(root, text="Generate Image", command=gui)
    generate_button.pack()

    root.mainloop()