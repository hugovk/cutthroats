#!/usr/bin/env python
# encoding: utf-8
"""
Given some known cutthroats, find their verb- stems.
Then given a text, find other words beginning with those verbs.
They might be new cutthroats!

Run either on a local text file, or on a remote Project Gutenberg text.
"""
from __future__ import print_function, unicode_literals
import argparse
import sys
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
    from textblob import TextBlob  # pip install textblob
    blob = TextBlob(text)
    return set(word.lower() for word in blob.words)


def known(word, some_list):
    """Is word known in some_list?"""
    if word in some_list:
        return True
    unhyphenated = word.replace("-", "")
    if unhyphenated in some_list:
        return True
    elif word.rstrip("s") in some_list:
        return True
    elif unhyphenated.rstrip("s") in some_list:
        return True
    else:
        return False


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
        description="Given some known cutthroats, find their verb- stems."
                    "Then given a text, find other words beginning with "
                    "those verbs. They might be new cutthroats!",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '-c', '--cutthroats',
        default='cutthroats.txt',
        help="Text list of known cutthroats, one per line")
    parser.add_argument(
        '-nc', '--not-cutthroats',
        default='not-cutthroats.txt',
        help="Things that look like cutthroats but aren't")
    parser.add_argument(
        '-pg', '--gutenberg',
        type=int,
        help="ID number of a Project Gutenberg text (eg. 2701). "
             "Use this or a filename")
    parser.add_argument(
        '-f', '--filename',
        help="Filename of a text. Use this or PG ID")
    parser.add_argument(
        '-oh', '--only-hyphenated', action='store_true',
        help="Only return potential cutthroats that contain hyphens")
    parser.add_argument(
        '-nw', '--no-web', action='store_true',
        help="Don't open a web browser to show the source file")
    args = parser.parse_args()

    url = "https://www.gutenberg.org/ebooks/" + str(args.gutenberg)

    cutthroats = load_list(args.cutthroats)
    not_cutthroats = load_list(args.not_cutthroats)
    verbs = cut_verbs(cutthroats)
    # pprint(verbs)
    print("Found", len(verbs), "cutverbs")

    # TODO instead use a single mandatory argument:
    # if a local file with this name exists, open it
    # else if an integer, fetch from Project Gutenberg
    if args.gutenberg:
        text = text_from_pg(args.gutenberg)
    elif args.filename:
        with open(args.filename) as f:
            text = f.read().decode('unicode-escape')
    else:
        sys.exit("Give a filename or Project Gutenberg ID number")

    print("Text has", commafy(len(text)), "characters")
    # pprint(text)
    words = words_from_text(text)
    print("Text has", commafy(len(words)), "unique words")
    found_unknown = set()
    found_known = set()
    found_not_cutthroats = set()
    for word in words:
        if known(word, not_cutthroats):
            found_not_cutthroats.add(word)
            continue
        if (args.only_hyphenated and "-" in word) or not args.only_hyphenated:
            for verb in verbs:
                if args.only_hyphenated:
                    verb = verb + "-"
                if word.startswith(verb) and len(word) > len(verb):
                    is_known = known(word, cutthroats)
                    # print(word, "\t", verb, known)
                    if is_known:
                        found_known.add(word)
                    else:
                        found_unknown.add(word)
                        if args.gutenberg and len(found_unknown) == 1:
                            open_url(url)

    summarise(found_not_cutthroats, "not-cutthroats")
    summarise(found_known, "known cutthroats")
    summarise(found_unknown, "potential new cutthroats")

    if args.gutenberg:
        print("\nSource: " + url)
    elif args.filename:
        print("\nSource: " + args.filename)

# End of file
