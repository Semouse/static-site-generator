import unittest

from parser import split_nodes_delimiter
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
