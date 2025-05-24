from enum import Enum
import re


class BlockType(Enum):
    paragraph = 0
    heading = 1
    code = 2
    quote = 3
    unordered_list = 4
    ordered_list = 5

def block_to_block_type(block):

    matches = re.findall(r"^(#{1,6})\s(.+)$", block)

    if matches:
        return BlockType.heading

    # matches = re.findall(r"^```.+```$", block, re.MULTILINE)
    if block.startswith("```") and block.endswith("```"):
        return BlockType.code

    matches = re.findall(r"^(^>.+$)+$", block, re.MULTILINE)
    if matches:
        return BlockType.quote

    matches = re.findall(r"^(^- .+$)+$", block, re.MULTILINE)
    if matches:
        return BlockType.unordered_list

    # TODO: FAILS when an item contains multiple lines
    lines = block.split("\n")
    index = 1
    ordered = True
    for line in lines:
        if ordered:
            matches = re.findall(r"^(\d+)\. .+$", line)
            # print(f"\nORDERED: {matches}\n")

            if matches:
                # print("\nOrdered:", index, int(matches[0]))
                if int(matches[0]) != index:
                    ordered = False
                else:
                    index = index + 1
            else:
                ordered = False

    if ordered:
        return BlockType.ordered_list

    
    return BlockType.paragraph

