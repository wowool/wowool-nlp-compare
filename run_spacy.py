#!/usr/bin/env python
import argparse
import spacy
from pathlib import Path
from collections import Counter
from profile_it import profile_it
from spacy.pipeline import Sentencizer


def parse_arguments():
    """
    Parses the command line arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="input file", nargs="*", required=False)
    parser.add_argument("-i", "--input", help="input text")
    parser.add_argument("-m", "--model", help="input model")
    parser.add_argument("--no-show", help="Show the output", action="store_false")

    args = parser.parse_args()
    return args


def print_entities(doc):
    """
    Display entities.
    """
    sentencizer = Sentencizer()
    doc = sentencizer(doc)
    print(f"Document: {doc.text}")
    print(f"Number of sentences: {len(list(doc.sents))}")
    for sent in doc.sents:
        print(f"Sentence: {sent.text}")

    print("Entities:\n==========")
    for ent in doc.ents:
        uris[ent.label_] += 1
        print(f"{ent.text} - {ent.label_}")


@profile_it
def run(engine, text: str, fn=""):
    print(f"Processing: {fn}")
    return engine(text)


if __name__ == "__main__":
    kwargs = dict(parse_arguments()._get_kwargs())
    engine = spacy.load(kwargs["model"])
    uris = Counter()
    show = kwargs.pop("no_show")
    if "input" in kwargs and kwargs["input"]:
        text = kwargs.pop("input")
        doc = run(engine, text)
        if show:
            print_entities(doc)
    else:
        files = kwargs.pop("file")
        for filename in files:
            fn = Path(filename)
            if fn.exists():
                text = fn.read_text()
                doc = run(engine, text, fn)
                if show:
                    print_entities(doc)
            else:
                print(f"File not found: {fn}")

    print(uris)
