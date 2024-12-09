import unittest

from parameterized import parameterized

from document import extract_title


class TestExtractTitle(unittest.TestCase):
    @parameterized.expand(
        (
            (
                "simple",
                """
# Title

This is a document
""",
                "Title",
            ),
            (
                "and deletes extra whitespace",
                """
#    Title   

This is a document
""",
                "Title",
            ),
            (
                "h1 not first block",
                """
##### Date

# Title

## Subtitle

This is a document
""",
                "Title",
            ),
        )
    )
    def test_extracts_title_from_markdown_(self, name, markdown, title):
        output = extract_title(markdown)
        self.assertEqual(output, title)

    def test_raises_if_no_h1_in_markdown(self):
        md = """
This is a document

## With one section heading

And one paragraph
"""
        self.assertRaises(Exception, lambda: extract_title(md))
