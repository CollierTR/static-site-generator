import unittest

from textnode import TextNode, TextType
from leafnode import LeafNode
from text_to_html import text_node_to_html_node


class TestTextToHtml(unittest.TestCase):
    def test_eq(self):
        text_node = TextNode("bold text", TextType.BOLD_TEXT)
        transformed_text_node = text_node_to_html_node(text_node)
        html_node = LeafNode("b", "bold text")
        self.assertEqual(transformed_text_node.tag, html_node.tag)
        self.assertEqual(transformed_text_node.value, html_node.value)

    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")


if __name__ == "__main__":
    unittest.main()
