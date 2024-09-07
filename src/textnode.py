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
