import unittest

from parser import *
from textnode import TextNode, TextType

class TestParser(unittest.TestCase):
    def test_basic_single_delimiter(self):
        node = TextNode('Hello world `print("hello")` in python', TextType.TEXT)
        result = split_nodes_delimiter([node], '`', TextType.CODE)

        expected = [
            TextNode('Hello world ', TextType.TEXT),
            TextNode('print("hello")', TextType.CODE),
            TextNode(' in python', TextType.TEXT)
        ]

        self.assertEqual(result, expected)

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_images(text)
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(result, expected)

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        result = extract_markdown_links(text)
        expected = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(result, expected)


    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ], 
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )

    def test_markdown_to_blocks(self):
        markdown  = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""

        blocks = markdown_to_blocks(markdown)
        
        self.assertListEqual(
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
            blocks,
        )

    def test_heading_block_to_block_type(self):
        test_cases = [
            "# Heading 1",
            "## Heading 2",
            "### Heading 3",
            "#### Heading 4",
            "##### Heading 5",
            "###### Heading 6",
            "# Single word"
        ]
        for block in test_cases:
            with self.subTest(block=block):
                self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_code_block_to_block_type(self):
        test_cases = [
            "```python\nprint('hello')\n```",
            "```\ncode block\n```",
            "```javascript\nconsole.log('test')\n```"
        ]
        for block in test_cases:
            with self.subTest(block=block):
                self.assertEqual(block_to_block_type(block), BlockType.CODE)
    
    def test_quote_block_to_block_type(self):
        test_cases = [
            "> This is a quote",
            "> Multiple line quote\n> Second line",
            "> Single character"
        ]
        for block in test_cases:
            with self.subTest(block=block):
                self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
    
    def test_unordered_list_block_to_block_type(self):
        test_cases = [
            "- Item 1",
            "- Another item",
            "- "
        ]
        for block in test_cases:
            with self.subTest(block=block):
                self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
    
    def test_ordered_list_block_to_block_type(self):
        test_cases = [
            "1. First item",
            "1. Only item",
            "1. "
        ]
        for block in test_cases:
            with self.subTest(block=block):
                self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
    
    def test_paragraph_block_to_block_type(self):
        test_cases = [
            "This is a regular paragraph.",
            "No special characters at start",
            "2. This looks like ordered but doesn't start with 1.",
            "* This is not a dash",
            ">This has no space after >",
            "```incomplete code block",
            "code block```",
            "  # Heading with leading space",
            "\t# Heading with tab",
            "1.First item without space",
            "-Item without space"
        ]
        for block in test_cases:
            with self.subTest(block=block):
                self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_edge_cases_markdown_to_block_type(self):
        test_cases = [
            ("", BlockType.PARAGRAPH),
            ("#", BlockType.HEADING),
            ("> ", BlockType.QUOTE),
            ("- ", BlockType.UNORDERED_LIST),
            ("1. ", BlockType.ORDERED_LIST),
            ("```", BlockType.PARAGRAPH),
            (" ``` ", BlockType.PARAGRAPH),
        ]
        
        for block, expected in test_cases:
            with self.subTest(block=block):
                self.assertEqual(block_to_block_type(block), expected)
