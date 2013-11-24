from h2m.html2md import html2md

__author__ = 'alex'

import unittest

from h2m.html2md.assertions import assertEq

class BasicTest(unittest.TestCase):
  def test_a(self):
    in_html = '''<a href="http://yahoo.com">yahoo</a>'''
    out_md = '''[yahoo](http://yahoo.com)'''
    assertEq(out_md, html2md.html2md(in_html))

  def test_a_title(self):
    in_html = '''<a href="http://yahoo.com" title="some title">yahoo</a>'''
    out_md = '''[yahoo](http://yahoo.com "some title")'''
    assertEq(out_md, html2md.html2md(in_html))

  def test_a_attributes(self):
    in_html = '''<a href="http://yahoo.com" id="aid" class="cls1 cls2" rel="nofollow external">yahoo</a>'''
    out_md = '''[yahoo](http://yahoo.com "{{#aid cls1 cls2 rel='nofollow external'}}")'''
    assertEq(out_md, html2md.html2md(in_html))

  def test_a_all(self):
    in_html = '''<a href="http://yahoo.com"  title="some title" id="aid" class="cls1 cls2" rel="nofollow external">yahoo</a>'''
    out_md = '''[yahoo](http://yahoo.com "some title {{#aid cls1 cls2 rel='nofollow external'}}")'''
    assertEq(out_md, html2md.html2md(in_html))

  def test_a_name(self):
    in_html = '''<a name="anchor"></a>'''
    out_md = '''<a name="anchor"></a>'''
    assertEq(out_md, html2md.html2md(in_html))

  def test_strong(self):
    in_html = '''<strong>something with a <a href="http://yahoo.com">yahoo</a> link </strong>'''
    out_md = '''**something with a [yahoo](http://yahoo.com) link **'''
    assertEq(out_md, html2md.html2md(in_html))

  def test_emphasize(self):
    in_html = '''<em>something with a <a href="http://yahoo.com">yahoo</a></em>'''
    out_md = '''*something with a [yahoo](http://yahoo.com)*'''
    assertEq(out_md, html2md.html2md(in_html))

  def test_code(self):
    in_html = '''<code>class Object{}</code>'''
    out_md = '''`class Object{}`'''
    assertEq(out_md, html2md.html2md(in_html))

  def test_h2_simple(self):
    in_html = '''<h2>Very simple H2</h2>'''
    out_md = '''## Very simple H2'''
    assertEq(out_md, html2md.html2md(in_html))

  def test_h2_with_link(self):
    in_html = '''<h2 id="h2_id">Very simple H2 with <a href="http://yahoo.com" id="link_id">link</a> to</h2>'''
    out_md = '''## Very simple H2 with [link](http://yahoo.com "{{#link_id}}") to [..]("{{h2:#h2_id}}")'''
    assertEq(out_md, html2md.html2md(in_html))

  def test_img_attributes(self):
    in_html = '''<p><img alt="a picture" src="http://lh4.ggpht.com/_apBFwLItpPg/TYALk3vgpPI/AAAAAAAAAbU/hgZn27Cqdas/IBM%20The%204%20levels%20of%20server%20and%20storage%20system%20integration.jpg" width="468" height="351"></p>'''
    out_md = '''![a picture](http://lh4.ggpht.com/_apBFwLItpPg/TYALk3vgpPI/AAAAAAAAAbU/hgZn27Cqdas/IBM%20The%204%20levels%20of%20server%20and%20storage%20system%20integration.jpg "{{width=468 height=351}}")'''
    assertEq(out_md, html2md.html2md(in_html))


