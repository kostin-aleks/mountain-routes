#!/usr/bin/env python
"""
NAME
     test_regex.py

DESCRIPTION
     Test RegEx solution to validate tags in the text
"""

import re
from lxml import etree

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """ Command """
    help = 'Test RegEx solution to validate tags in the text'

    def handle(self, *args, **options):
        ALLOWED = ['a', 'i', 'strong', 'code']

        samples = [
            {
                'idx': 1,
                'txt': """
                  <ul>
                    <li>
                      <a href="/ukrainian/news/1684305407-v-vozdushnyh-silah-v-patriot.html">

                        <span class="meta meta-border d-block">
                            <span class="d-flex mb-2">
                                <span class="time-gray fz-12">09:36</span>
                                <span class="time-gray fz-12 ml-2">Общие новости</span>
                            </span>
                            <span class="fz-14 text-white title">
                                В Воздушных силах Украины и Белом доме
                                прокомментировали заявление РФ
                                о попадании в Patriot
                            </span>
                      </a>
                      </li>
                      <li>
                        <a href="/ukrainian/high/1684302820-shahab.html">

                          <span class="meta meta-border d-block">
                                <span class="d-flex mb-2">
                                    <span class="time-gray fz-12">09:20</span>
                                    <span class="time-gray fz-12 ml-2">Премьер-лига</span>
                                </span>
                                <span class="fz-14 text-white title">
                                    Шахаб высказался о возможном возвращении в Зарю
                                </span>
                          </span>
                        </a>
                      </li>
                    </ul>
                    """
            },
            {
                'idx': 2,
                'txt': """
                Please note that our alternative forum:
                <a href="https://projecteuler.chat">https://projecteuler.chat</a>
                runs on a different platform and will remain accessible during the whole time.
                We will use the forum if we need to communicate any issues of which we become aware.
                """
            },
            {
                'idx': 3,
                'txt': """
                A few changes have been made to the website.
                The most notable change will be the artwork
                for the Levels.
                As the problem set continued to grow, the number of unused images in reserve
                was beginning to become depleted. Consequently, they have been replaced
                with a more colourful,
                interesting, and sustainable set of images that should last us
                many problems into the future.
                """
            },
        ]

        for sample in samples:
            print(f"\nsample {sample['idx']}")
            txt = sample['txt']
            result = re.search(r"<[^>]*>", txt)
            if result:
                print('text contains tags')
                items = re.findall(r"<[^>]*>", txt)
                for item in items:
                    tag = re.search(r"<[\s,\/]*([a-z,A-Z]+)\s*[^>]*>", item)
                    tag_name = tag.groups()[0]
                    # print(tag_name)
                    if tag_name not in ALLOWED:
                        print('text contains some forbidden tags')
                        break
                print("all tags in the text are allowed")
                parser = etree.XMLParser()
                try:
                    _ = etree.XML(txt, parser)
                except etree.XMLSyntaxError:
                    print(f'there are {len(parser.error_log)} syntax errors in the text as html')
                    for error in parser.error_log:
                        print(
                            f'error {error.message} at line {error.line} and column {error.column}')
            else:
                print("text doesn't contain any tag")

        return 'Done'
