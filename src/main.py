import os
from shutil import copy, rmtree
import logging
import re
import sys


from textnode import *
from htmlnode import *
from utils import markdown_to_html_node


logger = logging.getLogger(__name__)
logging.basicConfig(filename="copy_dir.log", encoding='utf-8', level = logging.DEBUG)


def extract_title(markdown):
    m = re.search("^# (.+)$$", markdown, re.MULTILINE)

    if not m:
        raise Exception("No h1 header")
    else:
        return m.group(1).strip()

def generate_page(from_path, template_path, dest_path, basepath):

    logger.info(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # contents = ""
    # tmplte = ""

    with open(from_path, "r") as f:
        contents = f.read()
    
    with open(template_path, "r") as f:
        tmplte = f.read()

    node = markdown_to_html_node(contents)
    html = node.to_html()

    title = extract_title(contents)

    tmplte = tmplte.replace("{{ Title }}", title)
    tmplte = tmplte.replace("{{ Content }}", html)
    tmplte = tmplte.replace("href=\"/", f"href=\"{basepath}")
    tmplte = tmplte.replace("src=\"/", f"src=\"{basepath}")

    with open(dest_path, "w") as f:
        f.write(tmplte)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):

    for fd in os.listdir(dir_path_content):
        src = os.path.join(dir_path_content, fd)
        dst = os.path.join(dest_dir_path, fd)
        logger.info(f"Analyzing {src} -> {dst}")

        if os.path.isfile(src):
            # Check MD ?
            logger.info(f"FILE {src}")
            generate_page(src, template_path, dst.replace('.md', '.html'), basepath)
        else:
            if not os.path.exists(dst):
                logger.info(f"Created dir {dst}")
                os.mkdir(dst)
            generate_pages_recursive(src, template_path, dst, basepath)




def copy_dir(org_dir, dst_dir):

    if os.path.exists(dst_dir):
        logger.info(f"{dst_dir} exists. Deletting")
        rmtree(dst_dir)

    os.mkdir(dst_dir)
    logger.info(f"Created {dst_dir}")

    for fd in os.listdir(org_dir):
        src = os.path.join(org_dir, fd)
        dst = os.path.join(dst_dir, fd)

        if os.path.isfile(src):
            copy(src, dst)
            logger.info(f"{src} copied to {dst}")
        else:
            copy_dir(src, dst)

def main():

    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    print("Basepath:", basepath)


    # tn = TextNode("Some anchor text", TextType.LINK, 'https://go.com')
    # print(tn)

    print("Copy 'static' to 'docs'")
    copy_dir("static", "docs")

    """
    generate_page("content/index.md", "template.html", "public/index.html")
    generate_page("content/blog/glorfindel/index.md", "template.html", "public/blog/glorfindel/index.html")
    """

    generate_pages_recursive("content", "template.html", "docs", basepath)


main()


