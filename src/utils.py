import re

from textnode import *
from block import *
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


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        text = node.text

        while text:
            try:
                start = text.index(delimiter)
                end = text.index(delimiter, start + len(delimiter)) + len(delimiter)
                new_nodes.append(TextNode(text[:start], node.text_type))
                new_nodes.append(TextNode(text[start:end].replace(delimiter, ''), text_type))
                text = text[end:]
            except ValueError:
                new_nodes.append(TextNode(text, node.text_type))
                text = ''

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
                props = {"src": child.url, "alt": child.text}
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

            case BlockType.quote:
                """
                html_children = []
                lines = list(map(lambda x: x[1:], b.strip().split("\n")))
                for l in lines:
                    for n in text_to_children(l):
                        html_children.append(n)

                """
                b = b.lstrip()
                b = b.replace('\n>', '\n')
                b = b.lstrip('>')
                if b[-1] != '\n':
                    b = b + '\n'
                html_children = text_to_children(b)
                html_nodes.append(ParentNode("blockquote", html_children, None))

            case BlockType.unordered_list:
                
                # Blocks are stripped
                items = b.split("\n- ")
                items[0] = items[0].replace('- ', '')
                html_children = []
                for item in items:
                    html_children.append(ParentNode("li", text_to_children(item)))
                html_nodes.append(ParentNode("ul", html_children, None))

            case BlockType.ordered_list:

                # Blocks are stripped
                start = 3
                html_children = []
                for m in re.finditer("^\d+\. ", b[3:], re.MULTILINE):
                    text = b[start:m.start()+3].strip()
                    html_children.append(ParentNode("li", text_to_children(text)))
                    start = m.start() + 3 + len(m.group(0))

                text = b[start:].strip()
                html_children.append(ParentNode("li", text_to_children(text)))

                html_nodes.append(ParentNode("ol", html_children, None))

            case BlockType.heading:
                start = re.match("^#{1,6} ", b).end()
                html_children = text_to_children(b[start:])
                html_nodes.append(ParentNode("h"+str(start-1), html_children, None))

            case BlockType.code:
                # ESPECIAL, NO INLINE
                html_children = [text_node_to_html_node(TextNode(b[3:-3], TextType.TEXT))]
                html_nodes.append(ParentNode("pre", [ParentNode("code", html_children, None)], None))

            case _:
                raise Exception("Not implemented")

    return ParentNode("div", html_nodes, None)
