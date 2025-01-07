import argparse
import spacy
from pathlib import Path


def parse_arguments():
    """
    Parses the command line arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="input file", nargs="+", required=True)
    parser.add_argument("-m", "--model", help="input model")

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    kwargs = dict(parse_arguments()._get_kwargs())

    engine = spacy.load(kwargs["model"])
    files = kwargs.pop("file")
    for filename in files:
        fn = Path(filename)
        if fn.exists():
            text = fn.read_text()
            doc = engine(text)
            print("Entities:\n==========")
            for ent in doc.ents:
                print(f"{ent.text} - {ent.label_}")
        else:
            print(f"File not found: {fn}")
