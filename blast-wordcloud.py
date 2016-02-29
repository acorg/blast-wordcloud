#!/usr/bin/env python

from __future__ import print_function

import argparse

import pytagcloud
from pytagcloud import create_tag_image, make_tags
from pytagcloud.lang.counter import get_tag_counts

from Bio.Blast import NCBIXML

parser = argparse.ArgumentParser(
    description='Make a wordcloud from BLAST XML output')

parser.add_argument('--out', required=True, help='The name of the output file')

parser.add_argument('--in', required=True, help='The BLAST XML input file.')

parser.add_argument(
    '--ncbiTitles', default=False, action='store_true',
    help=('If True, subject titles are assumed to come from an NCBI '
          'database and will have the first space-delimited field '
          'and anything after a comma ignored. This useful for cleaning '
          'up titles like '
          'gi|361057412|gb|CP003178.1| Niastella koreensis, complete genome'))

args = parser.parse_args()

titles = []

with open(args.xml) as fp:
    for record in NCBIXML.parse(fp):
        for description in record.descriptions:
            title = description.title
            if args.ncbiTitles:
                title = title[title.index(' '):title.index(',')]
            titles.append(title)


pytagcloud.lang = 'english'

tags = make_tags(get_tag_counts(' '.join(titles)), maxsize=80)
create_tag_image(tags, args.out, size=(900, 600))
