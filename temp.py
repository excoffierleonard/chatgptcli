from rich.console import Console
from rich.markdown import Markdown

# Initialize a rich console
console = Console()

# Your markdown string
markdown_text = """
# Heading 1
## Heading 2
### Heading 3

This is some **bold** text and *italic* text.

- Item 1
- Item 2
- Item 3

[Link to Google](https://www.google.com)
"""

# Render Markdown
markdown = Markdown(markdown_text)

# Print the Markdown
console.print(markdown)
