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

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    kwargs = dict(parse_arguments()._get_kwargs())
    engine = Pipeline(kwargs["pipeline"])
    uris = Counter()
    if "input" in kwargs and kwargs["input"]:
        text = kwargs.pop("input")
        doc = engine(text)
        print("Entities:\n==========")
        for ent in doc.concepts():
            uris[ent.uri] += 1
            print(f"{ent.text} - {ent.uri}")
    else:
        files = kwargs.pop("file")
        for filename in files:
            fn = Path(filename)
            if fn.exists():
                text = fn.read_text()
                doc = engine(text)
                print("Entities:\n==========")
                for ent in doc.concepts():
                    uris[ent.uri] += 1
                    print(f"{ent.text} - {ent.uri}")
            else:
                print(f"File not found: {fn}")

    print(uris)
