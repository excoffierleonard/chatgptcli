import sys
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

class CLI:
    def run_cli():
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

class GUI:
    def __init__(self, root):
        self.root = root
        self.setup_gui()

    def setup_gui(self):
        self.root.title("OpenAI Image Generator")
        
        self.root.grid_columnconfigure(1, weight=1)

        self.prompt_text = self.create_text("Prompt:", 0)
        self.model_var, self.model_option_menu = self.create_option_menu("Model:", "dall-e-2", ["dall-e-2", "dall-e-3"], row=1)
        self.n_spinbox = self.create_spinbox("Number of Images:", 1, 10, "readonly", 2)
        self.quality_var, self.quality_option_menu = self.create_option_menu("Quality:", "standard", ["standard", "hd"], row=3)
        self.response_format_var, self.response_format_option_menu = self.create_option_menu("Response Format:", "url", ["url", "b64_json"], row=4)
        self.size_var, self.size_option_menu = self.create_option_menu("Size:", "1024x1024", ["256x256", "512x512", "1024x1024", "1024x1792", "1792x1024"], row=5)
        self.style_var, self.style_option_menu = self.create_option_menu("Style:", "vivid", ["vivid", "natural"], row=6)
        self.user_entry = self.create_entry("User:", 7)
        self.generate_button = self.create_button("Generate Image:", self.generate_images, 8)
        
        self.prompt_text.bind("<KeyRelease>", self.check_prompt)
        self.model_var.trace_add("write", self.update_gui_based_on_model)
        
        self.check_prompt()
        self.update_gui_based_on_model()

    def create_text(self, text, row):
        tk.Label(self.root, text=text).grid(row=row, column=0, sticky='e')
        text = tk.Text(self.root, height=10, width=50)
        text.grid(row=row, column=1, pady=10, sticky='nsew', columnspan=2)
        return text

    def create_option_menu(self, text, default, options, row):
        tk.Label(self.root, text=text).grid(row=row, column=0, sticky='e')
        var = tk.StringVar(value=default)
        option_menu = tk.OptionMenu(self.root, var, *options)
        option_menu.grid(row=row, column=1, pady=10, sticky='w')
        return var, option_menu

    def create_spinbox(self, text, from_, to, state, row):
        tk.Label(self.root, text=text).grid(row=row, column=0, sticky='e')
        spinbox = tk.Spinbox(self.root, from_=from_, to=to, state=state, width=15)
        spinbox.grid(row=row, column=1, pady=10, sticky='w')
        return spinbox

    def create_entry(self, text, row):
        tk.Label(self.root, text=text).grid(row=row, column=0, sticky='e')
        entry = tk.Entry(self.root)
        entry.grid(row=row, column=1, pady=10, sticky='w')
        return entry

    def create_button(self, text, command, row):
        button = tk.Button(self.root, text=text, command=command)
        button.grid(row=row, column=0, pady=10, columnspan=2)
        return button

    def check_prompt(self, *event):
        prompt_content = self.prompt_text.get("1.0", "end-1c").strip()
        if prompt_content:
            self.generate_button.config(state=tk.NORMAL)
        else:
            self.generate_button.config(state=tk.DISABLED)

    def update_gui_based_on_model(self, *args):
        model = self.model_var.get()

        self.quality_option_menu['menu'].entryconfig("standard", state="normal")
        self.response_format_var.set("url")
        self.response_format_option_menu['menu'].entryconfig("url", state="normal")
        self.response_format_option_menu['menu'].entryconfig("b64_json", state="disabled")
        self.size_var.set("1024x1024")
        self.size_option_menu['menu'].entryconfig("1024x1024", state="normal")
        self.style_option_menu['menu'].entryconfig("vivid", state="normal")

        if model == "dall-e-2":
            self.n_spinbox.config(values=tuple(range(1, 11)))

            self.quality_var.set("standard")
            self.quality_option_menu['menu'].entryconfig("hd", state="disabled")

            self.size_option_menu['menu'].entryconfig("256x256", state="normal")
            self.size_option_menu['menu'].entryconfig("512x512", state="normal")
            self.size_option_menu['menu'].entryconfig("1024x1792", state="disabled")
            self.size_option_menu['menu'].entryconfig("1792x1024", state="disabled")

            self.style_var.set("vivid")

            self.style_option_menu['menu'].entryconfig("natural", state="disabled")

        if model == "dall-e-3":
            self.n_spinbox.config(value=(1))

            self.quality_option_menu['menu'].entryconfig("hd", state="normal")

            self.size_option_menu['menu'].entryconfig("256x256", state="disabled")
            self.size_option_menu['menu'].entryconfig("512x512", state="disabled")
            self.size_option_menu['menu'].entryconfig("1024x1792", state="normal")
            self.size_option_menu['menu'].entryconfig("1792x1024", state="normal")

            self.style_option_menu['menu'].entryconfig("natural", state="normal")
    
    def generate_images(self):
        try:
            result = api(
                self.prompt_text.get("1.0", "end-1c"),
                self.model_var.get(),
                int(self.n_spinbox.get()),
                self.quality_var.get(),
                self.response_format_var.get(),
                self.size_var.get(),
                self.style_var.get(),
                self.user_entry.get()
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
                prompt = self.prompt_text.get("1.0", "end-1c")
                messagebox.showinfo("Success", f"Image(s) generated successfully.\n\nPrompt:\n\n{prompt}")

        except Exception as e:
            messagebox.showerror("Error", e)

    def run_gui():
        root = tk.Tk()
        GUI(root)
        root.mainloop()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        CLI.run_cli()
    else:
        GUI.run_gui()