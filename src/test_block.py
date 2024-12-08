from parameterized import parameterized

import unittest

from block import BlockType, markdown_to_blocks, block_to_block_type


class TestMarkdownToBlocks(unittest.TestCase):
    @parameterized.expand(
        (
            (
                "markdown document",
                """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
                """,
                [
                    "# This is a heading",
                    "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                    "* This is the first list item in a list block\n* This is a list item\n* This is another list item",
                ],
            ),
        )
    )
    def test_converts_(self, name, input, expected_output):
        output = markdown_to_blocks(input)
        self.assertEqual(output, expected_output)


class TestBlockToBlockType(unittest.TestCase):
    @parameterized.expand(
        (
            ("heading", "### this is a heading", BlockType.HEADING),
            (
                "tricky non heading",
                "####### this is not a heading (too many #s)",
                BlockType.PARAGRAPH,
            ),
            (
                "code",
                "```py\nname=input('Enter your name: ')\nprint('Hello ' + name + '!')\n```",
                BlockType.CODE,
            ),
            (
                "quote",
                "> something profound\n> by someone\n> who knows something",
                BlockType.QUOTE,
            ),
            (
                "matching unordered list",
                "* buy chicken\n* buy sauce\n* make dinner",
                BlockType.UNORDERED_LIST,
            ),
            (
                "matching unordered list",
                "- buy chicken\n- buy sauce\n- make dinner",
                BlockType.UNORDERED_LIST,
            ),
            (
                "mismatching unordered list",
                "- buy chicken\n* buy sauce\n- make dinner",
                BlockType.UNORDERED_LIST,
            ),
            (
                "ordered list",
                "1. buy chicken\n2. buy sauce\n3. make dinner",
                BlockType.ORDERED_LIST,
            ),
            (
                "wrong ordered list",
                "3. buy chicken\n4. buy sauce\n5. make dinner",
                BlockType.PARAGRAPH,
            ),
            (
                "random paragraph",
                "This is some *very* random text",
                BlockType.PARAGRAPH,
            ),
        )
    )
    def test_detects(self, name, input, expected_output):
        output = block_to_block_type(input)
        self.assertEqual(output, expected_output)
