import unittest

from context import html2md
from assertions import assertEq


__author__ = 'alex'


class ListsTest(unittest.TestCase):
    def test_basic(self):
        in_html = '''<ul>
<li>item 1</li>
<li>item 2</li>
<li>item 3</li>
</ul>'''
        out_md = '''*    item 1
*    item 2
*    item 3'''
        assertEq(out_md, html2md.html2md(in_html))

    def test_imbricated(self):
        in_html = '''<ul>
<li>item 1</li>
<li>item 2
<ol>
<li>sitem 2.1</li>
<li>sitem 2.2</li>
<li>sitem 2.3</li>
</ol>
</li>
<li>item 3</li>
</ul>'''
        out_md = '''*    item 1
*    item 2
     1.    sitem 2.1
     1.    sitem 2.2
     1.    sitem 2.3
*    item 3'''
        assertEq(out_md, html2md.html2md(in_html))

    def test_paragraph_items(self):
        in_html = '''<ul>
<li><p>item 1</p></li>
<li>
<p>item 2</p>
<p>item 2 item 2</p>
<p>item 2 item 2 item 2</p>
</li>
<li>item 3</li>
</ul>'''
        out_md = '''*    item 1

*    item 2

     item 2 item 2

     item 2 item 2 item 2

*    item 3'''
        assertEq(out_md, html2md.html2md(in_html))

    def test_paragraph_mixed(self):
        in_html = '''<ul>
<li>item 1</li>
<li>item 2</li>
<li><p>item 3</p>

<p>item 3 paragraph 2</p></li>
<li>item 4</li>
<li>item 5</li>
</ul>'''
        out_md = '''*    item 1
*    item 2
*    item 3

     item 3 paragraph 2

*    item 4
*    item 5'''
        assertEq(out_md, html2md.html2md(in_html))

    def test_blockquote(self):
        in_html = '''
<ul>
<li><blockquote>
  <p>item 1</p>
</blockquote></li>
<li><blockquote>
  <p>item 2 paragraph 1</p>

<p>item 2 paragraph 2</p>
</blockquote></li>
<li><p>item 3</p></li>
</ul>
'''
        out_md = '''*    > item 1

*    > item 2 paragraph 1

     > item 2 paragraph 2

*    item 3'''
        assertEq(out_md, html2md.html2md(in_html))

    def test_blockquote_complex(self):
        in_html = '''<ul>
<li>item 1</li>
<li><p>item 2</p>

<blockquote>
  <p>item 2 paragraph 1</p>

<p>item 2 paragraph 2</p>
</blockquote></li>
<li><p>item 3</p>

<blockquote>
  <p>item 3 blockquote</p>
</blockquote></li>
</ul>'''
        out_md = '''*    item 1
*    item 2

     > item 2 paragraph 1

     > item 2 paragraph 2

*    item 3

     > item 3 blockquote'''
        assertEq(out_md, html2md.html2md(in_html))

    def test_cheatsheet(self):
        in_html = '''
<ul>
<li><p>A list item.</p>

<p>With multiple paragraphs.</p>

<blockquote>
  <p>And a blockquote</p>
</blockquote></li>
<li><p>Another List item with
a hard wrapped 2nd line.</p>

<pre><code> 10 PRINT "and a code block"
</code></pre></li>
</ul>'''
        out_md = '''*    A list item.

     With multiple paragraphs.

     > And a blockquote

*    Another List item with
     a hard wrapped 2nd line.

         10 PRINT "and a code block"'''
        assertEq(out_md, html2md.html2md(in_html))


if __name__ == '__main__':
    unittest.main()