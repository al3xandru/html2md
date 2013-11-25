import unittest

from context import html2md
from assertions import assertEq


__author__ = 'alex'


class SpecialListsTest(unittest.TestCase):
    def test_text_and_paragraph(self):
        in_html = '''<ul>
<li>item 1</li>
<li>item 2
<p>item 2 paragraph</p>
<p>item 2 item 2</p>
</li>
<li>item 3</li>
</ul>'''
        out_md = '''*   item 1
*   item 2

    item 2 paragraph

    item 2 item 2

*   item 3'''
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
        out_md = '''*   item 1
*   item 2
*   item 3

    item 3 paragraph 2

*   item 4
*   item 5'''
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
        out_md = '''*   > item 1

*   > item 2 paragraph 1

    > item 2 paragraph 2

*   item 3'''
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
        out_md = '''*   item 1
*   item 2

    > item 2 paragraph 1

    > item 2 paragraph 2

*   item 3

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

<pre><code>
project/
    __init__.py
    example1.py
    test/
        __init__.py
        test_example1.py
</code></pre></li>
</ul>'''
        out_md = '''*   A list item.

    With multiple paragraphs.

    > And a blockquote

*   Another List item with
    a hard wrapped 2nd line.

        project/
            __init__.py
            example1.py
            test/
                __init__.py
                test_example1.py'''
        assertEq(out_md, html2md.html2md(in_html))


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(SpecialListsTest)


if __name__ == '__main__':
    unittest.main()