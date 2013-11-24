import unittest

from context import html2md
from assertions import assertEq


__author__ = 'alex'


class BlockquoteTest(unittest.TestCase):
    def test_no_paragraph(self):
        in_html = '''<blockquote>some text</blockquote>'''
        out_md = '''> some text'''
        assertEq(out_md, html2md.html2md(in_html))

    def test_paragraph(self):
        in_html = '''<blockquote><p>some text</p></blockquote>'''
        out_md = '''> some text'''
        assertEq(out_md, html2md.html2md(in_html))

    def test_multi_paragraph(self):
        in_html = '''<blockquote>
<p>some paragraph</p>
<p>another paragraph</p>
</blockquote>'''
        out_md = '''> some paragraph

> another paragraph'''
        assertEq(out_md, html2md.html2md(in_html))

    def test_multi_line_prefix(self):
        in_html = '''<blockquote>
<p>some paragraph
that has multiple lines</p>
<p>another paragraph that has
three lines
in total</p>
</blockquote>'''
        out_md = '''> some paragraph
> that has multiple lines

> another paragraph that has
> three lines
> in total'''
        assertEq(out_md, html2md.html2md(in_html))

    def test_pre(self):
        in_html = '''<blockquote>
<pre><code>{
  "_id" : ObjectId("4bfea7246c6151d127f80100"),
  ...
  "created" : { "d" : "2010-03-29", "t" : "20:15:34" }
}</code></pre>
</blockquote>'''
        out_md = '''>     {
>       "_id" : ObjectId("4bfea7246c6151d127f80100"),
>       ...
>       "created" : { "d" : "2010-03-29", "t" : "20:15:34" }
>     }'''
        assertEq(out_md, html2md.html2md(in_html))

    def test_list(self):
        in_html = '''<blockquote>
<ol><li>MongoDB assumes that you have a 64-bit machine</li>
<li>MongoDB assumes that you're using a little-endian system</li>
<li>MongoDB assumes that you have more than one server</li>
<li>MongoDB assumes you want fast/unsafe, but lets you do slow/safe</li>
<li>MongoDB developers assume you'll complain if something goes wrong</li>
</ol></blockquote>'''
        out_md = '''> 1.  MongoDB assumes that you have a 64-bit machine
> 1.  MongoDB assumes that you're using a little-endian system
> 1.  MongoDB assumes that you have more than one server
> 1.  MongoDB assumes you want fast/unsafe, but lets you do slow/safe
> 1.  MongoDB developers assume you'll complain if something goes wrong'''
        assertEq(out_md, html2md.html2md(in_html))

    def test_complex(self):
        in_html = '''<blockquote>
<p>MongoDB assumes that you have a 64-bit machine</p>
<blockquote>
<p>MongoDB assumes that you're using a little-endian system</p>
<p>MongoDB assumes that you have more than one server</p>
</blockquote>
<p>MongoDB assumes you want fast/unsafe, but lets you do slow/safe</p>
</blockquote>'''
        out_md = '''> MongoDB assumes that you have a 64-bit machine

> > MongoDB assumes that you're using a little-endian system

> > MongoDB assumes that you have more than one server

> MongoDB assumes you want fast/unsafe, but lets you do slow/safe'''
        assertEq(out_md, html2md.html2md(in_html))


if __name__ == '__main__':
    unittest.main()