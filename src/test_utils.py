import unittest

from textnode import TextNode, TextType
from utils import *

"""
    TODO: Add more tests
    Write test with assertEqual NOT using print !!!
"""

class TestTextNode(unittest.TestCase):
    def test_split_nodes(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        print("\nUTILS --------------\n")
        for n in new_nodes:
            print(n)


if __name__ == "__main__":
    unittest.main()


