import re
from textnode import TextType, TextNode

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
            string = re.split(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", remainder, 1)
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
            string = re.split(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", remainder, 1)
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

    
    





