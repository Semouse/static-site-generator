import re
from textnode import TextNode, TextType

image_regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
link_regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
                
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid markdown: unclosed delimiter '(delimiter'")
        for i, part in enumerate(parts):
            if not part:
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))

    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(image_regex, text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(link_regex, text)
    return matches
