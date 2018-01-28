import re
import operator
import requests

from functools import reduce
from os.path import basename, splitext
from urllib.parse import urlsplit
from bs4 import BeautifulSoup
from newspaper import Article


def get_page_info(url):
    page = Article(url)
    page_og = OpenGraph()
    image_url = None
    global_type = None
    page_content = None

    def get_page_head():
        headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.2 '
                          '(KHTML, like Gecko) Chrome/15.0.874.121 Safari/535.2',
        }

        try:
            resp_headers = requests.head(url, headers=headers).headers
        except requests.exceptions.RequestException:
            raise LinkException('Failed to read link.')
        return resp_headers

    def get_title_from_url():
        name_url = splitext(basename(urlsplit(url).path))[0]
        words = re.findall(r'[a-zA-Z0-9]+', name_url)
        return ' '.join([word.capitalize() for word in words])

    def summary_from_text(txt, size=250):
        return txt[:size] if isinstance(txt, str) and len(txt) > size else txt

    def build_tags(*args):
        tags = reduce(operator.add, args)
        return list(filter(lambda x: bool(x), set(tags)))

    page_type, page_subtype = get_page_head()['Content-Type'].split('/')
    page_subtype = re.findall(r'[a-zA-Z0-9]+', page_subtype)[0]

    if page_type == 'image':
        image_url = url
        global_type = page_type

    if page_type == 'text':
        page.download()
        page_content = page.html

        if page_subtype == 'html':
            page_og = OpenGraph(html=page_content)
            page.parse()

    page_text = page.text or page_content

    return {
        'type': page_og.type or global_type or page_subtype,
        'title': page_og.title or page.title or get_title_from_url(),
        'summary': page_og.description or page.meta_description or summary_from_text(page_text),
        'image': page_og.image or page.meta_img or page.top_image or image_url,
        'tags': build_tags(page.meta_keywords, list(page.tags)),
        'publish_date': page.publish_date or None,
        'text': page_text,
    }


class OpenGraph:
    __data__ = {}

    def __init__(self, html=None):
        self.__data__ = {}
        if html:
            self._parse(html)

    def __contains__(self, item):
        return item in self.__data__

    def __getattr__(self, name):
        if name in self.__data__:
            return self.__data__[name]
        return None

    def _parse(self, html):
        doc = BeautifulSoup(html, 'lxml')
        ogs = doc.html.head.findAll(property=re.compile(r'^og'))

        for og in ogs:
            if og.has_attr('content'):
                self.__data__[og['property'][3:]] = og['content']


class LinkException(Exception):
    pass
