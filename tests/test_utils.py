import unittest

from textnode import TextNode, TextType
from utils import extract_title


class TestUtils(unittest.TestCase):
    def test_extract_title(self):
        markdown_good = "# Hello World!"
        markdown_bad = "## Hello Saturn!"
        solution_good = "Hello World!"
        solution_bad = "Hello Saturn!"

        self.assertEqual(extract_title(markdown_good), solution_good)
        with self.assertRaises(Exception):
            extract_title(markdown_bad)


if __name__ == "__main__":
    unittest.main()
