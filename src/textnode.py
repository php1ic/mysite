import re

import parentnode
import leafnode


class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
                self.text == other.text
                and self.text_type == other.text_type
                and self.url == other.url
                )

    def __repr__(self):
        return f"{type(self).__name__}({self.text}, {self.text_type}, {self.url})"


text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"


def text_node_to_html_node(text_node: TextNode):
    if text_node.text_type == text_type_text:
        return leafnode.LeafNode(None, text_node.text)
    if text_node.text_type == text_type_bold:
        return leafnode.LeafNode("b", text_node.text)
    if text_node.text_type == text_type_italic:
        return leafnode.LeafNode("i", text_node.text)
    if text_node.text_type == text_type_code:
        return leafnode.LeafNode("code", text_node.text)
    if text_node.text_type == text_type_link:
        return leafnode.LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == text_type_image:
        return leafnode.LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise ValueError(f"Unknown text type: {text_node.text_type}")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = list()
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue

        sub_nodes = list()
        subs = node.text.split(delimiter)

        if len(subs) % 2 == 0:
            raise ValueError(f"ERROR: Unmatched {delimiter}")

        for sub in range(len(subs)):
            if subs[sub] == "":
                continue

            if sub % 2 == 0:
                sub_nodes.append(TextNode(subs[sub], text_type_text))
            else:
                sub_nodes.append(TextNode(subs[sub], text_type))

        new_nodes.extend(sub_nodes)

    return new_nodes


def extract_markdown_images(text: str):
    image_regex = r"!\[(.*?)\]\((.*?)\)"
    return re.findall(image_regex, text)


def extract_markdown_links(text):
    link_regex = r"(?<!!)\[(.*?)\]\((.*?)\)"
    return re.findall(link_regex, text)


def split_nodes_image(old_nodes):
    new_nodes = list()

    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue

        original_text = old_node.text
        images = extract_markdown_images(original_text)

        if len(images) == 0:
            new_nodes.append(old_node)
            continue

        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)

            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")

            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], text_type_text))

            new_nodes.append(
                TextNode(
                    image[0],
                    text_type_image,
                    image[1],
                )
            )

            original_text = sections[1]

        if original_text != "":
            new_nodes.append(TextNode(original_text, text_type_text))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = list()

    for old_node in old_nodes:

        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue

        original_text = old_node.text

        links = extract_markdown_links(original_text)

        if len(links) == 0:
            new_nodes.append(old_node)
            continue

        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)

            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")

            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], text_type_text))

            new_nodes.append(TextNode(link[0], text_type_link, link[1]))

            original_text = sections[1]

        if original_text != "":
            new_nodes.append(TextNode(original_text, text_type_text))

    return new_nodes


def text_to_textnodes(text):
    new_nodes = [TextNode(text, text_type_text)]
    new_nodes = split_nodes_delimiter(new_nodes, "**", text_type_bold)
    new_nodes = split_nodes_delimiter(new_nodes, "*", text_type_italic)
    new_nodes = split_nodes_delimiter(new_nodes, "`", text_type_code)
    new_nodes = split_nodes_link(new_nodes)
    new_nodes = split_nodes_image(new_nodes)

    return new_nodes


def markdown_to_blocks(markdown):
    return [s.strip() for s in markdown.split('\n\n') if s != ""]


block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"


def block_to_block_type(block: str):
    # Empty block
    if block == "":
        return block_type_paragraph

    # Header
    if block.startswith('#'):
        return block_type_heading

    # Code
    lines = block.split('\n')
    if len(lines)> 1 and lines[0].startswith('```') and lines[-1].endswith('```'):
        return block_type_code

    # Quote: Need to check start of all lines
    quote = True
    for line in lines:
        if not line.startswith('>'):
            quote = False
            break

    if quote:
        return block_type_quote

    # Unordered list: Need to check start of all lines
    ulist = True
    for line in lines:
        if not line.startswith(('* ', '- ')):
            ulist = False
            break

    if ulist:
        return block_type_unordered_list

    # Ordered list: Need to check start of all lines
    olist = True
    for i, line in enumerate(lines, start=1):
        if not line.startswith(f'{i}. '):
            olist = False
            break

    if olist:
        return block_type_ordered_list

    return block_type_paragraph


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = list()
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return parentnode.ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == block_type_paragraph:
        return paragraph_to_html_node(block)
    if block_type == block_type_heading:
        return heading_to_html_node(block)
    if block_type == block_type_code:
        return code_to_html_node(block)
    if block_type == block_type_ordered_list:
        return olist_to_html_node(block)
    if block_type == block_type_unordered_list:
        return ulist_to_html_node(block)
    if block_type == block_type_quote:
        return quote_to_html_node(block)
    raise ValueError("Invalid block type")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = list()
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return parentnode.ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")
    text = block[(level + 1):]
    children = text_to_children(text)
    return parentnode.ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    children = text_to_children(text)
    code = parentnode.ParentNode("code", children)
    return parentnode.ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = list()
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(parentnode.ParentNode("li", children))
    return parentnode.ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = list()
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(parentnode.ParentNode("li", children))
    return parentnode.ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = list()
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return parentnode.ParentNode("blockquote", children)
