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
        assertEq(out_md, html2md.html2md(in_html))

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
        assertEq(out_md, html2md.html2md(in_html))


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




def suite():
    return unittest.TestSuite([unittest.TestLoader().loadTestsFromTestCase(ListsTest),
                               unittest.TestLoader().loadTestsFromTestCase(BlockquoteTest)])


if __name__ == '__main__':
    unittest.main()