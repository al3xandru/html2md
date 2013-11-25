import unittest

from context import html2md
from assertions import assertEq


__author__ = 'alex'


class HtmlAttributesTest(unittest.TestCase):
    def test_h2_attributes(self):
        in_html = u'''<h2 id="h2_id">Very simple H2</h2>'''
        out_md = u'''## Very simple H2 [..]("{{h2:#h2_id}}")'''
        assertEq(out_md, html2md.html2md(in_html))

    def test_paragraph_attributes(self):
        in_html = u'''<p style="margin-top:2em;" id="pid" class="pclass">something to write in here </p>'''
        out_md = u'''something to write in here  [..]("{{p:#pid pclass style='margin-top:2em;'}}")'''
        assertEq(out_md, html2md.html2md(in_html))

    def test_disabled_attributes(self):
        in_html = u'''<center>a stupid example</center>'''
        out_md = u'''a stupid example'''
        assertEq(out_md, html2md.html2md(in_html, attrs=False))

        in_html = u'''<h2 id="h2_id">Very simple H2</h2>'''
        out_md = u'''## Very simple H2'''
        assertEq(out_md, html2md.html2md(in_html, attrs=False))

        in_html = u'''<p style="margin-top:2em;" id="pid" class="pclass">something to write in here </p>'''
        out_md = u'''something to write in here'''
        assertEq(out_md, html2md.html2md(in_html, attrs=False))


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(HtmlAttributesTest)

if __name__ == '__main__':
    unittest.main()
