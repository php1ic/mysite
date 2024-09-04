import unittest

import htmlnode


class TestHTMLNode(unittest.TestCase):
    def test_tag(self):
        test_tag = 'a'
        node = htmlnode.HTMLNode(tag=test_tag)
        self.assertEqual(node.tag, test_tag)

    def test_props_1(self):
        test_prop = {"href": "https://www.google.com", "target": "_blank", }
        test_output = " href=\"https://www.google.com\" target=\"_blank\""

        node = htmlnode.HTMLNode(props=test_prop)
        self.assertEqual(node.props_to_html(), test_output)

    def test_props_2(self):
        test_prop = {"href": "https://boot.dev", "target": "new_job", }
        test_output = " href=\"https://boot.dev\" target=\"new_job\""

        node = htmlnode.HTMLNode(props=test_prop)
        self.assertEqual(node.props_to_html(), test_output)


if __name__ == "__main__":
    unittest.main()
