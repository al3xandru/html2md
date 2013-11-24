# -*- coding: utf8 -*-
import re
import os
import sys

from h2m.html2md.BeautifulSoup import ICantBelieveItsBeautifulSoup
from h2m.html2md.BeautifulSoup import Tag, NavigableString

__author__ = 'alex'


def html2md(text):
  proc = Processor(text)
  return proc.get_output()


class Processor(object):
  def __init__(self, html):
    self.html = html
    self.soup = ICantBelieveItsBeautifulSoup(html)
    self._text_buffer = []
    self._attributes_stack = []
    self._indentation_stack = []
    self._inside_footnote = False
    self._list_level = 0
    self._list_item_has_block = False
    self._output = u''
    self._footnote_ref = 0
    self._process(self.soup)
    if self._text_buffer:
      self._flush_buffer()

  def get_output(self):
    return self._output.rstrip(u'\n\r')
  
  def _process(self, element):
    for t in element.contents:
      self._proc(t)

  def _proc(self, t):
    if isinstance(t, NavigableString):
      if not self._is_empty(t):
        self._text_buffer.append(t.strip('\r\n'))
      return
    if isinstance(t, Tag):
      self._process_tag(t)

  def _process_tag(self, tag):
    if tag.name == 'a':
      if tag.has_key('href'):
        self._text_buffer.append(u'[')
        self._process(tag)
        self._text_buffer.append(u']')
        self._text_buffer.append(u'(')
        self._text_buffer.append(tag['href'])
        attrs = dict(tag.attrs) if tag.attrs else {}
        self.removeAttrs(attrs, 'href', 'title')
        attrs_str = self.simpleAttrs(attrs)
        if attrs_str or tag.has_key('title'):
          self._text_buffer.append(u' "')
          if tag.has_key('title'):
            self._text_buffer.append(tag['title'])
            if attrs_str:
              self._text_buffer.append(u' ')
          if attrs_str:
            self._text_buffer.append(attrs_str)
          self._text_buffer.append(u'"')
        self._text_buffer.append(u')')
      else:
        self._text_buffer.append(unicode(tag))
      return
    if tag.name in ('b', 'strong'):
      self._text_buffer.append(u"**")
      self._process(tag)
      self._text_buffer.append(u"**")
      return
    if tag.name == 'blockquote':
      self._push_attributes(tag=tag)
      self._indentation_stack.append('bq')
      self._process(tag)
      self._write_block(sep=u'\n' * 2)
      self._indentation_stack.pop()
      return
    if tag.name == 'br':
      self._text_buffer.append(u"  " + os.linesep)
      return
    if tag.name == 'center':
      self._push_attributes(tagname='p', attrs={'style': 'text-align:center;'})
      self._process(tag)
      self._write_block(sep=os.linesep * 2)
      return
    if tag.name == 'code':
      self._text_buffer.append(u"`")
      self._text_buffer.append(tag.getText())
      self._text_buffer.append(u"`")
      return
    if tag.name == 'dl':
      return
    if tag.name == 'dt':
      self._process(tag)
      self._write_block(sep=u'\n')
      return
    if tag.name == 'dd':
      self._text_buffer.append(u':')
      self._text_buffer.append(u' ' * 4)
      self._process(tag)
      self._write_block(sep=u'\n' * 2)
      return
    if tag.name == 'del':
      self._text_buffer.append(u"~~")
      self._process(tag)
      self._text_buffer.append(u"~~")
      return
    if tag.name == 'div':
      div_class = tag.get('class')
      if div_class:
        if div_class.find('footnote') > -1:
          self._inside_footnote = True
          self._flush_buffer()
          self._process_footnotes(tag)
          self._inside_footnote = False
          return
      self._write(unicode(tag), sep=os.linesep * 2)
      return
    if tag.name in ('em', 'i'):
      self._text_buffer.append(u"*")
      self._process(tag)
      self._text_buffer.append(u"*")
      return
    if tag.name in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
      self._push_attributes(tag=tag)
      self._text_buffer.append(u'#' * int(tag.name[1]) + ' ')
      self._process(tag)
      self._write_block(sep=os.linesep * 2)
      self._text_buffer = []
      return
    if tag.name == 'hr':
      if not self._inside_footnote:
        self._write(u'-----', sep=u'\n'*2)
      return
    if tag.name == 'img':
      self._text_buffer.append(u'![')
      self._text_buffer.append(tag.get('alt') or tag.get('title') or '')
      self._text_buffer.append(u']')
      self._text_buffer.append(u'(')
      self._text_buffer.append(tag['src'])
      attrs = dict(tag.attrs) if tag.attrs else {}
      self.removeAttrs(attrs, 'src', 'title', 'alt')
      attrs_str = self.simpleAttrs(attrs)
      if attrs_str or tag.has_key('title'):
        self._text_buffer.append(u' "')
        if tag.has_key('title'):
          self._text_buffer.append(tag['title'])
          if attrs_str:
            self._text_buffer.append(u' ')
        if attrs_str:
          self._text_buffer.append(attrs_str)
        self._text_buffer.append(u'"')
      self._text_buffer.append(u')')
      return
    if tag.name == 'li':
      list_item_has_block = False
      last_block_name = None
      blocks_counter = 0
      self._push_attributes(tag=tag)
      if tag.string:
        self._proc(tag.string)
        self._write_block(sep=u'\n')
      else:
        elements = []
        for c in tag.contents:
          if isinstance(c, NavigableString) and not self._is_empty(c):
            elements.append(c)
          elif isinstance(c, Tag):
            elements.append(c)
