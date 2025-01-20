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
    parser.add_argument("--no-show", help="Show the output", action="store_false")

    args = parser.parse_args()
    return args


def print_entities(doc):
    """
    Display entities.
    """
    print("Entities:\n==========")
    for ent in doc.entities:
        uris[ent.type] += 1
        print(f"{ent}")


if __name__ == "__main__":
    kwargs = dict(parse_arguments()._get_kwargs())
    engine = stanza.Pipeline(kwargs["language"], processors="tokenize,ner,coref")
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
                # print(doc)

                # for i, sentence in enumerate(doc.sentences):
                #     print(f"====== Sentence {i+1} tokens =======")
                #     print(
                #         *[
                #             f"id: {token.id}\ttext: {token.text}"
                #             for token in sentence.tokens
                #         ],
                #         sep="\n",
                #     )

            else:
                print(f"File not found: {fn}")

    print(uris)
