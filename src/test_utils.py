import unittest

from textnode import TextNode, TextType
from utils import *
from htmlnode import *


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

    def test_split_multinodes(self):
        node1 = TextNode("This is **more bold** and _italic_ test", TextType.TEXT)
        node2 = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        
        self.assertListEqual([TextNode("This is ", TextType.TEXT)
                              , TextNode("more bold", TextType.BOLD)
                              , TextNode(" and ", TextType.TEXT)
                              , TextNode("italic", TextType.ITALIC)
                              , TextNode(" test", TextType.TEXT)
                              , TextNode("This is text with a ", TextType.TEXT)
                              , TextNode("code block", TextType.CODE)
                              , TextNode(" word", TextType.TEXT)
                              ], new_nodes)



    def test_split_italic_bold(self):
        node = TextNode("Fucking **order** matters. FALSE: Don't use * for italics, USE <underscore> like so: _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)

        new_nodes2 = split_nodes_delimiter([node], "_", TextType.ITALIC)
        new_nodes2 = split_nodes_delimiter(new_nodes2, "**", TextType.BOLD)

        self.assertListEqual(new_nodes, new_nodes2)


    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")
                              , ("to youtube", "https://www.youtube.com/@bootdotdev")]
                             , matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_begin(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) at the beginning and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" at the beginning and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )


    def test_split_links(self):
        node = TextNode(
            "[link](https://i.imgur.com/zjjcJKZ.png) at the beginning and [another link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" at the beginning and ", TextType.TEXT),
                TextNode(
                    "another link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_text_2_textnodes(self):

        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        new_nodes = text_to_textnodes(text)
        print("\nTEXT 2 TEXTNODES\n")
        for n in new_nodes:
            print(n)


        print("\n----------------\n")

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_paragraphs(self):
        md = """This is **bolded** paragraph text in a p tag here

This is another paragraph with _italic_ text and `code` here
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_blockquote(self):
        md = """
>Quote 1
>Quote 2 with **bold** and _italic_
"""
        node = markdown_to_html_node(md)
        self.assertEqual("<div><blockquote>Quote 1\nQuote 2 with <b>bold</b> and <i>italic</i>\n</blockquote></div>", node.to_html())


    def test_blockquote_extra(self):
        md = """
Antes

>Quote 1
>Quote 2 with **bold** and _italic_

Despues
"""
        node = markdown_to_html_node(md)
        self.assertEqual("<div><p>Antes</p><blockquote>Quote 1\nQuote 2 with <b>bold</b> and <i>italic</i>\n</blockquote><p>Despues</p></div>", node.to_html())

    def test_unordered(self):
        md = """
- Un 1
Varias lineas
- Un 2 with **bold** and _italic_
- ITEM 3
"""
        node = markdown_to_html_node(md)
        self.assertEqual("<div><ul><li>Un 1\nVarias lineas</li><li>Un 2 with <b>bold</b> and <i>italic</i></li><li>ITEM 3</li></ul></div>"
                         , node.to_html())

    def test_unordered_extra(self):
        md = """
Antes

- Un 1
Varias lineas
- Un 2 with **bold** and _italic_
- ITEM 3

Despues
"""
        node = markdown_to_html_node(md)
        self.assertEqual("<div><p>Antes</p><ul><li>Un 1\nVarias lineas</li><li>Un 2 with <b>bold</b> and <i>italic</i></li><li>ITEM 3</li></ul><p>Despues</p></div>"
                         , node.to_html())


    def test_ordered(self):
        md = """
1. Un 1
2. Un 2 with **bold** and _italic_
3. ITEM 3
"""
        node = markdown_to_html_node(md)
        self.assertEqual("<div><ol><li>Un 1</li><li>Un 2 with <b>bold</b> and <i>italic</i></li><li>ITEM 3</li></ol></div>"
                         , node.to_html())


if __name__ == "__main__":
    unittest.main()


