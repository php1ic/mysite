import unittest

import textnode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = textnode.TextNode("This is a text node", "bold")
        node2 = textnode.TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_url_eq(self):
        node = textnode.TextNode("3This is a text node", "bold", "https://boot.dev")
        node2 = textnode.TextNode("3This is a text node", "bold", "https://boot.dev")
        self.assertEqual(node, node2)

    def test_type_not_eq(self):
        node = textnode.TextNode("1This is a text node", "italics")
        node2 = textnode.TextNode("1This is a text node", "bold")
        self.assertNotEqual(node, node2)

    def test_url_not_eq(self):
        node = textnode.TextNode("2This is a text node", "bold", "https://boot.dev")
        node2 = textnode.TextNode("2This is a text node", "bold",  "https://beet.dov")
        self.assertNotEqual(node, node2)


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_bold(self):
        node = textnode.TextNode("This is bold", textnode.text_type_bold)
        html_node = textnode.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")


if __name__ == "__main__":
    unittest.main()
