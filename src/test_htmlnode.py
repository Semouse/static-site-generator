import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_repr_empty_node(self):
        node = HTMLNode()
        expected_repr = "tag: None, value: None, childeren: None, props: None"
        self.assertEqual(repr(node), expected_repr)

    def test_props_to_html(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }

        node = HTMLNode(props = props)
        expected_repr = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected_repr)

    def test_img_props_to_html(self):
        props = {
            "src": "img_girl.jpg",
            "width": "500",
            "height": "600"
        }

        node = HTMLNode(props = props)
        expected_repr = ' src="img_girl.jpg" width="500" height="600"'
        self.assertEqual(node.props_to_html(), expected_repr)