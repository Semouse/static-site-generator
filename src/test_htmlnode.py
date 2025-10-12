import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_em(self):
        node = LeafNode("em", "Emphasized text")
        self.assertEqual(node.to_html(), "<em>Emphasized text</em>")

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "Main heading level 1")
        self.assertEqual(node.to_html(), "<h1>Main heading level 1</h1>")

    def test_parent_to_html_ex(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        result = node.to_html()
        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(result, expected)

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>")
    


