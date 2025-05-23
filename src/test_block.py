import unittest

from block import *

class TestBlock(unittest.TestCase):
    def test_block_code(self):
        md = """
```
Code block 1
Code block 2
```
"""
        md = md.strip()
        self.assertEqual(BlockType.code, block_to_block_type(md))

    def test_block_qupte(self):
        md = """
>Quote block 1
>Quote block 2
"""

        md = md.strip()
        self.assertEqual(BlockType.quote, block_to_block_type(md))


    def test_ordered_block(self):
        md = """1. Linea1
2. Linea2
3. Linea3
"""
        md = md.strip()
        self.assertEqual(BlockType.ordered_list, block_to_block_type(md))

    def test_ordered_block_FAIL(self):
        md = """10. Linea1
2. Linea2
3. Linea3
"""
        md = md.strip()
        self.assertNotEqual(BlockType.ordered_list, block_to_block_type(md))

    def test_paragraph(self):
        md = """A normal paragraph.
Second line in the paragraph
"""
        md = md.strip()
        self.assertEqual(BlockType.paragraph, block_to_block_type(md))


if __name__ == "__main__":
    unittest.main()

