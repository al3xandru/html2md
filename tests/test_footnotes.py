# -*- coding: utf8 -*-
import unittest

from context import html2md
from assertions import assertEq


__author__ = 'alex'


class Footnotes(unittest.TestCase):
    def test_footnoteref_basic(self):
        in_html = '''<p>Some footnote reference<sup id="fnref:1492395-1"><a href="#fn:1492395-1" rel="footnote">[1]</a></sup> followed by text</p>'''
        out_md = '''Some footnote reference[^1] followed by text'''
        assertEq(out_md, html2md.html2md(in_html, footnotes=True))

    def test_footnoteref_oldstyle(self):
        in_html = '''<p>Some footnote ref<sup id="fnref:1"><q>[<a href="#fn:1" rel="footnote">1</a>]</q></sup> followed by text</p>'''
        out_md = '''Some footnote ref[^1] followed by text'''
        assertEq(out_md, html2md.html2md(in_html, footnotes=True))

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

[^2]: A nice visualization of HBase'''
        assertEq(out_md, html2md.html2md(in_html, footnotes=True))



EXAMPLES = u'''
<p>of my Mac. Luckily the Sonos forums are pretty good.<sup id="fnref:forums"><a href="#fn:forums" rel="footnote" sl-processed="1">1</a></sup></p>

<div class="footnote">
<hr>
<ol>
<li id="fn:forums">
<p>Not from the Synology Media Server &nbsp;<a href="#fnref:forums" rev="footnote" title="Jump back to footnote 1 in the text" sl-processed="1">↩</a></p>
</li>
</ol>
</div>


<p>your computing needs.<sup id="fnref:1"><a href="#fn:1" rel="footnote">1</a></sup> Nobody’s </p>

<div class="footnotes">
<hr>
<ol>

<li id="fn:1">
<p>If et an iPad at all.</p>

<p>You'd reading.&nbsp;<a href="#fnref:1" rev="footnote">↩</a></p>
</li>

</ol>
</div>

<p>display in this year’s Mini,<sup id="fnr1-2013-11-15"><a href="#fn1-2013-11-15">1</a></sup> but it never even </p>

<div class="footnotes">
<hr>
<ol>
<li id="fn1-2013-11-15">
<p>first generation.&nbsp;<a href="#fnr1-2013-11-15" class="footnoteBackLink" title="Jump back to footnote 1 in the text.">↩</a></p>
</li>
</ol>
</div>

<p>I'd really love to know how this is done<sup id="fnref:2-fn-done"><a href="#fn:2-fn-done" rel="footnote" target="_blank">1</a></sup>.</p>

<div class="footnote">
<hr><ol><li id="fn:2-fn-done">
<p>than to speculate.&nbsp;<a href="#fnref:2-fn-done" rev="footnote" title="Jump back to footnote 1 in the text" target="_blank">↩</a></p>
</li>
</ol></div>
'''

if __name__ == '__main__':
    unittest.main()