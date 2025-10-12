import unittest

from textnode import TextNode, TextType
from htmlnode import LeafNode

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

    def test_plaintext(self):
        node = TextNode("This is a text node", TextType.PLAINTEXT)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        text_node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node.to_html_node()
        expected = LeafNode("b", "Bold text")
        self.assertEqual(html_node.tag, expected.tag)
        self.assertEqual(html_node.value, expected.value)

    def test_italic(self):
        text_node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node.to_html_node()
        expected = LeafNode("i", "Italic text")
        self.assertEqual(html_node.tag, expected.tag)
        self.assertEqual(html_node.value, expected.value)

    def test_codetext(self):
        text_node = TextNode("print('hello')", TextType.CODETEXT)
        html_node = text_node.to_html_node()
        expected = LeafNode("code", "print('hello')")
        self.assertEqual(html_node.tag, expected.tag)
        self.assertEqual(html_node.value, expected.value)

    def test_link(self):
        text_node = TextNode("Click me", TextType.LINK, "https://example.com")
        html_node = text_node.to_html_node()
        expected = LeafNode("a", "Click me", {"href": "https://example.com"})
        self.assertEqual(html_node.tag, expected.tag)
        self.assertEqual(html_node.value, expected.value)
        self.assertEqual(html_node.props, expected.props)

    def test_image(self):
        text_node = TextNode("A beautiful image", TextType.IMAGE, "/path/to/image.jpg")
        html_node = text_node.to_html_node()
        expected = LeafNode("img", "", {"src": "/path/to/image.jpg", "alt": "A beautiful image"})
        self.assertEqual(html_node.tag, expected.tag)
        self.assertEqual(html_node.value, expected.value)
        self.assertEqual(html_node.props, expected.props)

    def test_link_without_url(self):
        with self.assertRaises(ValueError):
            text_node = TextNode("Link text", TextType.LINK)
    
    def test_image_without_url(self):
        with self.assertRaises(ValueError):
            text_node = TextNode("Alt text", TextType.IMAGE)


if __name__ == "__main__":
    unittest.main()
