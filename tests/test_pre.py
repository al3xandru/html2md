import unittest

from context import html2md
from assertions import assertEq


class PreTest(unittest.TestCase):
    def test_default(self):
        in_html = u'''
<pre>
def getText(self, separator=u""):
    if not len(self.contents):
        return u""
    stopNode = self._lastRecursiveChild().next
    strings = []
    current = self.contents[0]
    while current is not stopNode:
        if isinstance(current, NavigableString):
            strings.append(current.strip())
        current = current.next
    return separator.join(strings)
text = property(getText)
</pre>'''
        out_md = u'''
    def getText(self, separator=u""):
        if not len(self.contents):
            return u""
        stopNode = self._lastRecursiveChild().next
        strings = []
        current = self.contents[0]
        while current is not stopNode:
            if isinstance(current, NavigableString):
                strings.append(current.strip())
            current = current.next
        return separator.join(strings)
    text = property(getText)'''

        assertEq(out_md, html2md.html2md(in_html))

    def test_default_with_attributes(self):
        in_html = u'''
<pre class="code python literal-block">
def getText(self, separator=u""):
    if not len(self.contents):
        return u""
    stopNode = self._lastRecursiveChild().next
    strings = []
    current = self.contents[0]
    while current is not stopNode:
        if isinstance(current, NavigableString):
            strings.append(current.strip())
        current = current.next
    return separator.join(strings)
text = property(getText)
</pre>'''
        out_md = u'''
    def getText(self, separator=u""):
        if not len(self.contents):
            return u""
        stopNode = self._lastRecursiveChild().next
        strings = []
        current = self.contents[0]
        while current is not stopNode:
            if isinstance(current, NavigableString):
                strings.append(current.strip())
            current = current.next
        return separator.join(strings)
    text = property(getText)'''

        assertEq(out_md, html2md.html2md(in_html))

    def test_default_with_code(self):
        in_html = u'''
<pre><code>
def getText(self, separator=u""):
    if not len(self.contents):
        return u""
    stopNode = self._lastRecursiveChild().next
    strings = []
    current = self.contents[0]
    while current is not stopNode:
        if isinstance(current, NavigableString):
            strings.append(current.strip())
        current = current.next
    return separator.join(strings)
text = property(getText)
</code></pre>'''
        out_md = u'''
    def getText(self, separator=u""):
        if not len(self.contents):
            return u""
        stopNode = self._lastRecursiveChild().next
        strings = []
        current = self.contents[0]
        while current is not stopNode:
            if isinstance(current, NavigableString):
                strings.append(current.strip())
            current = current.next
        return separator.join(strings)
    text = property(getText)'''

        assertEq(out_md, html2md.html2md(in_html))

    def test_github_with_attributes(self):
        in_html = u'''
<p>A code sample:</p>
<pre class="code python literal-block">
def getText(self, separator=u""):
    if not len(self.contents):
        return u""
    stopNode = self._lastRecursiveChild().next
    strings = []
    current = self.contents[0]
    while current is not stopNode:
        if isinstance(current, NavigableString):
            strings.append(current.strip())
        current = current.next
    return separator.join(strings)
text = property(getText)
</pre>'''
        out_md = u'''
A code sample:

```code python literal-block
def getText(self, separator=u""):
    if not len(self.contents):
        return u""
    stopNode = self._lastRecursiveChild().next
    strings = []
    current = self.contents[0]
    while current is not stopNode:
        if isinstance(current, NavigableString):
            strings.append(current.strip())
        current = current.next
    return separator.join(strings)
text = property(getText)
```'''

        assertEq(out_md, html2md.html2md(in_html, fenced_code='github'))

class PygmentsPreTest(unittest.TestCase):
    def atest_pygments(self):
        in_html = u'''
<pre class="code python literal-block">
<span class="kn">from</span> <span class="nn">BeautifulSoup</span> <span class="kn">import</span> <span class="n">BeautifulSoup</span>
<span class="kn">import</span> <span class="nn">urllib2</span>
<span class="n">soup</span> <span class="o">=</span> <span class="n">BeautifulSoup</span><span class="p">(</span><span class="n">urllib2</span><span class="o">.</span><span class="n">urlopen</span><span class="p">(</span><span class="s">'http://java.sun.com'</span><span class="p">)</span><span class="o">.</span><span class="n">read</span><span class="p">())</span>
<span class="n">menu</span> <span class="o">=</span> <span class="n">soup</span><span class="o">.</span><span class="n">findAll</span><span class="p">(</span><span class="s">'div'</span><span class="p">,</span><span class="n">attrs</span><span class="o">=</span><span class="p">{</span><span class="s">'class'</span><span class="p">:</span><span class="s">'pad'</span><span class="p">})</span>
<span class="k">for</span> <span class="n">subMenu</span> <span class="ow">in</span> <span class="n">menu</span><span class="p">:</span>
<span class="n">links</span> <span class="o">=</span> <span class="n">subMenu</span><span class="o">.</span><span class="n">findAll</span><span class="p">(</span><span class="s">'a'</span><span class="p">)</span>
<span class="k">for</span> <span class="n">link</span> <span class="ow">in</span> <span class="n">links</span><span class="p">:</span>
<span class="k">print</span> <span class="s">"</span><span class="si">%s</span><span class="s"> : </span><span class="si">%s</span><span class="s">"</span> <span class="o">%</span> <span class="p">(</span><span class="n">link</span><span class="o">.</span><span class="n">string</span><span class="p">,</span> <span class="n">link</span><span class="p">[</span><span class="s">'href'</span><span class="p">])</span>
</pre>'''
        out_md = u'''
    from BeautifulSoup import BeautifulSoup
    import urllib2
    soup = BeautifulSoup(urllib2.urlopen('http://java.sun.com').read())
    menu = soup.findAll('div',attrs={'class':'pad'})
    for subMenu in menu:
        links = subMenu.findAll('a')
        for link in links:
            print "%s : %s" % (link.string, link['href'])
'''
        assertEq(out_md, html2md.html2md(in_html))


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(PreTest)


if __name__ == '__main__':
    unittest.main()

