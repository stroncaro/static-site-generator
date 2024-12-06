import unittest

from leafnode import LeafNode


class LeafNodeTest(unittest.TestCase):
    def test_to_html_without_attributes(self):
        node = LeafNode("p", "This is a paragraph of text.")
        html = node.to_html()
        self.assertEqual(html, "<p>This is a paragraph of text.</p>")

    def test_to_html_with_attributes(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        html = node.to_html()
        self.assertEqual(html, '<a href="https://www.google.com">Click me!</a>')

    def test_to_html_without_tag(self):
        node = LeafNode(None, "This is raw text", None)
        html = node.to_html()
        self.assertEqual(html, "This is raw text")
