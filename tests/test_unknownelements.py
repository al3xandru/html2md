import unittest

from context import html2md
from assertions import assertEq


UNPROCESSED_HTML_ELEMENTS = ('abbr', 'area', 'audio', 'aside'
                             'bdi', 'bdo', 'button',
                             'canvas', 'caption', 'cite', 'colgroup',
                             'data', 'datalist', 'del', 'details', 'dfn',
                             'embed',
                             'fieldset', 'figcaption', 'figure', 'form',
                             'iframe', 'ins',
                             'kbd', 'keygen',
                             'label', 'legend',
                             'map', 'mark', 'meter',
                             'noscript',
                             'object', 'optgroup', 'option', 'output',
                             'param', 'progress',
                             'q',
                             'rp', 'rt', 'ruby',
                             's', 'samp', 'script', 'select', 'shadow', 'small', 'style', 'sub',
                             'template', 'textarea', 'tfoot', 'th', 'thead', 'time', 'tr', 'track',
                             'var', 'video',
                             'wbr'
)
REMOVED_HTML_ELEMENTS = ('nav', 'menu', 'menuitem')

NON_STANDARD_ELEMENTS = (
    'acronym', 'applet', 'bgsound', 'big', 'blink', 'center', 'dir', 'font', 'frame', 'frameset',
    'hgroup', 'isindex', 'listing', 'marquee', 'nobr', 'noframes', 'plaintext', 'spacer', 'strike', 'tt',
    'xmp'
)


class UnprocessedElements(unittest.TestCase):
    def test_unprocessed(self):
        """Cureently failing: col, input, sup"""
        results = {}
        for tag in UNPROCESSED_HTML_ELEMENTS:
            in_html = u'''<p>A paragraph with an <{0}>inserted text</{0}> and existing text.</p>'''.format(tag)
            out_md = u'''A paragraph with an <{0}>inserted text</{0}> and existing text.'''.format(tag)
            try:
                assertEq(out_md, html2md.html2md(in_html))
            except AssertionError, aser:
                results[tag] = aser
        if results:
            print
            for k, v in results.iteritems():
                print "Failed tag: ", k, v
                print
            self.fail("%s tags failed (%s)" % (len(results), results.keys()))

    def test_removed(self):
        """Currently failing only due to spacing issues"""
        results = {}
        for tag in REMOVED_HTML_ELEMENTS:
            in_html = u'''<p>A paragraph with an <{0}>inserted text</{0}> and existing text.</p>'''.format(tag)
            out_md = u'''A paragraph with an  and existing text.'''.format(tag)
            try:
                assertEq(out_md, html2md.html2md(in_html))
            except AssertionError, aser:
                results[tag] = aser
        if results:
            print
            for k, v in results.iteritems():
                print "Failed tag: ", k, v
                print
            self.fail("%s tags failed (%s)" % (len(results), results.keys()))

class BlockElementsTest(unittest.TestCase):
    def test_iframe(self):
        in_html = u'''
<p>YouTube:</p>

<iframe width="420" height="315" src="//www.youtube.com/embed/rnujQquKCQY" frameborder="0" allowfullscreen="allowfullscreen"></iframe>

<p>Slideshare:</p>

<iframe src="http://www.slideshare.net/slideshow/embed_code/28512891" width="427" height="356" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC;border-width:1px 1px 0;margin-bottom:5px" allowfullscreen="allowfullscreen"> </iframe>
<div style="margin-bottom:5px"> <strong> <a href="https://www.slideshare.net/subagini/effective-presentation-skills-28512891" title="Effective presentation skills" target="_blank">Effective presentation skills</a> </strong> from <strong><a href="http://www.slideshare.net/subagini" target="_blank">Subagini Manivannan</a></strong> </div>
        '''
        out_md = u'''YouTube:

<iframe width="420" height="315" src="//www.youtube.com/embed/rnujQquKCQY" frameborder="0" allowfullscreen="allowfullscreen"></iframe>

Slideshare:

<iframe src="http://www.slideshare.net/slideshow/embed_code/28512891" width="427" height="356" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC;border-width:1px 1px 0;margin-bottom:5px" allowfullscreen="allowfullscreen"> </iframe>

**[Effective presentation skills](https://www.slideshare.net/subagini/effective-presentation-skills-28512891 "Effective presentation skills {{target=_blank}}")** from **[Subagini Manivannan](http://www.slideshare.net/subagini "{{target=_blank}}")**'''

        assertEq(out_md, html2md.html2md(in_html))


def suite():
    return unittest.TestSuite([unittest.TestLoader().loadTestsFromTestCase(UnprocessedElements),
                               unittest.TestLoader().loadTestsFromTestCase(BlockElementsTest)])


if  __name__ == '__main__':
    unittest.main()

