import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        output = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(), output)

    def test_simple_child(self):
        node = ParentNode("a", [LeafNode("b", "Some Text")])
        output = "<a><b>Some Text</b></a>"
        self.assertEqual(node.to_html(), output)
