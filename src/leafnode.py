from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)


    def to_html(self):
        if not self.value:
            raise ValueError

        if not self.tag:
            return self.value

        html = f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        return html


    def __repr__(self):
        obj = {
                "tag": self.tag,
                "value": self.value,
                "props": self.props_to_html()
                }
        return obj
