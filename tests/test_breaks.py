import unittest

from context import html2md
from assertions import assertEq


class ParagraphBreaksText(unittest.TestCase):
    def test_linebreak(self):
        in_html = '''<p>This is a paragraph with<br />
a forced line break<br />
used in 2 places.'''
        out_md = '''This is a paragraph with
a forced line break
used in 2 places.'''
        assertEq(out_md, html2md.html2md(in_html))



if  __name__ == '__main__':
    unittest.main()