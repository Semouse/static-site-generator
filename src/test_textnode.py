import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        first_node = TextNode("This is a text node", TextType.BOLD)
        second_node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(first_node, second_node)

    def test_not_eq_text(self):
        first_node = TextNode("This is a text node", TextType.BOLD)
        second_node = TextNode("This is not a text node", TextType.BOLD)
        self.assertNotEqual(first_node, second_node)

    def test_not_eq_text_type(self):
        first_node = TextNode("This is a text node", TextType.BOLD)
        second_node = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(first_node, second_node)

    def test_not_eq_url(self):
        first_node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        second_node = TextNode("This is a text node", TextType.BOLD, "https://google.com")
        self.assertNotEqual(first_node, second_node)


if __name__ == "__main__":
    unittest.main()
