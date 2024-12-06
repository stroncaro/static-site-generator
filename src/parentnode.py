from typing import Dict, List
from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(
        self, tag: str, children: List[HTMLNode], props: Dict[str, str] | None = None
    ) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode should have a tag")

        if not self.children:
            raise ValueError("ParentNode should have children")

        open, close = self.tag_to_html_tags()
        children = "".join(child.to_html() for child in self.children)
        return f"{open}{children}{close}"
