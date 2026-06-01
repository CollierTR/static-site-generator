
class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        """Initialize an HTMLNode.

        Args:
            tag: HTML tag name (e.g. 'p', 'a').
            value: Text content of the node.
            children: List of child HTMLNode instances.
            props: Dictionary of HTML attributes.
        """
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props


    def to_html(self):
        """Render the node as HTML. Must be overridden by subclasses."""
        raise NotImplementedError;


    def props_to_html(self):
        """Convert props dict to an HTML attribute string.

        Returns:
            A string of HTML attributes (e.g. " href='#' target='_blank'").
        """
        if not self.props or len(self.props) < 1:
            return ""

        props_string = ""

        for key, value in self.props.items():
            props_string += f' {key}="{value}"'

        return props_string

    def __repr__(self):
        """Return a dict representation of the HTMLNode."""
        obj = {
                "tag": self.tag,
                "value": self.value,
                "children": self.children,
                "props": self.props_to_html()
                }
        return obj