#        if len(elements) == 1:
#          elem = elements[0]
#          if isinstance(elem, NavigableString):
#            self._proc(elements[0])
#            self._write_block(sep=u'\n')
#          else:
#            if elem.name == 'p':
#              self._write('\n')
#            self._proc(elem)
#        else:
        for c in elements:
          if isinstance(c, Tag) and c.name in ('blockquote', 'ol', 'p', 'pre', 'ul', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            blocks_counter += 1
            list_item_has_block = True
            last_block_name = c.name
            self._write_block(sep=u'\n')
          self._proc(c)
      if list_item_has_block:
        trim_newlines = False
#        if last_block_name == 'p' and blocks_counter < 3:
#          trim_newlines = True
        if last_block_name in ('ul', 'ol') and blocks_counter < 2:
          trim_newlines = True
        if trim_newlines and self._output[-2:] == '\n\n':
          self._output = self._output[:-1]
      if self._indentation_stack[-1] in ('cul', 'col'):
        self._indentation_stack[-1] = self._indentation_stack[-1][1:]
      return
    if tag.name == 'ol':
      self._list_level += 1
      self._push_attributes(tag=tag)
      self._indentation_stack.append('ol')
      self._process(tag)
      self._indentation_stack.pop()
      self._list_level -= 1
      self._write('', sep=os.linesep)
      if self._list_level == 0:
        self._write('', sep=os.linesep)
      return
    if tag.name == 'p':
      # must finish it by 2 * os.linesep
      self._push_attributes(tag=tag)
      self._process(tag)
      self._write_block(sep=os.linesep * 2)
      return
    if tag.name == 'pre':
      self._push_attributes(tag=tag)
      self._indentation_stack.append('pre')
      self._text_buffer.append(tag.getText())
      self._write_block(sep=u'\n')
      self._indentation_stack.pop()
      return
    if tag.name == 'sup':
      sup_txt = tag.getText()
      if _FOOTNOTE_REF_re.match(sup_txt):
        self._footnote_ref += 1
        self._text_buffer.append(u'[^%s]' % self._footnote_ref)
      else:
        self._write(unicode(tag))
      return
    if tag.name == 'tt':
      self._text_buffer.append(u"`")
      self._text_buffer.append(tag.getText())
      self._text_buffer.append(u"`")
      return
    if tag.name == 'ul':
      self._push_attributes(tag=tag)
      self._list_level += 1
      self._indentation_stack.append('ul')
      self._process(tag)
      self._indentation_stack.pop()
      self._list_level -= 1
      self._write('', sep=os.linesep)
      if self._list_level == 0:
        self._write('', sep=os.linesep)
      return

    self._write(unicode(tag), sep=os.linesep * 2)

  def _write_block(self, sep=''):
    if not self._attributes_stack and not self._text_buffer:
      return
    indentation = u''
    extra_indentation = u''
    for idx in range(len(self._indentation_stack)):
      indent_type = self._indentation_stack[idx]
      if indent_type == 'bq':
        indentation += u'> '
        extra_indentation += u'> '
      elif indent_type == 'pre':
        indentation += u' ' * 4
        extra_indentation += u' ' * 4
      elif indent_type == 'ol':
        indentation += u'1.  '
        extra_indentation += u' ' * 4
        self._indentation_stack[idx] = 'col'
      elif indent_type == 'ul':
        indentation += u'*   '
        extra_indentation += (u' ' * 4)
        self._indentation_stack[idx] = 'cul'
      elif indent_type == 'cul':
        indentation = extra_indentation = (u' ' * 4)
      elif indent_type == 'col':
        indentation = extra_indentation = (u' ' * 4)


    attributes = []
    for tagname, attrs in self._attributes_stack:
      attributes.append(self.elemAttrs(tagname, attrs, '..'))
    self._attributes_stack = []

    txt = indentation
    txt += ''.join(self._text_buffer)
    txt = txt.replace(u'\r\n', u'\n')
    if sep and txt.endswith('\n'):
      txt = txt.rstrip('\n')
    txt = txt.replace(u'\n', u'\n' + extra_indentation)
    if attributes:
      txt += u' ' + u' '.join(attributes)
    self._write(txt, sep)
    self._text_buffer = []
    
  def _write(self, value, sep=''):
    if value and value[0] == '\n' and self._output and self._output[-1] == '\n':
      value = value[1:]
    self._output += _entity2ascii(value) + sep

  def simpleAttrs(self, attrs):
    if not attrs:
      return u""

    attr_arr = []
    lattrs = attrs.copy()
    if lattrs.has_key('id'):
      attr_arr.append("#%s" % lattrs['id'])
      del lattrs['id']
    if lattrs.has_key('class'):
      [attr_arr.append(sv) for sv in lattrs['class'].split()]
      del lattrs['class']

    for k,v in lattrs.items():
      use_sep = False
      for c in (' ', ':', '-', ';'):
        if v.find(c) > -1:
          use_sep = True
          break
      if use_sep:
        attr_arr.append("%s='%s'" % (k,v))
      else:
        attr_arr.append("%s=%s" % (k,v))
    return u"{{%s}}" % " ".join(attr_arr)

  def elemAttrs(self, tag_name, attrs, sep):
    if not attrs:
      return u""
    attr_arr = []
    lattrs = attrs.copy()
    if lattrs.has_key('id'):
      attr_arr.append("#%s" % lattrs['id'])
      del lattrs['id']
    if lattrs.has_key('class'):
      [attr_arr.append(sv) for sv in lattrs['class'].split()]
      del lattrs['class']
    for k,v in lattrs.items():
      use_sep = False
      for c in (' ', ':', '-', ';'):
        if v.find(c) > -1:
          use_sep = True
          break
      if use_sep:
        attr_arr.append("%s='%s'" % (k,v))
      else:
        attr_arr.append("%s=%s" % (k,v))
    return u"[%s](\"{{%s:%s}}\")" % (sep, tag_name, " ".join(attr_arr))
  
  def removeAttrs(self, attrs, *keys):
    if not attrs:
      return
    for k in keys:
      try:
        del attrs[k]
      except KeyError:
        pass

  def _is_empty(self, value):
    if not value:
      return True
    svalue = value.strip(' \t\n\r')
    if not svalue:
      return True
    return False

  def _flush_buffer(self):
    if self._text_buffer:
      self._write(''.join(self._text_buffer))

  def _push_attributes(self, tag=None, tagname=None, attrs=None):
    attr_dict = None
    if tag:
      tagname = tag.name
      if tag.attrs:
        attr_dict = dict(tag.attrs)
      elif attrs:
        attr_dict = attrs
      else:
        attr_dict = {}
    if tagname and attrs:
      attr_dict = attrs
    if attr_dict:
      self._attributes_stack.append((tagname, attr_dict))

  def _process_footnotes(self, tag):
    self._write('', sep=os.linesep * 2)
    index = 0
    for li in tag.findAll('li'):
      buffer = []
      index += 1
      links = li.findAll('a')

      if links:
        links[-1].extract()

      buffer.append("[^%s]: " % index)

      children = []
      for c in li.contents:
        if isinstance(c, NavigableString):
          if not self._is_empty(c):
            children.append(c)
        elif isinstance(c, Tag):
          children.append(c)
      if len(children) == 1 and isinstance(children[0], Tag) and children[0].name == 'p':
        children = children[0].contents
      for c in children:
        if isinstance(c, NavigableString):
          buffer.append(c)
        elif isinstance(c, Tag):
          if c.name in ('a', 'b', 'strong', 'code', 'del', 'em', 'i', 'img', 'tt'):
            self._process_tag(c)
            buffer.extend(self._text_buffer)
            self._text_buffer = []
          else:
            buffer.append(unicode(c))

      footnote = u''.join(buffer).strip(' \n\r')
      if footnote.endswith('()'):
        footnote = footnote[:-2]
      self._write(footnote, sep=os.linesep)

_FOOTNOTE_REF_re = re.compile('\[?[a-zA-Z0-9]\]?')

def _entity2ascii(val):
  for ent, asc in _ENTITY_DICT.items():
    val = val.replace(ent, asc)
  return val

_ENTITY_DICT = {
  '&#8212;': '--',
  '&#8216;': "'",
  '&#8217;': "'",
  '&#8220;': '"',
  '&#8221;': '"',
  '&#8230;': '...',
  u'…'     : '...',
}

def main(instream):
  text = instream.read()
  markup = html2md(text)
  return markup

if __name__ == '__main__':
  input = sys.argv[1]
  if not os.path.exists(input):
    print "Input must be either a directory or a file"
    sys.exit(1)

  if os.path.isfile(input):
    result = main(open(input))
  else:
    result = main(sys.stdin)

  print result

