import argparse
import stanza
from pathlib import Path
from collections import Counter


def parse_arguments():
    """
    Parses the command line arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="input file", nargs="*", required=False)
    parser.add_argument("-i", "--input", help="input text")
    parser.add_argument("-l", "--language", help="language: example 'en'")

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    kwargs = dict(parse_arguments()._get_kwargs())
    engine = stanza.Pipeline(kwargs["language"], processors="tokenize,ner,coref")
    uris = Counter()

    if "input" in kwargs and kwargs["input"]:
        text = kwargs.pop("input")
        doc = engine(text)
        print("Entities:\n==========")
        for ent in doc.entities:
            uris[ent.type] += 1
            print(f"{ent}")
    else:
        files = kwargs.pop("file")

        for filename in files:
            fn = Path(filename)
            if fn.exists():
                text = fn.read_text()
                doc = engine(text)
                print(doc)

                for i, sentence in enumerate(doc.sentences):
                    print(f"====== Sentence {i+1} tokens =======")
                    print(
                        *[
                            f"id: {token.id}\ttext: {token.text}"
                            for token in sentence.tokens
                        ],
                        sep="\n",
                    )

                print("Entities:\n==========")
                for ent in doc.ents:
                    uris[ent.type] += 1
                    print(f"{ent}")
            else:
                print(f"File not found: {fn}")

    print(uris)
