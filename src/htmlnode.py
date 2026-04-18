
class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props


    def to_html(self):
        raise NotImplementedError;


    def props_to_html(self):
        if not self.props or len(self.props) < 1:
            return ""

        props_string = ""

        for key, value in self.props.items():
            props_string += f" {key}='{value}'"

        return props_string

    def __repr__(self):
        obj = {
                "tag": self.tag,
                "value": self.value,
                "children": self.children,
                "props": self.props_to_html()
                }
        return obj


