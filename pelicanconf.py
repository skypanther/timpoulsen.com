#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = "Tim Poulsen"
SITENAME = "Tim Poulsen"
SITEURL = "https://www.timpoulsen.com"
SITETITLE = "Tim Poulsen"
SITESUBTITLE = "Me geeking out about random things"
SITEDESCRIPTION = "Tim Poulsen's blog of software, hardware, and life"
SITELOGO = "/images/tim_poulsen.jpg"

ARTICLE_URL = "{date:%Y}/{slug}.html"
ARTICLE_SAVE_AS = "{date:%Y}/{slug}.html"

STATIC_PATHS = ["static", "images", "extra/main.css", "extra/custom.css"]
PLUGIN_PATHS = [
    "plugins",
    "plugins/pelicanfly",
    "/Users/timpoulsen/repos/other/pelican-plugins",
]
PLUGINS = ["seo", "tag_cloud"]

BROWSER_COLOR = "#143742"
ROBOTS = "index, follow"

CC_LICENSE = {
    "name": "Creative Commons Attribution-ShareAlike",
    "version": "4.0",
    "slug": "by-sa",
}

COPYRIGHT_YEAR = 2023

EXTRA_PATH_METADATA = {
    "extra/main.css": {"path": "theme/css/main.css"},
    "extra/custom.css": {"path": "theme/css/custom.css"},
}
CUSTOM_CSS = "theme/css/main.css"

MAIN_MENU = True


THEME = "themes/Flex"
PATH = "content"

TIMEZONE = "America/New_York"

DEFAULT_LANG = "en"

# Feed generation is usually not desired when developing
FEED_DOMAIN = SITEURL
FEED_ALL_ATOM = "feeds/all.atom.xml"
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (("Topics", "/categories.html"),)

# Social widget
SOCIAL = (
    ("fa-brands", "mastodon", "https://fosstodon.org/@skypanther", "Mastodon"),
    ("fa-brands", "github", "https://github.com/skypanther", "GitHub"),
    ("fa-brands", "linkedin", "https://www.linkedin.com/in/timpoulsen", "LinkedIn"),
    ("fa-brands", "keybase", "https://keybase.io/skypanther", "Keybase"),
    ("fa-solid", "square-rss", "feeds/all.atom.xml", "RSS Feed"),
)

MENUITEMS = (
    ("Topics", "/categories.html"),
    ("About", "/pages/about.html"),
    ("Tags", "/tags.html"),
)

DEFAULT_PAGINATION = 10
# PAGINATION_PATTERNS = (
#     (1, "{url}", "{save_as}"),
#     (2, "{base_name}/page/{number}/", "{base_name}/page/{number}/index.html"),
# )

TAG_CLOUD_SORTING = "size"
TAG_CLOUD_BADGE = False

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

LOAD_CONTENT_CACHE = False

SEO_REPORT = True  # SEO report is enabled by default
SEO_ENHANCER = True  # SEO enhancer is disabled by default
SEO_ENHANCER_OPEN_GRAPH = True  # Subfeature of SEO enhancer
