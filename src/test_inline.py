import unittest

from parameterized import parameterized

from textnode import TextNode, TextType
from inline import (
    text_node_to_html_node,
    split_node_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_images,
    split_nodes_links,
    text_to_text_nodes,
)


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


class TestMarkdownImageExtraction(unittest.TestCase):
    @parameterized.expand(
        (
            (
                "one image",
                "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)",
                [
                    ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ],
            ),
            (
                "two images",
                "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
                [
                    ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                    ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
                ],
            ),
            (
                "no alt text",
                "This is an image with no alt text ![](https://i.imgur.com/aKaOqIh.gif)",
                [
                    ("", "https://i.imgur.com/aKaOqIh.gif"),
                ],
            ),
        )
    )
    def test_image_extraction(self, name, input, expected_output):
        output = extract_markdown_images(input)
        self.assertEqual(output, expected_output)


class TestMarkdownLinkExtraction(unittest.TestCase):
    @parameterized.expand(
        (
            (
                "one link",
                "This is text with a link [to boot dev](https://www.boot.dev)",
                [
                    ("to boot dev", "https://www.boot.dev"),
                ],
            ),
            (
                "two links",
                "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/)",
                [
                    ("to boot dev", "https://www.boot.dev"),
                    ("to youtube", "https://www.youtube.com/"),
                ],
            ),
            (
                "image and link",
                "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and a link [to youtube](https://www.youtube.com/)",
                [
                    ("to youtube", "https://www.youtube.com/"),
                ],
            ),
        )
    )
    def test_image_extraction(self, name, input, expected_output):
        output = extract_markdown_links(input)
        self.assertEqual(output, expected_output)


class TestSplitNodesImage(unittest.TestCase):
    @parameterized.expand(
        (
            (
                "single node with one image in middle",
                [
                    TextNode(
                        "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and a link [to youtube](https://www.youtube.com/)",
                        TextType.NORMAL,
                    )
                ],
                [
                    TextNode("This is text with a ", TextType.NORMAL),
                    TextNode(
                        "rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"
                    ),
                    TextNode(
                        " and a link [to youtube](https://www.youtube.com/)",
                        TextType.NORMAL,
                    ),
                ],
            ),
            (
                "single node with one image at start",
                [
                    TextNode(
                        "![rick roll](https://i.imgur.com/aKaOqIh.gif) is a meme",
                        TextType.NORMAL,
                    )
                ],
                [
                    TextNode(
                        "rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"
                    ),
                    TextNode(" is a meme", TextType.NORMAL),
                ],
            ),
            (
                "single node with one image at end",
                [
                    TextNode(
                        "Get Rick Rolled!![rick roll](https://i.imgur.com/aKaOqIh.gif)",
                        TextType.NORMAL,
                    )
                ],
                [
                    TextNode("Get Rick Rolled!", TextType.NORMAL),
                    TextNode(
                        "rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"
                    ),
                ],
            ),
        )
    )
    def test_splits_images_from_(self, name, input, expected_output):
        output = split_nodes_images(input)
        self.assertEqual(output, expected_output)


class TestSplitNodesLinks(unittest.TestCase):
    @parameterized.expand(
        (
            (
                "single node with link at end",
                [
                    TextNode(
                        "This is text with a link [to youtube](https://www.youtube.com/)",
                        TextType.NORMAL,
                    )
                ],
                [
                    TextNode("This is text with a link ", TextType.NORMAL),
                    TextNode("to youtube", TextType.LINK, "https://www.youtube.com/"),
                ],
            ),
            (
                "single node with link in middle",
                [
                    TextNode(
                        "Go [to youtube](https://www.youtube.com/) to watch some videos",
                        TextType.NORMAL,
                    )
                ],
                [
                    TextNode("Go ", TextType.NORMAL),
                    TextNode("to youtube", TextType.LINK, "https://www.youtube.com/"),
                    TextNode(" to watch some videos", TextType.NORMAL),
                ],
            ),
            (
                "single node with link at start",
                [
                    TextNode(
                        "[Youtube](https://www.youtube.com/) to watch some videos",
                        TextType.NORMAL,
                    )
                ],
                [
                    TextNode("Youtube", TextType.LINK, "https://www.youtube.com/"),
                    TextNode(" to watch some videos", TextType.NORMAL),
                ],
            ),
            (
                "tricky case where text repeats",
                [
                    TextNode(
                        "Have you gone to Youtube? [Youtube](https://www.youtube.com/)",
                        TextType.NORMAL,
                    )
                ],
                [
                    TextNode("Have you gone to Youtube? ", TextType.NORMAL),
                    TextNode("Youtube", TextType.LINK, "https://www.youtube.com/"),
                ],
            ),
        )
    )
    def test_splits_images_from_(self, name, input, expected_output):
        output = split_nodes_links(input)
        self.assertEqual(output, expected_output)


class TestTextToTextNode(unittest.TestCase):

    @parameterized.expand(
        (
            (
                "complex_case",
                "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://www.youtube.com/)",
                [
                    TextNode("This is ", TextType.NORMAL),
                    TextNode("text", TextType.BOLD),
                    TextNode(" with an ", TextType.NORMAL),
                    TextNode("italic", TextType.ITALIC),
                    TextNode(" word and a ", TextType.NORMAL),
                    TextNode("code block", TextType.CODE),
                    TextNode(" and an ", TextType.NORMAL),
                    TextNode(
                        "obi wan image",
                        TextType.IMAGE,
                        "https://i.imgur.com/fJRm4Vk.jpeg",
                    ),
                    TextNode(" and a ", TextType.NORMAL),
                    TextNode("link", TextType.LINK, "https://www.youtube.com/"),
                ],
            ),
        )
    )
    def test_text(self, name, input, expected_output):
        output = text_to_text_nodes(input)
        self.assertEqual(output, expected_output)
