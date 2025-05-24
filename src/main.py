from textnode import *
from htmlnode import *


def main():

    tn = TextNode("Some anchor text", TextType.LINK, 'https://go.com')
    print(tn)



main()


