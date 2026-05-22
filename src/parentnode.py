from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        """Initialize a ParentNode.

        Args:
            tag: HTML tag name (required).
            children: List of child HTMLNode instances (required, non-empty).
            props: Optional dictionary of HTML attributes.
        """
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        """Render the parent node and all children as an HTML string.

        Returns:
            An HTML string recursively wrapping all child nodes.

        Raises:
            ValueError: If tag is missing or children is empty.
        """
        if not self.tag:
            raise ValueError("Class requires a tag value")

        if not self.children:
            raise ValueError("ParentNode Class requires an array of children (html class instances)")

        children_html = "".join(child.to_html() for child in self.children)
        html = f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

        return html
