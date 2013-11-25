import unittest

from context import html2md
from assertions import assertEq


__author__ = 'alex'


class HtmlAttributesTest(unittest.TestCase):
    def test_h2_attributes(self):
        in_html = u'''<h2 id="h2_id">Very simple H2</h2>'''
        out_md = u'''## Very simple H2 [..]("{{h2:#h2_id}}")'''
        assertEq(out_md, html2md.html2md(in_html, strip=True))

    def test_paragraph_attributes(self):
        in_html = '''<p style="margin-top:2em;" id="pid" class="pclass">something to write in here </p>'''
        out_md = '''something to write in here  [..]("{{p:#pid pclass style='margin-top:2em;'}}")'''
        assertEq(out_md, html2md.html2md(in_html, strip=True))

def suite():
    return unittest.TestLoader().loadTestsFromTestCase(HtmlAttributesTest)

if __name__ == '__main__':
    unittest.main()
