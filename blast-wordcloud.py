#!/usr/bin/env python

"""
A python program to make a word cloud from BLAST XML output. Run

    $ blast-wordcloud.py --help

to see usage & options, or read on.
"""

import argparse
from collections import defaultdict
from wordcloud import WordCloud

from Bio.Blast import NCBIXML


parser = argparse.ArgumentParser(
    description='Make a word cloud from BLAST XML output')

parser.add_argument('--out', required=True, help='The name of the output file')

parser.add_argument('--xml', required=True, help='The BLAST XML input file.')

parser.add_argument(
    '--ncbiTitles', default=False, action='store_true',
    help=('If True, subject titles are assumed to come from an NCBI '
          'database and will have the first space-delimited field '
          'and anything after a comma ignored. This useful for cleaning '
          'up titles like '
          'gi|361057412|gb|CP003178.1| Niastella koreensis, complete genome'))

args = parser.parse_args()

titles = defaultdict(int)

with open(args.xml) as fp:
    for record in NCBIXML.parse(fp):
        for description in record.descriptions:
            title = description.title
            if args.ncbiTitles:
                title = title[title.index(' '):title.find(',')]
            for word in title.lower().split():
                titles[word] += 1

wordCloud = WordCloud(width=900, height=600).generate_from_frequencies(
    titles.items())
wordCloud.to_file(args.out)
