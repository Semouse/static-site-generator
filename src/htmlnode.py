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
