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


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_example(self):
        node = textnode.TextNode("This is text with a `code block` word", textnode.text_type_text)
        new_nodes = textnode.split_nodes_delimiter([node], "`", textnode.text_type_code)

        nodes = [
            textnode.TextNode("This is text with a ", textnode.text_type_text),
            textnode.TextNode("code block", textnode.text_type_code),
            textnode.TextNode(" word", textnode.text_type_text),
        ]
        self.assertEqual(new_nodes, nodes)

    def test_bold(self):
        node = textnode.TextNode("This is text with a **bolded** word", textnode.text_type_text)
        new_nodes = textnode.split_nodes_delimiter([node], "**", textnode.text_type_bold)

        nodes = [
            textnode.TextNode("This is text with a ", textnode.text_type_text),
            textnode.TextNode("bolded", textnode.text_type_bold),
            textnode.TextNode(" word", textnode.text_type_text),
        ]
        self.assertEqual(new_nodes, nodes)

    def test_italic(self):
        node = textnode.TextNode("This is text with a *italic* word", textnode.text_type_text)
        new_nodes = textnode.split_nodes_delimiter([node], "*", textnode.text_type_italic)

        nodes = [
            textnode.TextNode("This is text with a ", textnode.text_type_text),
            textnode.TextNode("italic", textnode.text_type_italic),
            textnode.TextNode(" word", textnode.text_type_text),
        ]
        self.assertEqual(new_nodes, nodes)


class TestExtractMarkdownImages(unittest.TestCase):
    def test_example(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        output = textnode.extract_markdown_images(text)
        expected_output = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(expected_output, output)


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_example(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        output = textnode.extract_markdown_links(text)
        expected_output = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(expected_output, output)


if __name__ == "__main__":
    unittest.main()
