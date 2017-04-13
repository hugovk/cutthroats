#!/usr/bin/env python
# encoding: utf-8
"""
Find words matching a pattern in a Project Gutenberg text.

For example, to find hyphenated words with capped initials:

python word-finder.py "^[A-Z].*-.+" -pg 6049

TODO input from text file instead of PG?
"""
from __future__ import print_function
import argparse
import re
import webbrowser
# from pprint import pprint


def load_list(the_filename):
    try:
        with open(the_filename, 'r') as f:
            my_list = [
                line.decode('unicode-escape').rstrip(u'\n') for line in f]
    except IOError:
        my_list = []
    return my_list


def cut_verbs(cutthroats):
    """Given a list of cutthroats, find the verb- stems.
    Ignores unhyphenated.
    """
    verbs = set()
    for cutthroat in cutthroats:
        if "-" in cutthroat:
            first_word = cutthroat.split()[0].split(",")[0]
            if "-" in first_word:
                verb = first_word.split("-")[0]
                verbs.add(verb.lower())
                # print(verb, "\t", first_word, "\t", cutthroat)
    return verbs


def text_from_pg(id_number):
    # https://github.com/c-w/Gutenberg
    from gutenberg.acquire import load_etext
    # from gutenberg.cleanup import strip_headers

    # text = strip_headers(load_etext(id_number)).strip()
    text = load_etext(id_number).strip()
    return text


def words_from_text(text):
    """Split the text into a set of words"""
    # https://textblob.readthedocs.org/en/dev/
    print("Split text into words")
    from textblob import TextBlob
    blob = TextBlob(text)
#     return set(word.lower() for word in blob.words)
    return set(blob.words)


def open_url(url):
    if not args.no_web:
        webbrowser.open(url, new=2)  # 2 = open in a new tab, if possible


def print_it(text):
    """cmd.exe cannot do Unicode so encode first"""
    print(text.encode('utf-8'))


def commafy(value):
    """Add thousands commas"""
    return "{:,}".format(value)


def summarise(some_set, text):
    if len(some_set):
        print("\nFound", len(some_set), text + ":\n")
        some_set = sorted(some_set)
        print_it("\n".join(some_set))
    else:
        print("\nFound no " + text + ".\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Find words matching a pattern in Project Gutenberg.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        'pattern',
        help="Input regex")
    parser.add_argument(
        '-pg', '--gutenberg',
        type=int, default=2701,
        help="ID number of a Project Gutenberg text")
    parser.add_argument(
        '-nw', '--no-web', action='store_true',
        help="Don't open a web browser to show the source file")
    args = parser.parse_args()

    url = "https://www.gutenberg.org/ebooks/" + str(args.gutenberg)

    text = text_from_pg(args.gutenberg)
    print("Text has", commafy(len(text)), "characters")
    # pprint(text)
    words = words_from_text(text)
    print("Text has", commafy(len(words)), "unique words")
    found = set()
    for word in words:
        if word not in found and re.search(args.pattern, word):
            found.add(word)

    summarise(found, "matching words")

    print("\nSource: " + url)

# End of file
