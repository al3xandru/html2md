#!/usr/bin/env python
"""
html2markdown transforms the input HTML into Markdown.

Options:

-i: use instapaper mobilized for cleaning up the body
-e=encoding:  for passing in an encoding
"""

import logging
import os
import re
import sys
import urllib

try:
  import htmlentitydefs
  from HTMLParser import HTMLParseError
except ImportError: #Python3
  import html.entities as htmlentitydefs
  from html.parser import HTMLParseError


from BeautifulSoup import ICantBelieveItsBeautifulSoup
from h2m.html2text import HTML2Text, wrapwrite

from httpyz import human_headers, http, unicodebaby

_FILTERED_EXTENSIONS = ('.pdf', '.ps',
  '.tar.gz', '.zip',
  '.jpg', '.jpeg', '.png', '.gif', '.bmp'
)
_REPLACEABLE_CHARS = (8211, 8212, 8216, 8217, 8220, 8221, 8230, 8592, 8594, )

def process(input_opts, **settings):
  output = {
    'text'  : u'',
    'title' : os.path.basename(input_opts['uri']),
    'uri'   : input_opts['uri'],
  }

  _preprocess(input_opts)
  output.update(meta(input_opts))

  h = _init_html2text(input_opts.get('baseurl'), **settings)

  try:
    output['text'] = h.handle(input_opts['data'])
  except HTMLParseError, htmlErr:
    logging.exception("HTMLParseError (%s): line: %s, offset: %s from\n%s",
      htmlErr.msg, htmlErr.lineno, htmlErr.offset, input_opts['data']
    )
    logging.debug('Pass input through ICantBelieveItsBeautifulSoup')
    soup = ICantBelieveItsBeautifulSoup(input_opts['data'])
    h = _init_html2text(input_opts.get('baseurl'), **settings)
    try:
      if soup.body:
        output['text'] = h.handle(unicode(soup.body))
      else:
        output['text'] = h.handle(unicode(soup))
    except HTMLParseError, htmlErr:
      logging.error('HTMLParseError (%s) with ICantBelieveItsBeautifulSoup: line: %s, offset: %s',
        htmlErr.msg, htmlErr.lineno, htmlErr.offset
      )

  return output


def _preprocess(input_opts):
  if not input_opts.has_key('is_text'):
    input_opts['is_text'] = _maybe_text(input_opts['uri'])

  text = input_opts['data']
  if not text or not input_opts['is_text']:
    return
  for repl in _REPLACEABLE_CHARS:
    text = text.replace(unichr(repl), "&#%s;" % repl)

  input_opts['data'] = text

def meta(input_opts):
  output = {}

  if input_opts['is_text']:
    try:
      soup = ICantBelieveItsBeautifulSoup(input_opts['data'])
      el_title = soup.findAll('title')
      if el_title:
        title = el_title[0].getText()
        if title:
          title = title.replace('\n', ' ')
          title = title.strip()
          title = re.sub('\s+', ' ', title)
          output['title'] = title

      if input_opts['use_instapaper']:
        input_opts['data'] = _clean_html(input_opts['data'], soup)
    except Exception:
      pass

  return output

def _init_html2text(baseurl, **settings):
  h = HTML2Text(baseurl=baseurl)

  # settings
  for k,v in settings.items():
    setattr(h, k, v)

  return h

def _clean_html(data, soup):
  story_div = soup.find('div', attrs={'id': 'story'}) or soup.find('body')
  if story_div:
    _fix_links(story_div)
    return unicode(story_div)
  else:
    return data

def _fix_links(soup):
  links = soup.findAll('a', attrs={'href': True})
  for link in links:
    href = link['href']
    if href.startswith('#') or href.startswith('/'):
      continue
    for _iprefix in ('http://www.instapaper.com/m?u=',
                     'http://instapaper.com/m?u=',
                     'https://www.instapaper.com/m?u=',
                     'https://instapaper.com/m?u='):
      if href.startswith(_iprefix):
        link['href'] = urllib.unquote(href[len(_iprefix):])
        continue

def _maybe_text(name):
  """ Tests if the input format is possibly HTML by looking at the extension. """
  lname = name.lower()
  for ext in _FILTERED_EXTENSIONS:
    if lname.endswith(ext):
      return False
  return True


if __name__ == "__main__":
  input_opts = {
    'encoding'        : 'utf-8',
    'use_instapaper'  : False,
    'uri'             : sys.argv[-1],
    'baseurl'         : '',
    'is_url'          : False,
    'is_text'         : False,
    'data'            : u''
  }

  if len(sys.argv) > 0:
    for opt in sys.argv[1:-1]:
      if '-i' == opt:
        input_opts['use_instapaper'] = True
      elif opt.startswith('-e='):
        input_opts['encoding'] = opt.split('=')[1]

    if input_opts['uri'].startswith('http://') or input_opts['uri'].startswith('https://'):
      input_opts['baseurl'] = input_opts['uri']
      input_opts['is_url'] = True

      if _maybe_text(input_opts['uri']):
        input_opts['is_text'] = True
        if input_opts['use_instapaper']:
          response = http.get('http://www.instapaper.com/m', params=dict(u=input_opts['uri']), headers=human_headers())
        else:
          response = http.get(input_opts['uri'], headers=human_headers())
          input_opts['baseurl'] = response.url

        input_opts['data'] = response.data
        if isinstance(input_opts['data'], unicode):
          print "unicode"
        else:
          print "str"
        if input_opts.get('encoding') is None:
          input_opts['encoding'] = response.encoding
      else:
        input_opts['baseurl'] = input_opts['uri']
        input_opts['data'] = u''
    else:
      input_opts['baseurl'] = ""
      if _maybe_text(input_opts['uri']):
        input_opts['is_text'] = True
        data = open(input_opts['uri'], 'rb').read()

        if input_opts.get('encoding') is None:
          input_opts['data'], input_opts['encoding'] = unicodebaby.to_unicode(data)
        else:
          input_opts['data'] = data.decode(input_opts['encoding'])
  else:
    input_opts['is_text'] = True
    input_opts['data'] = sys.stdin.read()
    if input_opts.get('encoding') is None:
      input_opts['data'], input_opts['encoding'] = unicodebaby.to_unicode(input_opts['data'])
    else:
      input_opts['data'] = input_opts['data'].decode(input_opts['encoding'])

  output = process(input_opts, body_width=0, inline_links=True, ignore_images=False, ignore_emphasis=False)

  wrapwrite(output['title'])
  wrapwrite(os.linesep)
  wrapwrite(output['uri'])
  wrapwrite(os.linesep)
  wrapwrite(os.linesep)
  wrapwrite(output['text'])
