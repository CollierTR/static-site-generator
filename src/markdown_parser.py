import re
from enum import Enum, auto
from textnode import TextType, TextNode
from text_to_html import text_node_to_html_node
from parentnode import ParentNode
from leafnode import LeafNode


def split_nodes_delimiter(old_nodes, delimiter, text_type):
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
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def split_nodes_link(old_nodes):
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
            string = re.split(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", remainder, maxsplit=1)
            if string[0]:
                new_nodes.append(TextNode(string[0], TextType.PLAIN_TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            remainder = string[3]

        if remainder:
            new_nodes.append(TextNode(remainder, TextType.PLAIN_TEXT))

    return new_nodes


def split_nodes_image(old_nodes):
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
            string = re.split(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", remainder, maxsplit=1)
            if string[0]:
                new_nodes.append(TextNode(string[0], TextType.PLAIN_TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            remainder = string[3]

        if remainder:
            new_nodes.append(TextNode(remainder, TextType.PLAIN_TEXT))

    return new_nodes


def text_to_textnodes(text):
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
    blocks = markdown_document.split("\n\n")
    cleaned_blocks = []

    for block in blocks:
        cleaned_block = block.strip()
        if not cleaned_block:
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
    lines = markdown_block.split("\n")

    if lines[0].strip().startswith("```"):
        return BlockType.CODE

    if re.match(r"^#{1,6}\s+", markdown_block.lstrip()):
        return BlockType.HEADING

    non_empty = [l for l in lines if l.strip()]
    if non_empty and all(l.lstrip().startswith(">") for l in non_empty):
        return BlockType.QUOTE

    if non_empty and all(l.lstrip().startswith("- ") for l in non_empty):
        return BlockType.UNORDERD_LIST

    if non_empty and all(re.match(r"^\d+\.\s+", l.lstrip()) for l in non_empty):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in text_nodes:
        if node.text_type == TextType.PLAIN_TEXT and not node.text:
            continue
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes


def block_to_code_html_node(block):
    lines = block.split("\n")

    if lines and lines[0].strip().startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip().startswith("```"):
        lines = lines[:-1]

    if lines:
        non_empty = [l for l in lines if l.strip()]
        if non_empty:
            min_indent = min(len(l) - len(l.lstrip()) for l in non_empty)
            lines = [l[min_indent:] if len(l) >= min_indent else l for l in lines]

    code_text = "\n".join(lines)
    if code_text and not code_text.endswith("\n"):
        code_text += "\n"

    return ParentNode("pre", [LeafNode("code", code_text)])


def block_to_heading_html_node(block):
    match = re.match(r"^#{1,6}\s+(.*)$", block.lstrip())
    if not match:
        return ParentNode("p", text_to_children(block))
    level = len(block) - len(block.lstrip())
    match = re.match(r"^(#{1,6})\s+(.*)$", block.lstrip())
    level = len(match.group(1))
    content = match.group(2)
    return ParentNode(f"h{level}", text_to_children(content))


def block_to_paragraph_html_node(block):
    text = " ".join(block.split("\n"))
    text = re.sub(r" +", " ", text).strip()
    return ParentNode("p", text_to_children(text))


def block_to_quote_html_node(block):
    lines = block.split("\n")
    stripped_lines = []
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith("> "):
            stripped_lines.append(stripped[2:])
        elif stripped.startswith(">"):
            stripped_lines.append(stripped[1:])
        else:
            stripped_lines.append(line)
    text = " ".join(stripped_lines)
    text = re.sub(r" +", " ", text).strip()
    return ParentNode("blockquote", text_to_children(text))


def block_to_unordered_list_html_node(block):
    lines = block.split("\n")
    items = []
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith("- "):
            content = stripped[2:]
        elif stripped.startswith("-"):
            content = stripped[1:]
        else:
            content = stripped
        items.append(ParentNode("li", text_to_children(content)))
    return ParentNode("ul", items)


def block_to_ordered_list_html_node(block):
    lines = block.split("\n")
    items = []
    for line in lines:
        stripped = line.lstrip()
        match = re.match(r"^\d+\.\s+(.*)$", stripped)
        if match:
            content = match.group(1)
        else:
            content = stripped
        items.append(ParentNode("li", text_to_children(content)))
    return ParentNode("ol", items)


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.CODE:
            children.append(block_to_code_html_node(block))
        elif block_type == BlockType.HEADING:
            children.append(block_to_heading_html_node(block))
        elif block_type == BlockType.QUOTE:
            children.append(block_to_quote_html_node(block))
        elif block_type == BlockType.UNORDERD_LIST:
            children.append(block_to_unordered_list_html_node(block))
        elif block_type == BlockType.ORDERED_LIST:
            children.append(block_to_ordered_list_html_node(block))
        else:
            children.append(block_to_paragraph_html_node(block))

    return ParentNode("div", children)


def process_inline_markdown(block_of_markdown):
    return text_to_textnodes(block_of_markdown)


def textNodes_to_html_nodes(textNode_array):
    if not textNode_array:
        return []
    html_nodes = []
    for textNode in textNode_array:
        htmlNode = text_node_to_html_node(textNode)
        html_nodes.append(htmlNode)
    return html_nodes
