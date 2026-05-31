from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        """Initialize a LeafNode.

        Args:
            tag: HTML tag name.
            value: Text content (required, non-empty).
            props: Optional dictionary of HTML attributes.
        """
        super().__init__(tag=tag, value=value, children=None, props=props)


    def to_html(self):
        if self.tag in ("img", "br", "hr", "input", "area", "base", "col", "embed", "link", "meta", "param", "source", "track", "wbr"):
            return f"<{self.tag}{self.props_to_html()}>"

        if not self.value:
            raise ValueError("Class requires a value")

        if not self.tag:
            return self.value

        html = f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        return html


    def __repr__(self):
        """Return a dict representation of the LeafNode."""
        obj = {
                "tag": self.tag,
                "value": self.value,
                "props": self.props_to_html()
                }
        return obj
