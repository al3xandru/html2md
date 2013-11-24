from h2m.html2md import html2md

__author__ = 'alex'

import unittest

from h2m.html2md.assertions import assertEq

class HtmlAttributesTest(unittest.TestCase):
  def test_h2_attributes(self):
    in_html = '''<h2 id="h2_id">Very simple H2</h2>'''
    out_md = '''## Very simple H2 [..]("{{h2:#h2_id}}")'''
    assertEq(out_md, html2md.html2md(in_html))

  def test_paragraph_attributes(self):
    in_html = '''<p style="margin-top:2em;" id="pid" class="pclass">something to write in here </p>'''
    out_md = '''something to write in here  [..]("{{p:#pid pclass style='margin-top:2em;'}}")'''
    assertEq(out_md, html2md.html2md(in_html))



