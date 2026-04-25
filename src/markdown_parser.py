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


def extract_markdown_images(text): #return list of tups
    matches = re.findall(r"!\[(+[\w\d])\]\((+[\w\d])\)", text)
    return matches

def extract_markdown_links(text): #return list of tups
    matches = re.findall(r"!\[([\w\d]+)\]\(([\w\d]+)\)", text)
    return matches
