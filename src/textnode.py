from enum import Enum, auto

class TextType(Enum):
    PLAIN_TEXT = auto()
    BOLD_TEXT = auto()
    ITALIC_TEXT = auto()
    CODE_TEXT = auto()
    LINK  = auto()
    IMAGE = auto()

class TextNode():
    def __init__(self, text, text_type, link=None):
        self.text = text
        self.text_type = text_type
        self.link = link

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.link == other.link
            and self.text_type == other.text_type
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.link})"
