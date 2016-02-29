This is a Python program to display word clouds based on the titles that
are matched by [BLAST](https://en.wikipedia.org/wiki/BLAST).

![example.png](example.png)

## Usage

First, run `blast` and use `-outfmt 5` on the command line to get XML
output. Let's suppose that's in a file called `blast-output.xml`. Then:

```sh
$ blast-wordcloud.py --xml blast-output.xml --out word-cloud.png
```

In this example, your word cloud image will be saved to `word-cloud.png`.

If the BLAST database you're matching against was downloaded from NCBI,
you'll likely find the `--ncbiTitles` option useful. That will transform an
NCBI sequence title like "gi|361057412|gb|CP003178.1| Niastella koreensis,
complete genome" into "Niastella koreensis". It uses a simple heuristic -
only keep the text between the first space and the first comma in the
title, but it is quite effective.

## Installing under Linux and Mac OS X

You'll need Python installed, which should already be the case. You might
want to make a [virtualenv](https://pypi.python.org/pypi/virtualenv) for
the installation (otherwise you'll need to run the following using `sudo`,
which isn't recommended).

Then do `pip install -r requirements.txt`.

