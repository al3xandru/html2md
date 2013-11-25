import unittest

from context import html2md
from assertions import assertEq


class ListsTest(unittest.TestCase):
    def test_deep_blockquote(self):
        in_html = u'''
<ul>
    <li>first</li>
    <li>second
        <ul>
            <li>1.1</li>
            <li>
                1.2
                <blockquote>
                    a blockquote on second level list item
                </blockquote>
                <blockquote>
                    <p>blockquote with p on second level list item</p>
                </blockquote>
                <pre>
def main(instream):
    text = instream.read()
    markup = html2md(text)
    return markup
                </pre>
                <p>a normal paragraph</p>
                <pre><code>
def main(instream):
    text = instream.read()
    markup = html2md(text)
    return markup
                </code></pre>
            </li>
            <li>1.3</li>
        </ul>
    </li>
    <li>last</li>
</ul>'''
        out_md = u"""
*   first
*   second

    *   1.1
    *   1.2

        > a blockquote on second level list item

        > blockquote with p on second level list item

            def main(instream):
                text = instream.read()
                markup = html2md(text)
                return markup

        a normal paragraph

            def main(instream):
                text = instream.read()
                markup = html2md(text)
                return markup

    *   1.3
*   last"""
        assertEq(out_md, html2md.html2md(in_html))


class BlockquoteTest(unittest.TestCase):
    def test_multilevel_blockquotes(self):
        in_html = u'''
<blockquote>
    <p>First level</p>
    <blockquote>
        <p>Second level</p>
        <blockquote>
            <p>Third level</p>
            <p>3rd level again</p>
        </blockquote>
        <p>Back on 2nd level</p>
    </blockquote>
    <p>Back on 1st level</p>
</blockquote>'''
        out_md = u'''> First.level

> > Second.level

> > > Third.level

> > > 3rd.level.again

> > Back.on.2nd.level

> Back.on.1st.level'''
        assertEq(out_md, html2md.html2md(in_html, strip=True))

    def test_twolevel_list(self):
        in_html = u'''
<blockquote>
    <p>First level</p>
    <blockquote>
        <p>Second level</p>
        <ul>
            <li>first</li>
            <li>second</li>
            <li>third</li>
        </ul>
    </blockquote>
</blockquote>'''
        out_md = u'''> First.level

> > Second.level

> > *   first
> > *   second
> > *   third'''
        assertEq(out_md, html2md.html2md(in_html, strip=True))


    def test_deep_pre(self):
        in_html = u'''
<blockquote>
    <blockquote>
        <pre>
def main(instream):
    text = instream.read()
    markup = html2md(text)
    return markup
        </pre>
        <p>a normal paragraph</p>
        <pre><code>
def main(instream):
    text = instream.read()
    markup = html2md(text)
    return markup
        </code></pre>
    </blockquote>
</blockquote>'''
        out_md = u'''> >     def main(instream):
> >         text = instream.read()
> >         markup = html2md(text)
> >         return markup

> > a normal paragraph

> >     def main(instream):
> >         text = instream.read()
> >         markup = html2md(text)
> >         return markup
'''.rstrip()
        assertEq(out_md, html2md.html2md(in_html), show_punctuation=False)


class PreTest(unittest.TestCase):
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
    return unittest.TestSuite([unittest.TestLoader().loadTestsFromTestCase(ListsTest),
                               unittest.TestLoader().loadTestsFromTestCase(BlockquoteTest),
                               unittest.TestLoader().loadTestsFromTestCase(PreTest)])


if __name__ == '__main__':
    unittest.main()