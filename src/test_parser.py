import unittest

from parser import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
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
