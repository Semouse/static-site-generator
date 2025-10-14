from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = 1
    BOLD = 2
    ITALIC = 3
    CODE = 4
    LINK = 5
    IMAGE = 6


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

        if text_type in [TextType.LINK, TextType.IMAGE] and url is None:
            raise ValueError(f"{text_type.name} text node must have URL")

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False

        return (self.text == other.text and self.text_type == other.text_type and self.url == other.url)

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.name}, {self.url})"

    def to_html_node(self):
        match self.text_type:
            case TextType.TEXT:
                node = LeafNode(tag=None, value=self.text)
                return node
            case TextType.BOLD:
                node = LeafNode(tag="b", value=self.text)
                return node
            case TextType.ITALIC:
                node = LeafNode(tag="i", value=self.text)
                return node
            case TextType.CODE:
                node = LeafNode(tag="code", value=self.text)
                return node
            case TextType.LINK:
                node = LeafNode(tag="a", value=self.text, props={"href": self.url})
                return node
            case TextType.IMAGE:
                node = LeafNode(tag="img", value="", props={"src": self.url, "alt": self.text})
                return node
            case _:
                raise ValueError("Unknown text node type")

