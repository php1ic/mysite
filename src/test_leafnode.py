import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_1(self):
        node = LeafNode("p", "This is a paragraph of text.")
        output = "<p>This is a paragraph of text.</p>"
        self.assertEqual(node.to_html(), output)

    def test_leaf_2(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        output = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(node.to_html(), output)

    def test_no_tag(self):
        node = LeafNode(None, "Some text")
        output = "Some text"
        self.assertEqual(node.to_html(), output)
