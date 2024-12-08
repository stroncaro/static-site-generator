from parameterized import parameterized

import unittest

from block import (
    BlockType,
    markdown_to_blocks,
    block_to_block_type,
    markdown_to_html_nodes,
)


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
            ("heading", "### this is a heading", BlockType.HEADING3),
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


class TestMarkdownToHTMLNodes(unittest.TestCase):
    @parameterized.expand(
        (
            (
                "single plain paragraph",
                "hello world!",
                "<div><p>hello world!</p></div>",
            ),
            (
                "single formatted paragraph",
                "*hello* **world!**",
                "<div><p><i>hello</i> <b>world!</b></p></div>",
            ),
            (
                "single paragraph with link",
                "go [to youtube](https://www.youtube.com)",
                '<div><p>go <a href="https://www.youtube.com">to youtube</a></p></div>',
            ),
            (
                "single paragraph with image",
                "![a mountain](https://link.to.image/mountain.jpg)",
                '<div><p><img src="https://link.to.image/mountain.jpg" alt="a mountain"></img></p></div>',
            ),
            (
                "two simple paragraphs",
                """
This is a simple markdown

It has two paragraphs
""",
                "<div><p>This is a simple markdown</p><p>It has two paragraphs</p></div>",
            ),
            ("single heading 1", "# Heading", "<div><h1>Heading</h1></div>"),
            ("single heading 2", "## Heading", "<div><h2>Heading</h2></div>"),
            ("single heading 3", "### Heading", "<div><h3>Heading</h3></div>"),
            ("single heading 4", "#### Heading", "<div><h4>Heading</h4></div>"),
            ("single heading 5", "##### Heading", "<div><h5>Heading</h5></div>"),
            ("single heading 6", "###### Heading", "<div><h6>Heading</h6></div>"),
            (
                "multiple headings",
                """
# My page heading

### My section heading
""",
                "<div><h1>My page heading</h1><h3>My section heading</h3></div>",
            ),
            (
                "heading with inline styles",
                "# I am **bold**",
                "<div><h1>I am <b>bold</b></h1></div>",
            ),
            (
                "code block",
                """
```
name = input("Enter your name: ")
print("Hello " + name + "!")
```
""",
                '<div><code>name = input("Enter your name: ")\nprint("Hello " + name + "!")</code></div>',
            ),
            (
                "quote block",
                "> Super interesting\n> quote I found",
                "<div><quote>Super interesting quote I found</quote></div>",
            ),
            (
                "ordered list",
                "1. find shelter\n2. start a fire\n3. don't die",
                "<div><ol><li>find shelter</li><li>start a fire</li><li>don't die</li></ol></div>",
            ),
            (
                "unordered list",
                "* find shelter\n* start a fire\n* don't die",
                "<div><ul><li>find shelter</li><li>start a fire</li><li>don't die</li></ul></div>",
            ),
            (
                "unordered list with inline elements",
                "* find **shelter**\n* start a *fire*\n* don't **die**",
                "<div><ul><li>find <b>shelter</b></li><li>start a <i>fire</i></li><li>don't <b>die</b></li></ul></div>",
            ),
        )
    )
    def test_markdown_to_html_with_(self, name, markdown, expected_html):
        html_node = markdown_to_html_nodes(markdown)
        self.assertEqual(html_node.to_html(), expected_html)
