from leafnode import LeafNode
from textnode import TextNode, TextType


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    type_func_map = {
        TextType.NORMAL: normal,
        TextType.BOLD: bold,
        TextType.ITALIC: italic,
        TextType.CODE: code,
        TextType.LINK: link,
        TextType.IMAGE: image,
    }
    func = type_func_map.get(text_node.text_type, None)
    if func is None:
        raise Exception("Unknown text node type")
    return func(text=text_node.text, url=text_node.url)


def normal(text: str, **_) -> LeafNode:
    return LeafNode(None, text)


def bold(text: str, **_) -> LeafNode:
    return LeafNode("b", text)


def italic(text: str, **_) -> LeafNode:
    return LeafNode("i", text)


def code(text: str, **_) -> LeafNode:
    return LeafNode("code", text)


def link(text: str, url: str) -> LeafNode:
    return LeafNode("a", text, {"href": url})


def image(text: str, url: str) -> LeafNode:
    return LeafNode("img", "", {"src": url, "alt": text})
