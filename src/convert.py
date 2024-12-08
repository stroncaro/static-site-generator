import re
from typing import List, Tuple, Callable

from leafnode import LeafNode
from textnode import TextNode, TextType


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.NORMAL:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Unknown text node type")


MD_IMAGE_REGEX = r"!\[(.*?)\]\((.+?)\)"
MD_LINK_REGEX = r"(?<!!)\[(.+?)\]\((.+?)\)"


# TODO: consolidate the extract_ methods to avoid doing the match twice
def extract_markdown_images(text: str) -> List[Tuple[str, str]]:
    return re.findall(MD_IMAGE_REGEX, text)


def extract_markdown_indeces_images(text: str) -> List[Tuple[int, int]]:
    return (
        (match.start(1) - 2, match.end(2) + 1)
        for match in re.finditer(MD_IMAGE_REGEX, text)
    )


def extract_markdown_links(text: str) -> List[Tuple[str, str]]:
    return re.findall(MD_LINK_REGEX, text)


def extract_markdown_indeces_links(text: str) -> List[Tuple[int, int]]:
    return (
        (match.start(1) - 1, match.end(2) + 1)
        for match in re.finditer(MD_LINK_REGEX, text)
    )


def split_nodes(
    old_nodes: List[TextNode],
    extractor: Callable[[str], List[Tuple[str, str | None]]],
    text_type: TextType,
) -> List[TextNode]:
    new_nodes = []
    for node in old_nodes:
        chunks = extractor(node.text)
        processed = split_nodes_processor(chunks, node.text_type, text_type)
        new_nodes.extend(processed)
    return new_nodes


def split_nodes_processor(
    chunks: List[Tuple[str, str | None]], even_type: TextType, odd_type: TextType
) -> List[TextNode]:
    types = (even_type, odd_type)
    return [
        TextNode(chunk[0], types[i % 2], chunk[1])
        for i, chunk in enumerate(chunks)
        if chunk[0] or chunk[1]
    ]


def extractor(
    tuple_extractor: Callable[[str], List[Tuple[str, str]]],
    index_extractor: Callable[[str], List[Tuple[int, int]]],
):
    def decorated(_):
        def inner(text: str) -> List[Tuple[str, str | None]]:
            chunks = []
            tuples = tuple_extractor(text)
            indeces = index_extractor(text)
            for (extracted_text, extracted_url), (start, end) in zip(tuples, indeces):
                chunks.append((text[:start], None))
                chunks.append((extracted_text, extracted_url))
                text = text[end:]
            chunks.append((text, None))
            return chunks

        return inner

    return decorated


@extractor(extract_markdown_images, extract_markdown_indeces_images)
def extractor_images(text: str) -> List[Tuple[str, str | None]]: ...


@extractor(extract_markdown_links, extract_markdown_indeces_links)
def extractor_links(text: str) -> List[Tuple[str, str | None]]: ...


def extractor_delimiter_factory(delimiter: str):
    def extractor_delimiter(text: str) -> List[Tuple[str, None]]:
        split_text = text.split(delimiter)
        if len(split_text) % 2 == 0:
            raise Exception(f"Malformed markdown text: {text}")
        return [(text_chunk, None) for text_chunk in split_text]

    return extractor_delimiter


def split_nodes_images(old_nodes: List[TextNode]) -> List[TextNode]:
    return split_nodes(old_nodes, extractor_images, TextType.IMAGE)


def split_nodes_links(old_nodes: List[TextNode]) -> List[TextNode]:
    return split_nodes(old_nodes, extractor_links, TextType.LINK)


def split_node_delimiter(
    old_nodes: List[TextNode], delimiter: str, text_type: TextType
) -> List[TextNode]:
    return split_nodes(old_nodes, extractor_delimiter_factory(delimiter), text_type)
