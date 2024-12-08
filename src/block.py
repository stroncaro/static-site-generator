import re


def markdown_to_blocks(markdown: str):
    markdown = markdown.strip()
    blocks = (block for block in re.split(r"\n{2,}", markdown.strip()))
    blocks = (block.strip() for block in blocks)
    return list(blocks)
