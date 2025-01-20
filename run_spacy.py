import argparse
import spacy
from pathlib import Path
from collections import Counter


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
    print("Entities:\n==========")
    for ent in doc.ents:
        uris[ent.label_] += 1
        print(f"{ent.text} - {ent.label_}")


if __name__ == "__main__":
    kwargs = dict(parse_arguments()._get_kwargs())
    engine = spacy.load(kwargs["model"])
    uris = Counter()
    show = kwargs.pop("no_show")
    if "input" in kwargs and kwargs["input"]:
        text = kwargs.pop("input")
        doc = engine(text)
        if show:
            print_entities(doc)
    else:
        files = kwargs.pop("file")
        for filename in files:
            fn = Path(filename)
            if fn.exists():
                text = fn.read_text()
                doc = engine(text)
                if show:
                    print_entities(doc)
            else:
                print(f"File not found: {fn}")

    print(uris)
