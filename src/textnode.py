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
