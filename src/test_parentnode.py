import unittest
from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_anchor_grandchildren(self):
        grandchild_node = LeafNode("a", "link", {"href": "www.google.com/test", "target": "_blank"})
        grandchild_node2 = LeafNode("a", "another link", {"href": "www.google.com/anothertest"})
        child_node = ParentNode("p", [grandchild_node, grandchild_node2])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><p><a href='www.google.com/test' target='_blank'>link</a><a href='www.google.com/anothertest'>another link</a></p></div>",
        )

if __name__ == "__main__":
    unittest.main()

