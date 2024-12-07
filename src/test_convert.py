import unittest

from parameterized import parameterized

from textnode import TextNode, TextType
from convert import text_node_to_html_node, split_node_delimiter


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


class TestTextNodeSplittingFunction(unittest.TestCase):
    def test_malformed_markdown(self):
        node = TextNode("Bold* word", TextType.NORMAL)
        self.assertRaises(
            Exception, lambda: split_node_delimiter([node], "*", TextType.BOLD)
        )

    @parameterized.expand(
        (
            (
                "start",
                TextNode("*Bold* word", TextType.NORMAL),
                [
                    TextNode("Bold", TextType.BOLD),
                    TextNode(" word", TextType.NORMAL),
                ],
            ),
            (
                "middle",
                TextNode("A *bold* word", TextType.NORMAL),
                [
                    TextNode("A ", TextType.NORMAL),
                    TextNode("bold", TextType.BOLD),
                    TextNode(" word", TextType.NORMAL),
                ],
            ),
            (
                "end",
                TextNode("Bold *word*", TextType.NORMAL),
                [
                    TextNode("Bold ", TextType.NORMAL),
                    TextNode("word", TextType.BOLD),
                ],
            ),
            (
                "many",
                TextNode("This *has* bold *words*", TextType.NORMAL),
                [
                    TextNode("This ", TextType.NORMAL),
                    TextNode("has", TextType.BOLD),
                    TextNode(" bold ", TextType.NORMAL),
                    TextNode("words", TextType.BOLD),
                ],
            ),
        )
    )
    def test_delimiter_position(self, name, input, output):
        result = split_node_delimiter([input], "*", TextType.BOLD)
        self.assertEqual(result, output)

    def test_complex_case(self):
        nodes = [
            TextNode("*This* world of **dew**\n", TextType.NORMAL),
            TextNode("is a *world* of **dew**,\n", TextType.NORMAL),
            TextNode("and `yet`, and `yet`.\n", TextType.NORMAL),
        ]

        expected_nodes = [
            TextNode("This", TextType.ITALIC),
            TextNode(" world of ", TextType.NORMAL),
            TextNode("dew", TextType.BOLD),
            TextNode("\n", TextType.NORMAL),
            TextNode("is a ", TextType.NORMAL),
            TextNode("world", TextType.ITALIC),
            TextNode(" of ", TextType.NORMAL),
            TextNode("dew", TextType.BOLD),
            TextNode(",\n", TextType.NORMAL),
            TextNode("and ", TextType.NORMAL),
            TextNode("yet", TextType.CODE),
            TextNode(", and ", TextType.NORMAL),
            TextNode("yet", TextType.CODE),
            TextNode(".\n", TextType.NORMAL),
        ]

        result = split_node_delimiter(nodes, "**", TextType.BOLD)
        result = split_node_delimiter(result, "*", TextType.ITALIC)
        result = split_node_delimiter(result, "`", TextType.CODE)
        self.assertEqual(result, expected_nodes)
