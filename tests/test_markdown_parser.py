import unittest

from textnode import TextNode, TextType
from markdown_parser import (
    split_nodes_delimiter,
    markdown_to_html_node,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    markdown_to_blocks,
    BlockType,
    block_to_block_type,
)


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_header_to_correct_BlockType(self):
        correct_block_type = BlockType.HEADING
        markdown_block = "### This is a heading!"
        converted_block = block_to_block_type(markdown_block)
        self.assertEqual(converted_block, correct_block_type)

    def test_code_to_correct_BlockType(self):
        correct_block_type = BlockType.CODE
        markdown_block = f"""
```
const lang = "Not Python"

console.log(lang)

```
"""
        converted_block = block_to_block_type(markdown_block.strip())
        self.assertEqual(converted_block, correct_block_type)

    def test_paragraph_to_correct_BlockType(self):
        correct_block_type = BlockType.PARAGRAPH
        markdown_block = "This is NOT a heading!"
        converted_block = block_to_block_type(markdown_block)
        self.assertEqual(converted_block, correct_block_type)

    def test_quote_to_correct_BlockType(self):
        correct_block_type = BlockType.QUOTE
        markdown_block = f"""
        > This is a 
        > quote!
        """
        converted_block = block_to_block_type(markdown_block.strip())
        self.assertEqual(converted_block, correct_block_type)




class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnode(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        array_of_nodes = [
            TextNode("This is ", TextType.PLAIN_TEXT),
            TextNode("text", TextType.BOLD_TEXT),
            TextNode(" with an ", TextType.PLAIN_TEXT),
            TextNode("italic", TextType.ITALIC_TEXT),
            TextNode(" word and a ", TextType.PLAIN_TEXT),
            TextNode("code block", TextType.CODE_TEXT),
            TextNode(" and an ", TextType.PLAIN_TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.PLAIN_TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(nodes, array_of_nodes)


class TestLinkAndImageTransfromation(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN_TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN_TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN_TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN_TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )




class TestRegexExtractors(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://i.imgur.com/zjjcJ.png). How do you like it?"
        )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJ.png")], matches)


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_no_nodes(self):
        result = split_nodes_delimiter([], "*", TextType.BOLD_TEXT)
        self.assertEqual(result, [])

    def test_no_delimiter(self):
        nodes = [TextNode("hello world", TextType.PLAIN_TEXT)]
        result = split_nodes_delimiter(nodes, "*", TextType.BOLD_TEXT)

        expected = [TextNode("hello world", TextType.PLAIN_TEXT)]
        self.assertEqual(result, expected)

    def test_single_delimiter_pair(self):
        nodes = [TextNode("hello *world* test", TextType.PLAIN_TEXT)]
        result = split_nodes_delimiter(nodes, "*", TextType.BOLD_TEXT)

        expected = [
            TextNode("hello ", TextType.PLAIN_TEXT),
            TextNode("world", TextType.BOLD_TEXT),
            TextNode(" test", TextType.PLAIN_TEXT),
        ]
        self.assertEqual(result, expected)

    def test_multiple_delimiters(self):
        nodes = [TextNode("a *b* c *d* e", TextType.PLAIN_TEXT)]
        result = split_nodes_delimiter(nodes, "*", TextType.BOLD_TEXT)

        expected = [
            TextNode("a ", TextType.PLAIN_TEXT),
            TextNode("b", TextType.BOLD_TEXT),
            TextNode(" c ", TextType.PLAIN_TEXT),
            TextNode("d", TextType.BOLD_TEXT),
            TextNode(" e", TextType.PLAIN_TEXT),
        ]
        self.assertEqual(result, expected)

    def test_unclosed_delimiter_raises(self):
        nodes = [TextNode("hello *world test", TextType.PLAIN_TEXT)]

        with self.assertRaises(Exception):
            split_nodes_delimiter(nodes, "*", TextType.BOLD_TEXT)

    def test_non_plain_text_passthrough(self):
        nodes = [TextNode("hello *world*", TextType.BOLD_TEXT)]
        result = split_nodes_delimiter(nodes, "*", TextType.ITALIC_TEXT)

        # Should not be modified
        self.assertEqual(result, nodes)

    def test_mixed_nodes(self):
        nodes = [
            TextNode("hello *world*", TextType.PLAIN_TEXT),
            TextNode("already bold", TextType.BOLD_TEXT),
        ]

        result = split_nodes_delimiter(nodes, "*", TextType.ITALIC_TEXT)

        expected = [
            TextNode("hello ", TextType.PLAIN_TEXT),
            TextNode("world", TextType.ITALIC_TEXT),
            TextNode("", TextType.PLAIN_TEXT),  # depends if you skip empty
            TextNode("already bold", TextType.BOLD_TEXT),
        ]

        self.assertEqual(result, expected)

    def test_adjacent_delimiters(self):
        nodes = [TextNode("hello **world**", TextType.PLAIN_TEXT)]
        result = split_nodes_delimiter(nodes, "*", TextType.BOLD_TEXT)

        # This exposes behavior with empty splits
        # Depending on implementation, you may skip empty strings
        expected = [
            TextNode("hello ", TextType.PLAIN_TEXT),
            TextNode("", TextType.BOLD_TEXT),
            TextNode("world", TextType.PLAIN_TEXT),
            TextNode("", TextType.BOLD_TEXT),
            TextNode("", TextType.PLAIN_TEXT),
        ]

        self.assertEqual(result, expected)

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


if __name__ == "__main__":
    unittest.main()
