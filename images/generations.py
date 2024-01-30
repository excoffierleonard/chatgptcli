import os
import argparse
from openai import OpenAI

# Get API key
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Initialize the ArgumentParser
parser = argparse.ArgumentParser(description='Generate images using OpenAI.')

# Define arguments with validation
parser.add_argument('-p', '--prompt', type=str, required=True, help='A text description of the desired image(s). The maximum length is 1000 characters for dall-e-2 and 4000 characters for dall-e-3.')
parser.add_argument('-m', '--model', type=str, default='dall-e-2', choices=['dall-e-2', 'dall-e-3'], help='The model to use for image generation.')
parser.add_argument('-n', type=int, default=1, choices=range(1, 11), help='The number of images to generate. Must be between 1 and 10. For dall-e-3, only n=1 is supported.')
parser.add_argument('-q', '--quality', type=str, default='standard', choices=['standard', 'hd'], help='The quality of the image that will be generated. hd creates images with finer details and greater consistency across the image. This param is only supported for dall-e-3.')
parser.add_argument('-rf', '--response_format', type=str, default='url', choices=['url', 'b64_json'], help='The format in which the generated images are returned. Must be one of url or b64_json.')
parser.add_argument('-s', '--size', type=str, default='1024x1024', choices=['256x256', '512x512', '1024x1024', '1792x1024', '1024x1792'], help='The size of the generated images. Must be one of 256x256, 512x512, or 1024x1024 for dall-e-2. Must be one of 1024x1024, 1792x1024, or 1024x1792 for dall-e-3 models.')
parser.add_argument('-st', '--style', type=str, default='vivid', choices=['vivid', 'natural'], help='The style of the generated images. Must be one of vivid or natural. Vivid causes the model to lean towards generating hyper-real and dramatic images. Natural causes the model to produce more natural, less hyper-real looking images. This param is only supported for dall-e-3.')
parser.add_argument('-u', '--user', type=str, default='', help='A unique identifier representing your end-user, which can help OpenAI to monitor and detect abuse.')

# Parse arguments
args = parser.parse_args()

# Call the OpenAI API with the provided arguments
response = client.images.generate(
    prompt=args.prompt,
    model=args.model,
    n=args.n,
    quality=args.quality,
    response_format=args.response_format,
    size=args.size,
    style=args.style,
    user=args.user
)

# Print the response
print(response)