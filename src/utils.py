import re

from textnode import *
from block import *
from htmlnode import *


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    # TODO: Hacerlo SIN split ????????????????????????????????
    for node in old_nodes:
        words = node.text.split()
        new_text = ""
        words_list = []
        matching = False

        for w in words:
            if matching:
                if w.endswith(delimiter):
                    matching = False
                    words_list.append(w.replace(delimiter, ''))
                    new_nodes.append(TextNode(' '.join(words_list), text_type))
                    # TODO: pa<b>la</b>bra ya NO funcionaria
                    # Asi tampoco
                    # words_list = [' ']
                    words_list = []
                else:
                    words_list.append(w)
            else:
                # Nesting is NOT allowed
                # Italic Bold NOS possible
                if w.startswith(delimiter) and w[len(delimiter)] != delimiter[0]:
                    # new_nodes.append(TextNode(' '.join(words_list), TextType.TEXT))
                    # TODO: pa<b>la</b>bra ya NO funcionaria
                    # NO FUNCIONA
                    # words_list.append(' ')
                    new_nodes.append(TextNode(' '.join(words_list), node.text_type, node.url))
                    matching = True
                    words_list = []
                    # One word match
                    if w.endswith(delimiter):
                        matching = False
                        new_nodes.append(TextNode(w.replace(delimiter, ''), text_type))
                    else:
                        words_list.append(w.replace(delimiter, ''))
                else:
                    words_list.append(w)

        if len(words_list) > 0:
           new_nodes.append(TextNode(' '.join(words_list), node.text_type, node.url))

    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"\!\[([ \w]+)\]\(([^ ]+)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(^|[^\!])\[([ \w]+)\]\(([^ ]+)\)", text)
    for i in range(len(matches)):
        # We don't want Start of line OR character previous to [
        # We must match to avoid matching a link in an image
        # tuple slicing ONLY in Python3
        matches[i]= matches[i][1:]

    return matches


# TODO:
#
#   - Usa _ para italic
#   - NO confundir link con image. Si buscamos LINK >> no << podemos devolver el de IMAGE !!!


def split_nodes_image(old_nodes):

    # while match(node)
    #   new_nodes = [pre, image, post]
    #   pre = node until FIRST image delimiter
    #       if not empty add to new_nodes
    #   image = <delimiter>text url<delimiter>
    #       add to new_nodes
    #   post = rest
    #   node = post
    # if node not empty
    #   add to new_nodes

    new_nodes = []
    for node in old_nodes:
        text = node.text
        images = extract_markdown_images(text)
        # print("Text:", text)
        # print("Alt text:", images[0][0])
        
        while images:
            del_start = text.index(f"![{images[0][0]}")
            # print("del_start:", del_start)
            if del_start > 0:
                new_nodes.append(TextNode(text[:del_start], node.text_type, node.url))
            new_nodes.append(TextNode(images[0][0], TextType.IMAGE, images[0][1]))
            del_end = text.index(images[0][1]) + len(images[0][1]) + 1
            if del_end < len(text):
                text = text[del_end:]
            else:
                text = ''
            
            images = extract_markdown_images(text)

        if text:
            new_nodes.append(TextNode(text, node.text_type, node.url))

    return new_nodes



def split_nodes_link(old_nodes):

    # while match(node)
    #   new_nodes = [pre, image, post]
    #   pre = node until FIRST image delimiter
    #       if not empty add to new_nodes
    #   image = <delimiter>text url<delimiter>
    #       add to new_nodes
    #   post = rest
    #   node = post
    # if node not empty
    #   add to new_nodes

    new_nodes = []
    for node in old_nodes:
        text = node.text
        links = extract_markdown_links(text)
        
        while links:
            del_start = text.index(f"[{links[0][0]}")
            if del_start > 0:
                new_nodes.append(TextNode(text[:del_start], node.text_type, node.url))
            new_nodes.append(TextNode(links[0][0], TextType.LINK, links[0][1]))
            del_end = text.index(links[0][1]) + len(links[0][1]) + 1
            if del_end < len(text):
                text = text[del_end:]
            else:
                text = ''
            
            links = extract_markdown_links(text)

        if text:
            new_nodes.append(TextNode(text, node.text_type, node.url))

    return new_nodes



def text_to_textnodes(text):
    new_nodes = []

    node = TextNode(text, TextType.TEXT)

    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_link(new_nodes)
    new_nodes = split_nodes_image(new_nodes)

    return new_nodes


def markdown_to_blocks(markdown):

    blocks = markdown.split("\n\n")

    for i in range(len(blocks)):
        blocks[i] = blocks[i].strip()
        if blocks[i] == '' or blocks[i] == '\n':
            blocks.remove(blocks[i])

    return blocks

def text_to_children(text):

    children = text_to_textnodes(text)
    html_children = []

    for child in children:
        tag = ''
        match child.text_type:
            case TextType.TEXT:
                tag = None
                value = child.text
                props = None
            case TextType.BOLD:
                tag = "b"
                value = child.text
                props = None
            case TextType.ITALIC:
                tag = "i"
                value = child.text
                props = None
            case TextType.LINK:
                tag = "a"
                value = child.text
                props = {"href": child.url}
            case TextType.IMAGE:
                tag = "img"
                value = child.text
                props = {"src": child.url}
            case TextType.CODE:
                tag = "code"
                value = child.text
                props = None
            case _:
                raise Exception("Unknown TextType: " + child.text_type)

        
        html_children.append(LeafNode(tag, value, props))

    
    return html_children




def markdown_to_html_node(markdown):
    
    blocks = markdown_to_blocks(markdown)
    html_nodes = []

    for b in blocks:
        match block_to_block_type(b):
            case BlockType.paragraph:
                html_children = text_to_children(b)
                # hnode = HTMLNode('p', b, TODO_CHILDREN)
                html_nodes.append(ParentNode("p", html_children, None))


            case _:
                raise Exception("Not implemented")

    return ParentNode("div", html_nodes, None)
