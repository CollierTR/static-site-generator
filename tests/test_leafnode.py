import unittest
from leafnode import LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Hello, world!", {"href": "#", "target": "_blank"})
        self.assertEqual(node.to_html(), "<a href='#' target='_blank'>Hello, world!</a>")

    def test_not_eq(self):
        node = LeafNode(tag="h1", value="Hello World")
        node2 = LeafNode(tag="p", value="Hello World")
        self.assertNotEqual(node, node2)
        self.assertNotEqual(node.tag, node2.tag)


    def test_eq(self):
        node = LeafNode(tag="a", value="Hello World", props={"src": "www.goggle.com", "target": "_blank"})
        node2 = LeafNode(tag="p", value="Hello World")
        self.assertEqual(node.value, node2.value)
        self.assertEqual(node.props_to_html(), " src='www.goggle.com' target='_blank'")



if __name__ == "__main__":
    unittest.main()

