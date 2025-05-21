import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq_URL(self):
        n1 = TextNode("Node 1", TextType.BOLD)
        n2 = TextNode("Node 1", TextType.BOLD, 'https://go.com')
        self.assertNotEqual(n1, n2)

    def test_neq_type(self):
        n1 = TextNode("Node 1", TextType.BOLD)
        n2 = TextNode("Node 1", TextType.ITALIC)
        self.assertNotEqual(n1, n2)

    def test_neq_text(self):
        n1 = TextNode("Node 1", TextType.BOLD)
        n2 = TextNode("Node 2", TextType.BOLD)
        self.assertNotEqual(n1, n2)


if __name__ == "__main__":
    unittest.main()

