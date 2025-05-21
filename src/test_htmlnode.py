import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_print(self):
        hn = HTMLNode('a', 'This is a link', None, None)
        print(hn)

    def test_print_props(self):
        hnlink = HTMLNode('a', 'Children link', None, {"href": "https://boot.dev"})
        print(hnlink)
        print("props_to_html():")
        print(hnlink.props_to_html())

    def test_print_children(self):
        hnlink = HTMLNode('a', 'Children link', None, {"href": "https://boot.dev"})
        hn = HTMLNode('div', 'This is a DIV', None, None)
        hn2 = HTMLNode('p', 'A paragraph with a link', [hn, hnlink], None)
        print(hn2)
        print(hnlink)

    def test_empty(self):
        print("Empty node")
        en = HTMLNode()
        print(en)
