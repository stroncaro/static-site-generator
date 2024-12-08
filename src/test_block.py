from parameterized import parameterized

import unittest

from block import markdown_to_blocks


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
