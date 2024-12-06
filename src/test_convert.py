import unittest

from textnode import TextNode, TextType
from convert import text_node_to_html_node


class TestTextNodeToHTMLConversion(unittest.TestCase):

    def test_normal(self):
        node = TextNode("some text", TextType.NORMAL)
        html_node = text_node_to_html_node(node)
        target_repr = """HTMLNode(None, 'some text', None, None)"""
        self.assertEqual(html_node.__repr__(), target_repr)

    def test_bold(self):
        node = TextNode("some text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        target_repr = """HTMLNode('b', 'some text', None, None)"""
        self.assertEqual(html_node.__repr__(), target_repr)

    def test_italic(self):
        node = TextNode("some text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        target_repr = """HTMLNode('i', 'some text', None, None)"""
        self.assertEqual(html_node.__repr__(), target_repr)

    def test_code(self):
        node = TextNode("some text", TextType.CODE)
        html_node = text_node_to_html_node(node)
        target_repr = """HTMLNode('code', 'some text', None, None)"""
        self.assertEqual(html_node.__repr__(), target_repr)

    def test_link(self):
        node = TextNode("some text", TextType.LINK, "some url")
        html_node = text_node_to_html_node(node)
        target_repr = """HTMLNode('a', 'some text', None, {'href': 'some url'})"""
        self.assertEqual(html_node.__repr__(), target_repr)

    def test_image(self):
        node = TextNode("some text", TextType.IMAGE, "some url")
        html_node = text_node_to_html_node(node)
        target_repr = (
            """HTMLNode('img', '', None, {'src': 'some url', 'alt': 'some text'})"""
        )
        self.assertEqual(html_node.__repr__(), target_repr)
