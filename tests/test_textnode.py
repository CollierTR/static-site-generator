import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)

    def test_note_eq(self):
        node = TextNode("This is a text node", TextType.LINK, "#")
        node2 = TextNode("This is a text node with different text", TextType.BOLD_TEXT)
        self.assertNotEqual(node, node2)
        self.assertNotEqual(node.text_type, node2.text_type)

    def test_default_link(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertIsNone(node.link)


if __name__ == "__main__":
    unittest.main()

