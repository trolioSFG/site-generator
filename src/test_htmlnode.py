import unittest

from htmlnode import HTMLNode
from textnode import *
from utils import text_node_to_html_node


class TestHTMLNode(unittest.TestCase):
    def test_print(self):
        hn = HTMLNode('a', 'This is a link', None, None)
        print(hn)

    def test_print_props(self):
        print("TEST_PRINT_PROPS")
        hnlink = HTMLNode('a', 'Children link', None, {"href": "https://boot.dev"})
        print(hnlink)
        print("props_to_html():")
        print(hnlink.props_to_html())
        print("END TEST_PRINT_PROPS")

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


    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")


    def test_bold(self):
        node = TextNode("This is a BOLD node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'b')
        self.assertEqual(html_node.value, "This is a BOLD node")

    def test_link(self):
        node = TextNode("This is a link", TextType.LINK, "http://go.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props["href"], "http://go.com")

    def test_img(self):
        text = "This is an IMAGE",
        node = TextNode( text, TextType.IMAGE, "http://go.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["src"], "http://go.com")
        self.assertEqual(html_node.props["alt"], text)

