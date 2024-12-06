import unittest

from leafnode import LeafNode
from parentnode import ParentNode


class ParentNodeTest(unittest.TestCase):
    def test_to_html_raise_valueerror_if_no_tag(self):
        node = ParentNode(None, [LeafNode("b", "Bold text")])
        self.assertRaises(ValueError, lambda: node.to_html())

    def test_to_html_raise_valueerror_if_no_children(self):
        node = ParentNode("p", None)
        self.assertRaises(ValueError, lambda: node.to_html())

    def test_to_html_no_props(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        html = node.to_html()
        self.assertEqual(
            html, "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        )

    def test_to_html_with_props(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text", {"id": "italic"}),
                LeafNode(None, "Normal text"),
            ],
            {"id": "first"},
        )
        html = node.to_html()
        self.assertEqual(
            html,
            '<p id="first"><b>Bold text</b>Normal text<i id="italic">italic text</i>Normal text</p>',
        )

    def test_to_html_nested(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text"),
                        LeafNode("i", "italic text"),
                        LeafNode(None, "Normal text"),
                    ],
                ),
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text"),
                        LeafNode("i", "italic text"),
                        LeafNode(None, "Normal text"),
                    ],
                ),
            ],
        )
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></div>",
        )

    def test_to_html_neste_with_props(self):
        node = ParentNode(
            "body",
            [
                ParentNode(
                    "div",
                    [
                        LeafNode("h1", "Title!", {"id": "title"}),
                        LeafNode("h2", "Subtitle", {"id": "subtitle"}),
                    ],
                ),
                ParentNode(
                    "div",
                    [
                        LeafNode("p", "Some content"),
                        LeafNode("p", "And some more!"),
                    ],
                    {"id": "content", "class": "content"},
                ),
            ],
        )
        html = node.to_html()
        self.assertEqual(
            html,
            "<body>"
            + '<div><h1 id="title">Title!</h1><h2 id="subtitle">Subtitle</h2></div>'
            + '<div id="content" class="content"><p>Some content</p><p>And some more!</p></div>'
            + "</body>",
        )
