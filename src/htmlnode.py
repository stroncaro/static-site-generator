from typing import Dict, List, Self


class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: List[Self] | None = None,
        props: Dict[str, str] | None = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None:
            return ""
        return "".join(f' {key}="{val}"' for key, val in self.props.items())

    def __repr__(self) -> str:
        args = ", ".join(
            arg.__repr__() for arg in (self.tag, self.value, self.children, self.props)
        )
        return f"HTMLNode({args})"
