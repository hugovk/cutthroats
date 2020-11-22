#!/usr/bin/env python
"""
Find potential cutthroat compounds from a wordlist.
Specifically: find words with a single hyphen and no spaces,
and check (via Wordnik) the first part can be a verb and the second a noun.
For example: be-all, cease-fire, cure-all, do-good, fuss-budget, make-work.
"""
import argparse
import sys

import yaml
from wordnik import WordApi, swagger


def load_yaml(filename):
    """
    File should contain:
    wordnik_api_key: TODO_ENTER_YOURS
    """
    f = open(filename)
    data = yaml.safe_load(f)
    f.close()
    if not data.viewkeys() >= {"wordnik_api_key"}:
        sys.exit("Wordnik credentials missing from YAML: " + filename)
    return data


def read_file(filename):
    """ Open a file and return a list of lines"""
    with open(filename) as f:
        lines = f.readlines()
    return lines


def clean_lines(lines):
    """Keep those with no spaces and only one hyphen"""
    kept = []
    for line in lines:
        if " " not in line and line.count("-") == 1:
            line = line.translate(None, "'")  # Remove ' chars
            kept.append(line.strip())
    return kept


def is_pos(word, part_of_speech):
    """Is this word that part-of-speech?"""
    result = word_api.getDefinitions(word, partOfSpeech=part_of_speech, limit=1)
    if result:
        return True
    else:
        return False


def verb_nouns(lines):
    """Return lines where the first part can be a verb and the second a noun"""
    print("Potential cutthroats:")
    potentials = []
    for line in lines:
        parts = line.lower().split("-")
        if (
            parts[0]
            and parts[1]
            and is_pos(parts[0], "verb-transitive")
            and is_pos(parts[1], "noun")
        ):
            # is_pos(parts[0], "verb-transitive")):
            print(line)
            potentials.append(line)
    return potentials


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Find potential cutthroat compounds from a wordlist.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-y",
        "--yaml",
        default="wordnik.yaml",
        help="YAML file location containing Wordnik API key",
    )
    parser.add_argument(
        "-i",
        "--infile",
        default="index.noun-hyphenated",
        help="Input word file, one word per line",
    )
    args = parser.parse_args()

    lines = read_file(args.infile)
    print(len(lines))

    lines = clean_lines(lines)
    print(len(lines))

    credentials = load_yaml(args.yaml)
    wordnik_client = swagger.ApiClient(
        credentials["wordnik_api_key"], "http://api.wordnik.com/v4"
    )
    word_api = WordApi.WordApi(wordnik_client)

    lines = verb_nouns(lines)
    print(len(lines))

# End of file
