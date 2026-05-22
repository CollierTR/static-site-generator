import re
from enum import Enum, auto
from textnode import TextType, TextNode
from htmlnode import HTMLNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """Split TextNodes by a delimiter and wrap delimited sections with a new type.

    Args:
        old_nodes: List of TextNode instances to split.
        delimiter: String delimiter to split on (e.g. '**', '*').
        text_type: TextType to assign to delimited sections.

    Returns:
        List of TextNode instances with delimited sections transformed.

    Raises:
        Exception: If a matching closing delimiter is not found.
    """
    if not old_nodes:
        return []

    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node)
            continue
        split_nodes = node.text.split(delimiter)
        if len(split_nodes) % 2 == 0:
            raise Exception(f"Invalid Markdown! Unclosed '{delimiter}'!")
        else:
            for i, split in enumerate(split_nodes):
                if i % 2 == 0:
                    new_nodes.append(TextNode(split, TextType.PLAIN_TEXT))
                else:
                    new_nodes.append(TextNode(split, text_type))

    return new_nodes

def extract_markdown_images(text):
    """Extract markdown image references from text.

    Args:
        text: String containing markdown image syntax (![alt](url)).

    Returns:
        List of (alt_text, url) tuples.
    """
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    """Extract markdown link references from text (excluding images).

    Args:
        text: String containing markdown link syntax ([text](url)).

    Returns:
        List of (anchor_text, url) tuples.
    """
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches
    
def split_nodes_link(old_nodes):
    """Split TextNodes by markdown links.

    Args:
        old_nodes: List of TextNode instances to split.

    Returns:
        List of TextNode instances with links separated into LINK nodes.
    """
    if not old_nodes:
        return []

    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue

        remainder = node.text

        for link in links:
            string = re.split(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", remainder, 1)
            if string[0]:
                new_nodes.append(TextNode(string[0], TextType.PLAIN_TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            remainder = string[3]

        if remainder:
            new_nodes.append(TextNode(remainder, TextType.PLAIN_TEXT))
            

    return new_nodes
    
def split_nodes_image(old_nodes):
    """Split TextNodes by markdown images.

    Args:
        old_nodes: List of TextNode instances to split.

    Returns:
        List of TextNode instances with images separated into IMAGE nodes.
    """
    if not old_nodes:
        return []

    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node)
            continue

        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue

        remainder = node.text

        for image in images:
            string = re.split(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", remainder, 1)
            if string[0]:
                new_nodes.append(TextNode(string[0], TextType.PLAIN_TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            remainder = string[3]

        if remainder:
            new_nodes.append(TextNode(remainder, TextType.PLAIN_TEXT))
            

    return new_nodes

def text_to_textnodes(text):
    """Convert a raw markdown text string into a list of TextNodes.

    Applies delimiter splitting (code, bold, italic), then extracts
    images and links in order.

    Args:
        text: Raw markdown string.

    Returns:
        List of TextNode instances.
    """
    nodes = [TextNode(text, TextType.PLAIN_TEXT)]
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE_TEXT)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD_TEXT)
    nodes = split_nodes_delimiter(nodes, "__", TextType.BOLD_TEXT)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC_TEXT)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC_TEXT)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown_document):
    """Split a markdown document into blocks separated by blank lines.

    Args:
        markdown_document: Raw markdown string.

    Returns:
        List of stripped block strings.
    """
    blocks = markdown_document.split("\n\n")
    cleaned_blocks = []

    for block in blocks:
        cleaned_block = block.strip()
        if not block:
            continue
        cleaned_blocks.append(cleaned_block)
    return cleaned_blocks

class BlockType(Enum):
    PARAGRAPH = auto()
    HEADING = auto()
    CODE = auto()
    QUOTE = auto()
    UNORDERD_LIST = auto()
    ORDERED_LIST = auto()

def block_to_block_type(markdown_block):
    """Classify a markdown block into its BlockType.

    Args:
        markdown_block: A single markdown block string.

    Returns:
        The BlockType enum value for the block.
    """
    heading_re = r'^(#{1,6})\s+(.+)$'
    code_block_re = r'^```[\t ]*\n([\s\S]*?)\n```$'
    quote_block_re = r'^(?:>\s?.+(?:\n|$))+'
    unordered_list_re = r'^(?:-\s+.+(?:\n|$))+'
    ordered_list_re = r'^(?:\d+\.\s+.+(?:\n|$))+'
    
    match markdown_block:
        case _ if re.match(heading_re, markdown_block):
            return BlockType.HEADING
        case _ if re.match(code_block_re, markdown_block):
            return BlockType.CODE
        case _ if re.match(quote_block_re, markdown_block):
            return BlockType.QUOTE
        case _ if re.match(unordered_list_re, markdown_block):
            return BlockType.UNORDERD_LIST
        case _ if re.match(ordered_list_re, markdown_block):
            return BlockType.ORDERED_LIST
        case _:
            return BlockType.PARAGRAPH

def block_to_html(block, block_type):
    """Convert a markdown block and its type to an HTMLNode.

    Args:
        block: A single markdown block string.
        block_type: The BlockType of the block.

    Returns:
        An HTMLNode representing the block.
    """
    match block_type:
        case _ if BlockType.PARAGRAPH:
            html_node = HTMLNode("p", block)
        case _:
            return "base case"

def markdown_to_html_node(markdown):
    """Convert a full markdown document to an HTMLNode.

    Args:
        markdown: Raw markdown document string.

    Returns:
        An HTMLNode representing the document.
    """
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        html_node = block_to_html(block, block_type)
    return None

