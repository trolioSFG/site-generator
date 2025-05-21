from textnode import *
from htmlnode import *

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            node = LeafNode(None, text_node.text)
            return node
        case TextType.BOLD:
            node = LeafNode('b', text_node.text)
            return node
        case TextType.ITALIC:
            return LeafNode('i', text_node.text)
        case TextType.CODE:
            return LeafNode('code', text_node.text)
        case TextType.LINK:
            return LeafNode('a', text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode('img', '', {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Wrong TextType")


def main():

    tn = TextNode("Some anchor text", TextType.LINK, 'https://go.com')
    print(tn)



main()


