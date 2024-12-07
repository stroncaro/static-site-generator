import itertools
from typing import List

from leafnode import LeafNode
from textnode import TextNode, TextType


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.NORMAL:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Unknown text node type")


def split_node_delimiter(
    old_nodes: List[TextNode], delimiter: str, text_type: TextType
) -> List[TextNode]:

    def chunk_text_by_delimiter(text: str) -> List[str]:
        chunks = text.split(delimiter)
        if len(chunks) % 2 == 0:
            raise Exception(f"Malformed markdown text: {text}")
        return chunks

    def chunk_to_nodes(
        chunks: List[str],
        type_outside_delimiter: TextType,
        type_inside_delimiter: TextType,
    ) -> List[TextNode]:
        return [
            TextNode(text, (type_outside_delimiter, type_inside_delimiter)[i % 2])
            for i, text in enumerate(chunks)
            if text
        ]

    new_nodes = []
    for node in old_nodes:
        chunks = chunk_text_by_delimiter(node.text)
        nodes = chunk_to_nodes(chunks, node.text_type, text_type)
        new_nodes.extend(nodes)
    return new_nodes
