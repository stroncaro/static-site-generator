from enum import Enum
import re
from typing import List

from htmlnode import HTMLNode
from inline import text_to_text_nodes, text_node_to_html_node
from parentnode import ParentNode
from utils import all_true


def markdown_to_blocks(markdown: str) -> List[str]:
    markdown = markdown.strip()
    blocks = (block for block in re.split(r"\n{2,}", markdown.strip()))
    blocks = (block.strip() for block in blocks)
    return list(blocks)


class BlockType(Enum):
    PARAGRAPH = "p"
    HEADING1 = "h1"
    HEADING2 = "h2"
    HEADING3 = "h3"
    HEADING4 = "h4"
    HEADING5 = "h5"
    HEADING6 = "h6"
    CODE = "code"
    QUOTE = "blockquote"
    UNORDERED_LIST = "ul"
    ORDERED_LIST = "ol"
    LIST_ITEM = "li"


def block_to_block_type(block: str) -> BlockType:
    if block.startswith("# "):
        return BlockType.HEADING1
    if block.startswith("## "):
        return BlockType.HEADING2
    if block.startswith("### "):
        return BlockType.HEADING3
    if block.startswith("#### "):
        return BlockType.HEADING4
    if block.startswith("##### "):
        return BlockType.HEADING5
    if block.startswith("###### "):
        return BlockType.HEADING6

    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    lines = [line.strip() for line in block.split("\n")]

    quotes = (line.startswith(">") for line in lines)
    if all_true(quotes):
        return BlockType.QUOTE

    ul = (line.startswith("* ") or line.startswith("- ") for line in lines)
    if all_true(ul):
        return BlockType.UNORDERED_LIST

    ol = (line.startswith(f"{i+1}. ") for i, line in enumerate(lines))
    if all_true(ol):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        children = get_children(block, block_type)
        new_node = ParentNode(block_type.value, children)
        if block_type == BlockType.CODE:
            new_node = ParentNode("pre", [new_node])
        block_nodes.append(new_node)

    root_node = ParentNode("div", block_nodes)
    return root_node


def get_children(block: str, block_type: BlockType) -> List[HTMLNode]:
    match block_type:
        case BlockType.PARAGRAPH:
            inline_text = block
        case (
            BlockType.HEADING1
            | BlockType.HEADING2
            | BlockType.HEADING3
            | BlockType.HEADING4
            | BlockType.HEADING5
            | BlockType.HEADING6
        ):
            inline_text = block.lstrip("# ")
        case BlockType.CODE:
            inline_text = block.strip("`\n ")
        case BlockType.QUOTE:
            inline_text = " ".join(
                line.lstrip(">").strip() for line in block.split("\n")
            )
        case BlockType.LIST_ITEM:
            inline_text = block.split(" ", maxsplit=1)[1]
        case BlockType.UNORDERED_LIST | BlockType.ORDERED_LIST:
            items = (line for line in block.split("\n"))
            children = [get_children(line, BlockType.LIST_ITEM) for line in items]
            children = [ParentNode("li", child) for child in children]
            return children
        case _:
            raise Exception(f"Unknown block type: {block_type.name}")

    text_nodes = text_to_text_nodes(inline_text)
    html_nodes = [text_node_to_html_node(node) for node in text_nodes]
    return html_nodes
