import argparse
from wowool.native.core.pipeline import Pipeline
from pathlib import Path
from collections import Counter


def parse_arguments():
    """
    Parses the command line arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="input file", nargs="*", required=False)
    parser.add_argument("-i", "--input", help="input text")
    parser.add_argument("-p", "--pipeline", help="input model")
    parser.add_argument("--no-show", help="Show the output", action="store_false")
    args = parser.parse_args()
    return args


def print_entities(doc):
    """
    Display entities.
    """
    print(doc)
    print("Entities:\n==========")
    for ent in doc.concepts():
        print(f"{ent.text} - {ent.uri}")


if __name__ == "__main__":
    kwargs = dict(parse_arguments()._get_kwargs())
    engine = Pipeline(kwargs["pipeline"])
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
