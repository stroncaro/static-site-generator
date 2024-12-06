import unittest

from htmlnode import HTMLNode


class HTMLNodeTest(unittest.TestCase):
    def test_props_to_html_empty_props(self):
        node = HTMLNode("p", "Hello World")
        props = node.props_to_html()
        self.assertEqual(props, "")

    def test_props_to_html_one_prop(self):
        node = HTMLNode("p", "Hello World", None, {"class": "styled-paragraph"})
        props = node.props_to_html()
        self.assertEqual(props, ' class="styled-paragraph"')

    def test_props_to_html_many_props(self):
        node = HTMLNode(
            "p",
            "Hello World",
            None,
            {"id": "first", "class": "styled-paragraph", "style": "{color: black}"},
        )
        props = node.props_to_html()
        self.assertEqual(
            props, ' id="first" class="styled-paragraph" style="{color: black}"'
        )
