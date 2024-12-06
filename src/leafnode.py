from typing import Dict, Self
from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str | None,
        value: str,
        props: Dict[str, str] | None = None,
    ) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.tag:
            return self.value
        open, close = self.tag_to_html_tags()
        return f"{open}{self.value}{close}"
