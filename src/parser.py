import re
from textnode import TextNode, TextType

image_regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
link_regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"

def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    current_nodes = split_nodes_delimiter([node], '**', TextType.BOLD)
    current_nodes = split_nodes_delimiter(current_nodes, '_', TextType.ITALIC)
    current_nodes = split_nodes_delimiter(current_nodes, '`', TextType.CODE)
    current_nodes = split_nodes_image(current_nodes)
    current_nodes = split_nodes_link(current_nodes)

    return current_nodes

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

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        images = extract_markdown_images(node.text)
        start = 0
        for image in images:
            image_substring = f"![{image[0]}]({image[1]})"
            position = node.text.find(image_substring)

            if position != -1:
                new_nodes.append(TextNode(node.text[start:position], TextType.TEXT))
                new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
                start = position + len(image_substring)
        
        if start < len(node.text):
            new_nodes.append(TextNode(node.text[start:], TextType.TEXT))
        
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)
        start = 0
        for link in links:
            link_substring = f"[{link[0]}]({link[1]})"
            position = node.text.find(link_substring)
            if position != -1:
                new_nodes.append(TextNode(node.text[start:position], TextType.TEXT))
                new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                start = position + len(link_substring)

        if start < len(node.text):
            new_nodes.append(TextNode(node.text[start:], TextType.TEXT))

    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(image_regex, text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(link_regex, text)
    return matches

def markdown_to_blocks(markdown):
    result = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        trimmed_block = block.strip()
        if len(trimmed_block) > 0:
            result.append(trimmed_block)

    return result
    
