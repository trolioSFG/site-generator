from textnode import *


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    matching = False

    for node in old_nodes:
        words = node.text.split()
        new_text = ""
        words_list = []
        for w in words:
            if matching:
                if w.endswith(delimiter):
                    matching = False
                    words_list.append(w.replace(delimiter, ''))
                    new_nodes.append(TextNode(' '.join(words_list), text_type))
                    words_list = []
                else:
                    words_list.append(w)
            else:
                if w.startswith(delimiter):
                    new_nodes.append(TextNode(' '.join(words_list), TextType.TEXT))
                    matching = True
                    words_list = []
                    words_list.append(w.replace(delimiter, ''))
                else:
                    words_list.append(w)

        if len(words_list) > 0:
           new_nodes.append(TextNode(' '.join(words_list), TextType.TEXT))

    return new_nodes


                    
