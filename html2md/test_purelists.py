import unittest
from h2m.html2md import html2md

from h2m.html2md.assertions import assertEq

__author__ = 'alex'

class ListsTest(unittest.TestCase):
  def test_basic(self):
    in_html = '''
<ul>
<li>item 1</li>
<li>item 2</li>
<li>item 3</li>
</ul>'''

    out_md = '''*    item 1
*    item 2
*    item 3'''
    assertEq(out_md, html2md.html2md(in_html))

  def test_imbricated(self):
    in_html = '''
<ul>
<li>item 1</li>
<li>item 2
<ul>
<li>item 2.1</li>
<li>item 2.2</li>
<li>item 2.3</li>
</ul></li>
<li>item 3</li>
</ul>
'''
    out_md = '''*    item 1
*    item 2
     *    item 2.1
     *    item 2.2
     *    item 2.3
*    item 3'''
    assertEq(out_md, html2md.html2md(in_html))

  def test_paragraph_items(self):
    in_html = '''
<ul>
<li><p>item 1</p></li>
<li><p>item 2</p></li>
<li><p>item 3</p></li>
</ul>
'''
    out_md = '''*    item 1

*    item 2

*    item 3'''
    assertEq(out_md, html2md.html2md(in_html))

  def test_twoparagraph_item(self):
    in_html = '''
<ul>
<li>item 1</li>
<li><p>item 2</p>

<p>item 2 continued</p></li>
<li>item 3</li>
</ul>
'''
    out_md = '''*    item 1
*    item 2

     item 2 continued

*    item 3'''
    assertEq(out_md, html2md.html2md(in_html))

  def test_multipara_plus_imbricated(self):
    in_html = '''
<ul>
<li>item 1</li>
<li><p>item 2</p>

<p>continuation item 2</p>

<ul>
<li>item 2.1</li>
<li>item 2.2</li>
</ul></li>
<li>item 3</li>
</ul>
    '''
    out_md = '''*    item 1
*    item 2

     continuation item 2

     *    item 2.1
     *    item 2.2

*    item 3'''
    assertEq(out_md, html2md.html2md(in_html))

  def test_complex(self):
    in_html = '''
<ul>
<li>item 1</li>
<li><p>item 2</p>

<p>continuation item 2</p>

<ul>
<li>item 2.1</li>
<li>item 2.2</li>
</ul></li>
<li><p>item 3</p></li>
</ul>
'''
    out_md = '''*    item 1
*    item 2

     continuation item 2

     *    item 2.1
     *    item 2.2

*    item 3'''
    assertEq(out_md, html2md.html2md(in_html))    