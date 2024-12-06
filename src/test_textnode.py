import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq_without_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_without_url_explicitly(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD, None)
        self.assertEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://google.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://google.com")
        self.assertEqual(node, node2)

    def test_not_eq_with_different_text(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://google.com")
        node2 = TextNode("This is a TEXT node", TextType.BOLD, "https://google.com")
        self.assertNotEqual(node, node2)

    def test_not_eq_with_different_type(self):
        node = TextNode("This is a text node", TextType.NORMAL, "https://google.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://google.com")
        self.assertNotEqual(node, node2)

    def test_not_eq_with_different_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, "https://google.com")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
