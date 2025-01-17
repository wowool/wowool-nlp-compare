import argparse
from google.cloud import language_v1, language_v2
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
    engine = language_v2.LanguageServiceClient()
    document = language_v2.Document(
        content=text, type=language_v2.Document.Type.PLAIN_TEXT
    )

    doc = engine.annotate_text(
        request={
            "document": document,
            "encoding_type": language_v2.EncodingType.UTF8,
            "features": {
                "extract_entities": True,
                "extract_document_sentiment": True,
                "classify_text": True,
                "moderate_text": True,
            },
        }
    )
    print(doc)


def display_entities(doc):
    """
    Display entities.
    """
    ...


if __name__ == "__main__":
    kwargs = dict(parse_arguments()._get_kwargs())
    engine = language_v2.LanguageServiceClient()
    uris = Counter()
    if "input" in kwargs and kwargs["input"]:
        text = kwargs.pop("input")

        doc = get_entities(engine, text)
        display_entities(doc)
    else:
        files = kwargs.pop("file")
        for filename in files:
            fn = Path(filename)
            if fn.exists():
                text = fn.read_text()
                doc = get_entities(engine, text)
                display_entities(doc)
            else:
                print(f"File not found: {fn}")

    print(uris)
