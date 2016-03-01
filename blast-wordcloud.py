#!/usr/bin/env python

"""
A python program to make a word cloud from BLAST XML output. Run

    $ blast-wordcloud.py --help

to see usage & options, or read on.
"""

import re
import argparse
from collections import defaultdict
from wordcloud import WordCloud, STOPWORDS

from Bio.Blast import NCBIXML

VIRUS_STOPWORDS = '''
clone complete genome genom integration site stealth partial predicted
shotgun sequence sequenc protein dna rna chromosome microsatellite
satellite linkage pseudogene group strain voucher
'''

parser = argparse.ArgumentParser(
    description='Make a word cloud from BLAST XML output')

parser.add_argument(
    '--out', required=True, help='The name of the output file')

parser.add_argument(
    '--xml', required=True, help='The BLAST XML input file.')

parser.add_argument(
    '--maxWords', type=int, default=200,
    help='The maximum number of words the image should display.')

parser.add_argument(
    '--width', type=int, default=900,
    help='The height (in pixels) of the image to produce.')

parser.add_argument(
    '--height', type=int, default=600,
    help='The width (in pixels) of the image to produce.')

parser.add_argument(
    '--ncbiTitles', default=False, action='store_true',
    help=('If True, subject titles are assumed to come from an NCBI '
          'database and will have the first space-delimited field '
          'and anything after a comma ignored. This useful for cleaning '
          'up titles like '
          'gi|361057412|gb|CP003178.1| Niastella koreensis, complete genome'))

parser.add_argument(
    '--stop', action='append', dest='stopwords',
    help=('Specify a stop word (which will not be included in the word '
          'cloud). This option may be repeated.'))

args = parser.parse_args()

stopwords = set(VIRUS_STOPWORDS.split())
stopwords.update(STOPWORDS)
if args.stopwords:
    stopwords.update(args.stopwords)

wordRegexp = re.compile(r"\w[\w']+")
digitRegexp = re.compile(r"^[0-9]+$")

counts = defaultdict(int)

with open(args.xml) as fp:
    for record in NCBIXML.parse(fp):
        for description in record.descriptions:
            title = description.title
            if args.ncbiTitles:
                title = title[title.index(' '):title.find(',')]
            for match in wordRegexp.finditer(title.lower()):
                word = match.group()
                if word not in stopwords and not digitRegexp.match(word):
                    counts[word] += 1

wordCloud = WordCloud(width=args.width, height=args.height,
                      max_words=args.maxWords)
image = wordCloud.generate_from_frequencies(counts.items())
wordCloud.to_file(args.out)
