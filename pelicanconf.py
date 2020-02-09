#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Tim Poulsen'
SITENAME = 'Tim Poulsen'
SITEURL = 'https://www.timpoulsen.com'
SITETITLE = 'Tim Poulsen'
SITESUBTITLE = 'Explorations of software and hardware'
SITEDESCRIPTION = "Tim Poulsen's blog of software, hardware, and life"
SITELOGO = '/images/tim_poulsen.jpg'

ARTICLE_URL = '{date:%Y}/{slug}.html'
ARTICLE_SAVE_AS = '{date:%Y}/{slug}.html'

STATIC_PATHS = ["static", 'images', 'extra/main.css', 'extra/custom.css']
PLUGIN_PATHS = ["plugins", "/Users/timpoulsen/repos/other/pelican-plugins"]
PLUGINS = ['pelicanfly', 'tag_cloud']

BROWSER_COLOR = '#143742'
ROBOTS = 'index, follow'

CC_LICENSE = {
    'name': 'Creative Commons Attribution-ShareAlike',
    'version': '4.0',
    'slug': 'by-sa'
}

COPYRIGHT_YEAR = 2020

EXTRA_PATH_METADATA = {
    'extra/main.css': {'path': 'theme/css/main.css'},
    'extra/custom.css': {'path': 'theme/css/custom.css'},
}
CUSTOM_CSS = 'theme/css/main.css'

MAIN_MENU = True


THEME = 'themes/Flex'
PATH = 'content'

TIMEZONE = 'America/New_York'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_DOMAIN = SITEURL
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Topics', '/categories.html'),
       ('Skypanther Studios', 'http://skypanther.com'),
       )

# Social widget
SOCIAL = (('twitter', 'https://twitter.com/skypanther'),
          ('github', 'https://github.com/skypanther'),
          ('linkedin', 'https://www.linkedin.com/in/timpoulsen'),
          ('keybase', 'https://keybase.io/skypanther'),
          ('rss', 'feeds/all.atom.xml'),
        )

MENUITEMS = (('Topics', '/categories.html'),
             ('About', '/pages/about.html'),
             ('Tags', '/tags.html'),
             )

DEFAULT_PAGINATION = False

TAG_CLOUD_SORTING = 'size'
TAG_CLOUD_BADGE = False

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

LOAD_CONTENT_CACHE = False
