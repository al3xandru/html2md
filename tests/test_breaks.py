import unittest

from context import html2md
from assertions import assertEq


class BreaksText(unittest.TestCase):
    def test_linebreak(self):
        in_html = '''<p>This is a paragraph with<br />
a forced line break<br />
used in 2 places.'''
        out_md = u'''This is a paragraph with  
a forced line break  
used in 2 places.'''
        assertEq(out_md, html2md.html2md(in_html, strip=True))


    def test_hr(self):
        in_html = u'''<p>Some text.</p>
<hr/>
<p>Follow up text.</p>'''
        out_md = u'''Some text.

-----

Follow up text.'''
        assertEq(out_md, html2md.html2md(in_html, strip=True))


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(BreaksText)


if  __name__ == '__main__':
    unittest.main()

