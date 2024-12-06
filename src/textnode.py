from enum import Enum


class TextType(Enum):
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, value: object) -> bool:
        try:
            return (
                self.text == value.text
                and self.text_type == value.text_type
                and self.url == value.url
            )
        except AttributeError:
            return False

    def __repr__(self) -> str:
        return f"TextNode({self.text.__repr__()}, {self.text_type.__class__.__name__}.{self.text_type.name}, {self.url.__repr__()})"
