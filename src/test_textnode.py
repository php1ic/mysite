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


class TestInlineMarkdown(unittest.TestCase):
    def test_split_image(self):
        node = textnode.TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            textnode.text_type_text,
        )
        new_nodes = textnode.split_nodes_image([node])
        self.assertListEqual(
            [
                textnode.TextNode("This is text with an ", textnode.text_type_text),
                textnode.TextNode("image", textnode.text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = textnode.TextNode(
            "![image](https://www.example.com/image.png)",
            textnode.text_type_text,
        )
        new_nodes = textnode.split_nodes_image([node])
        self.assertListEqual(
            [textnode.TextNode("image", textnode.text_type_image, "https://www.example.com/image.png"),],
            new_nodes,
        )

    def test_split_images(self):
        node = textnode.TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            textnode.text_type_text,
        )
        new_nodes = textnode.split_nodes_image([node])
        self.assertListEqual(
            [
                textnode.TextNode("This is text with an ", textnode.text_type_text),
                textnode.TextNode("image", textnode.text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
                textnode.TextNode(" and another ", textnode.text_type_text),
                textnode.TextNode(
                    "second image", textnode.text_type_image, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = textnode.TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            textnode.text_type_text,
        )
        new_nodes = textnode.split_nodes_link([node])
        self.assertListEqual(
            [
                textnode.TextNode("This is text with a ", textnode.text_type_text),
                textnode.TextNode("link", textnode.text_type_link, "https://boot.dev"),
                textnode.TextNode(" and ", textnode.text_type_text),
                textnode.TextNode("another link", textnode.text_type_link, "https://blog.boot.dev"),
                textnode.TextNode(" with text that follows", textnode.text_type_text),
            ],
            new_nodes,
        )


class TestTextToNodes(unittest.TestCase):
    def test_from_website(self):
        input = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)" 
        nodes = textnode.text_to_textnodes(input)

        output = [
            textnode.TextNode("This is ", textnode.text_type_text),
            textnode.TextNode("text", textnode.text_type_bold),
            textnode.TextNode(" with an ", textnode.text_type_text),
            textnode.TextNode("italic", textnode.text_type_italic),
            textnode.TextNode(" word and a ", textnode.text_type_text),
            textnode.TextNode("code block", textnode.text_type_code),
            textnode.TextNode(" and an ", textnode.text_type_text),
            textnode.TextNode("obi wan image", textnode.text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"),
            textnode.TextNode(" and a ", textnode.text_type_text),
            textnode.TextNode("link", textnode.text_type_link, "https://boot.dev"),
        ]

        self.assertEqual(nodes, output)


class TestMarkdownToBlock(unittest.TestCase):
    def test_single_block(self):
        input = "A single string"
        output = [input]

        self.assertEqual(textnode.markdown_to_blocks(input), output)

    def test_from_website(self):
        input = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""

        output = [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                """* This is the first list item in a list block
* This is a list item
* This is another list item"""
                ]

        self.assertEqual(textnode.markdown_to_blocks(input), output)

    def test_multiple_empty_lines(self):
        input = """
A line with text


Another line"""

        output = [
                'A line with text',
                'Another line'
                ]

        self.assertEqual(textnode.markdown_to_blocks(input), output)


class TestBlockToBlockType(unittest.TestCase):
    def test_para(self):
        input = "Test string"
        output = textnode.block_type_paragraph
        self.assertEqual(textnode.block_to_block_type(input), output)

    def test_heading(self):
        input = "# Test string"
        output = textnode.block_type_heading
        self.assertEqual(textnode.block_to_block_type(input), output)

    def test_code(self):
        input = "```Test string\nmore stuff```"
        output = textnode.block_type_code
        self.assertEqual(textnode.block_to_block_type(input), output)

    def test_quote(self):
        input = "> Test string\n> Deep and meaningful"
        output = textnode.block_type_quote
        self.assertEqual(textnode.block_to_block_type(input), output)

    def test_ulist(self):
        input = "* Test string\n* Next item"
        output = textnode.block_type_unordered_list
        self.assertEqual(textnode.block_to_block_type(input), output)

    def test_olist(self):
        input = "1. Test string\n2. Next item"
        output = textnode.block_type_ordered_list
        self.assertEqual(textnode.block_to_block_type(input), output)

class TestToHTML(unittest.TestCase):
    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = textnode.markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""

        node = textnode.markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = textnode.markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = textnode.markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = textnode.markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = textnode.markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

if __name__ == "__main__":
    unittest.main()
