from enum import Enum
import functools
import re
from typing import List, Iterable

from utils import all_true


def markdown_to_blocks(markdown: str) -> List[str]:
    markdown = markdown.strip()
    blocks = (block for block in re.split(r"\n{2,}", markdown.strip()))
    blocks = (block.strip() for block in blocks)
    return list(blocks)


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block: str) -> BlockType:
    if block.startswith("#") and not block.startswith("#######"):
        return BlockType.HEADING
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
