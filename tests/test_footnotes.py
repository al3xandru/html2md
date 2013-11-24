import unittest

from context import html2md
from assertions import assertEq


__author__ = 'alex'


class Footnotes(unittest.TestCase):
    def test_footnoteref_basic(self):
        in_html = '''<p>Some footnote reference<sup id="fnref:1492395-1"><a href="#fn:1492395-1" rel="footnote">[1]</a></sup> followed by text</p>'''
        out_md = '''Some footnote reference[^1] followed by text'''
        assertEq(out_md, html2md.html2md(in_html))

    def test_footnoteref_oldstyle(self):
        in_html = '''<p>Some footnote ref<sup id="fnref:1"><q>[<a href="#fn:1" rel="footnote">1</a>]</q></sup> followed by text</p>'''
        out_md = '''Some footnote ref[^1] followed by text'''
        assertEq(out_md, html2md.html2md(in_html))


    def test_footnote(self):
        in_html = '''
<div class="footnotes">
<hr>
<ol>
<li id="fn:1">A nice visualization <a href="http://nosql.mypopescu.com/post/609721873/who-is-using-hbase">here</a>.
(<a class="footnoteBackLink" href="#fnref:1" rev="footnote" title="Jump back to footnote 1 in the text">h</a>)</li>
<li id="fn:2">A nice visualization of HBase (<a class="footnoteBackLink" href="#fnref:1" rev="footnote" title="Jump back to footnote 1 in the text">h</a>)</li>
</ol>
</div>
'''
        out_md = '''

[^1]: A nice visualization [here](http://nosql.mypopescu.com/post/609721873/who-is-using-hbase).

[^2]: A nice visualization of HBase '''
        assertEq(out_md, html2md.html2md(in_html))


if __name__ == '__main__':
    unittest.main()