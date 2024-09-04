import htmlnode


class ParentNode(htmlnode.HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("No tag given")

        if self.children is None:
            raise ValueError("No children given")

        output = ""

        for child in self.children:
            output += child.to_html()

        return f"<{self.tag}{self.props_to_html()}>{output}</{self.tag}>"
