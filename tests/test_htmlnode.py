import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):

    def test_not_eq(self):
        node = HTMLNode(tag="h1", value="Hello World")
        node2 = HTMLNode(tag="p", value="Hello World")
        self.assertNotEqual(node, node2)
        self.assertNotEqual(node.tag, node2.tag)


    def test_eq(self):
        node = HTMLNode(tag="a", value="Hello World", props={"src": "www.goggle.com", "target": "_blank"})
        node2 = HTMLNode(tag="p", value="Hello World")
        self.assertEqual(node.value, node2.value)
        self.assertEqual(node.props_to_html(), " src='www.goggle.com' target='_blank'")



if __name__ == "__main__":
    unittest.main()

