class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"tag: {self.tag!r}, value: {self.value!r}, childeren: {self.children!r}, props: {self.props!r}"

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        parts = []
        for key, value in self.props.items():
            parts.append(f' {key}="{value}"')

        return "".join(parts)


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError('Tag is required for leaf node')
        elif self.tag is None:
            return self.value
        else:
            return f"<{self.tag}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError('Tag is required for parent node')
        elif self.children is None:
            raise ValueError('Children node is required for parent node')
        else:
            nested = "".join(child.to_html() for child in self.children)
            return f"<{self.tag}>{nested}</{self.tag}>"
