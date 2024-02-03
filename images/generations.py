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

def create_option_menu(label, default, *options):
    tk.Label(root, text=f"{label}:").pack()
    var = tk.StringVar(value=default)
    option_menu = tk.OptionMenu(root, var, *options)
    option_menu.pack()
    return var, option_menu

def create_spinbox(label, from_, to, state):
    tk.Label(root, text=f"{label}:").pack()
    spinbox = tk.Spinbox(root, from_=from_, to=to, state=state)
    spinbox.pack()
    return spinbox

# Function to check the prompt and enable/disable the generate button
def check_prompt(event):
    prompt_content = prompt_text.get("1.0", "end-1c").strip()
    if prompt_content:
        generate_button.config(state=tk.NORMAL)
    else:
        generate_button.config(state=tk.DISABLED)

# Function to handle model selection changes and restrict n=1 if DALL-E 3 is chosen
def update_gui_based_on_model(*args):
    model = model_var.get()

    quality_option_menu['menu'].entryconfig("standard", state="normal")
    response_format_var.set("url")
    response_format_option_menu['menu'].entryconfig("url", state="normal")
    response_format_option_menu['menu'].entryconfig("b64_json", state="disabled")
    size_var.set("1024x1024")
    size_option_menu['menu'].entryconfig("1024x1024", state="normal")
    style_option_menu['menu'].entryconfig("vivid", state="normal")

    if model == "dall-e-2":
        n_spinbox.config(state="normal", values=tuple(range(1, 11)))

        quality_var.set("standard")
        quality_option_menu['menu'].entryconfig("hd", state="disabled")

        size_option_menu['menu'].entryconfig("256x256", state="normal")
        size_option_menu['menu'].entryconfig("512x512", state="normal")
        size_option_menu['menu'].entryconfig("1024x1792", state="disabled")
        size_option_menu['menu'].entryconfig("1792x1024", state="disabled")

        style_var.set("vivid")

        style_option_menu['menu'].entryconfig("natural", state="disabled")

    if model == "dall-e-3":
        n_spinbox.config(state="readonly", value=(1))

        quality_option_menu['menu'].entryconfig("hd", state="normal")

        size_option_menu['menu'].entryconfig("256x256", state="disabled")
        size_option_menu['menu'].entryconfig("512x512", state="disabled")
        size_option_menu['menu'].entryconfig("1024x1792", state="normal")
        size_option_menu['menu'].entryconfig("1792x1024", state="normal")

        style_option_menu['menu'].entryconfig("natural", state="normal")

# Check if any arguments were provided for CLI mode
if cli_mode:
    cli(args)
else:
    root = tk.Tk()
    root.title("OpenAI Image Generator")

    tk.Label(root, text="Prompt:").pack()
    prompt_text = tk.Text(root)
    prompt_text.pack()
    prompt_text.bind("<KeyRelease>", check_prompt)

    model_var, model_option_menu = create_option_menu("Model", "dall-e-2", "dall-e-2", "dall-e-3")
    model_var.trace('w', update_gui_based_on_model)

    n_spinbox = create_spinbox("Number of Images", 1, 10, "readonly")

    quality_var, quality_option_menu = create_option_menu("Quality", "standard", "standard", "hd")

    response_format_var, response_format_option_menu = create_option_menu("Response Format", "url", "url", "b64_json")

    size_var, size_option_menu = create_option_menu("Size", "1024x1024", "256x256", "512x512", "1024x1024", "1024x1792", "1792x1024")

    style_var, style_option_menu = create_option_menu("Style", "vivid", "vivid", "natural")

    tk.Label(root, text="User:").pack()
    user_entry = tk.Entry(root)
    user_entry.pack()

    generate_button = tk.Button(root, text="Generate Image", command=gui)
    generate_button.pack()
    generate_button.config(state=tk.DISABLED)

    update_gui_based_on_model()

    root.mainloop()

