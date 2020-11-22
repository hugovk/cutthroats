#!/usr/bin/env python
"""
Given some known cutthroats, find their verb- stems.
Then given a text, find other words beginning with those verbs.
They might be new cutthroats!

Run either on a local text file, or on a remote Project Gutenberg text.
"""
import argparse
import sys
import webbrowser

# from pprint import pprint


def load_set(the_filename):
    try:
        with open(the_filename) as f:
            my_set = {
                line.rstrip("\n").lower() for line in f
            }

        # Also add any "cut-throats" as "cutthroats"
        set_copy = my_set.copy()
        for word in set_copy:
            if "-" in word:
                my_set.add(word.replace("-", ""))
    except OSError:
        my_set = set()
    return my_set


def split_stems(cutthroats):
    """Given a list of cutthroats, find the verb- and -noun stems.
    Ignores unhyphenated.
    """
    verbs = set()
    nouns = set()
    for cutthroat in cutthroats:
        if "-" in cutthroat:
            for word in cutthroat.split():
                if "-" in word:
                    stems = word.rstrip(",").split("-")
                    verb = stems[0]
                    noun = stems[-1]
                    if len(verb):
                        verbs.add(verb.lower())
                    if len(noun):
                        nouns.add(noun.lower())
                    # print(verb, "\t", noun, "\t", word, "\t", cutthroat)
    return verbs, nouns


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
    return {word.lower() for word in blob.words}


def classify_word(word, cutthroats, found_known, found_unknown):
    is_known = known(word, cutthroats)
    # print(word, "\t", verb, is_known)
    if is_known:
        found_known.add(word)
    else:
        found_unknown.add(word)
        if args.gutenberg and len(found_unknown) == 1:
            open_url(url)
    return found_known, found_unknown


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


def commafy(value):
    """Add thousands commas"""
    return f"{value:,}"


def summarise(some_set, text):
    if len(some_set):
        print("\nFound", commafy(len(some_set)), text + ":\n")
        some_set = sorted(some_set)
        print("\n".join(some_set))
    else:
        print("\nFound no " + text + ".\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Given some known cutthroats, find their verb- stems."
        "Then given a text, find other words beginning with "
        "those verbs. They might be new cutthroats!",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-c",
        "--cutthroats",
        default="cutthroats.txt",
        help="Text list of known cutthroats, one per line",
    )
    parser.add_argument(
        "-nc",
        "--not-cutthroats",
        default="not-cutthroats.txt",
        help="Things that look like cutthroats but aren't",
    )
    parser.add_argument(
        "-pg",
        "--gutenberg",
        type=int,
        help="ID number of a Project Gutenberg text (eg. 2701). "
        "Use this or a filename",
    )
    parser.add_argument(
        "-f", "--filename", help="Filename of a text. Use this or PG ID"
    )
    parser.add_argument(
        "-oh",
        "--only-hyphenated",
        action="store_true",
        help="Only return potential cutthroats that contain hyphens",
    )
    parser.add_argument(
        "-mn",
        "--match-nouns",
        action="store_true",
        help="Only return potential cutthroats that also end in known -noun"
        "stems. Fewer results, but better chance of cutthroats?",
    )
    parser.add_argument(
        "-nw",
        "--no-web",
        action="store_true",
        help="Don't open a web browser to show the source file",
    )
    args = parser.parse_args()

    url = "https://www.gutenberg.org/ebooks/" + str(args.gutenberg)

    cutthroats = load_set(args.cutthroats)
    not_cutthroats = load_set(args.not_cutthroats)
    verbs, nouns = split_stems(cutthroats)
    # pprint(verbs)
    # pprint(nouns)
    print("Found", len(verbs), "cutverbs")
    print("Found", len(nouns), "throatnouns")

    # TODO instead use a single mandatory argument:
    # if a local file with this name exists, open it
    # else if an integer, fetch from Project Gutenberg
    if args.gutenberg:
        text = text_from_pg(args.gutenberg)
    elif args.filename:
        with open(args.filename) as f:
            text = f.read()
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

                if not word.startswith(verb):
                    continue

                if args.match_nouns:

                    for noun in nouns:
                        if word == verb + noun:
                            found_known, found_unknown = classify_word(
                                word, cutthroats, found_known, found_unknown
                            )
                            break

                else:  # don't match nouns

                    if len(word) > len(verb):

                        found_known, found_unknown = classify_word(
                            word, cutthroats, found_known, found_unknown
                        )

    summarise(found_not_cutthroats, "not-cutthroats")
    summarise(found_known, "known cutthroats")
    summarise(found_unknown, "potential new cutthroats")

    if args.gutenberg:
        print("\nSource: " + url)
    elif args.filename:
        print("\nSource: " + args.filename)

# End of file
