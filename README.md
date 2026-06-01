# Static Site Generator

A zero-dependency static site generator written in Python. Converts Markdown content into a static HTML website using only the Python standard library.

## Features

- Parses Markdown into HTML: headings, bold, italic, inline code, links, images, unordered lists, ordered lists, blockquotes, and code blocks
- Recursive directory processing mirrors content structure in output
- HTML template injection with `{{ Title }}` and `{{ Content }}` placeholders
- Static asset copying (CSS, images, etc.)
- No external dependencies
- Nested inline formatting support (e.g., bold within italic)
- Code blocks preserve internal Markdown verbatim

## Project Structure

```
.
|-- src/              Source code
|   |-- main.py              Entry point
|   |-- utils.py             File operations
|   |-- htmlnode.py          Base HTML node class
|   |-- leafnode.py          Leaf HTML elements
|   |-- parentnode.py        Parent HTML elements (children)
|   |-- textnode.py          Text node and type enum
|   |-- text_to_html.py      TextNode to HTML conversion
|   |-- markdown_parser.py   Markdown block and inline parser
|-- static/           Static assets (copied to public/)
|   |-- index.css
|   |-- images/
|-- content/          Markdown source files
|   |-- index.md
|   |-- contact/index.md
|   |-- blog/
|-- template.html     HTML template with placeholders
|-- tests/            Unit tests
|-- main.sh           Build and serve script
|-- test.sh           Test runner script
```

## Getting Started

**Prerequisites:** Python 3.x

Build the site:

```
python3 src/main.py
```

Preview locally:

```
python3 -m http.server 8888 --directory public
```

Or run both steps with:

```
bash main.sh
```

Run tests:

```
bash test.sh
```

Or directly:

```
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

## Template System

The file `template.html` uses `{{ Title }}` and `{{ Content }}` placeholders. The generator extracts the first `<h1>` from each Markdown file as the title and replaces the placeholders with the rendered HTML.

## License

This project is for educational purposes.
