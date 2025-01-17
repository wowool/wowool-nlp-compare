import argparse
from google.cloud import language_v1
from pathlib import Path
from collections import Counter


def parse_arguments():
    """
    Parses the command line arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="input file", nargs="*", required=False)
    parser.add_argument("-i", "--input", help="input text")

    args = parser.parse_args()
    return args


def get_entities(engine, text: str) -> dict:
    """
    Get entities from a text.
    """
    engine = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=text, type=language_v1.Document.Type.PLAIN_TEXT
    )

    doc = engine.analyze_entities(
        request={
            "document": document,
            "encoding_type": language_v1.EncodingType.UTF8,
        }
    )
    return doc


def display_entities(doc, uris):
    """
    Display entities.
    """
    print("", doc.entities)
    print("Entities:\n==========")
    for entity in doc.entities:
        uri = language_v1.Entity.Type(entity.type).name
        print(f"{entity.name} - {uri}")
        uris[uri] += 1
        for mention in entity.mentions:
            print(f"  - {mention.text.content}")


if __name__ == "__main__":
    kwargs = dict(parse_arguments()._get_kwargs())
    engine = language_v1.LanguageServiceClient()
    uris = Counter()
    if "input" in kwargs and kwargs["input"]:
        text = kwargs.pop("input")

        doc = get_entities(engine, text)
        display_entities(doc, uris)
    else:
        files = kwargs.pop("file")
        for filename in files:
            fn = Path(filename)
            if fn.exists():
                text = fn.read_text()
                doc = get_entities(engine, text)
                display_entities(doc, uris)
            else:
                print(f"File not found: {fn}")

    print(uris)
