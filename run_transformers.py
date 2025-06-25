#!/usr/bin/env python
import argparse
from pathlib import Path
from collections import Counter
from profile_it import profile_it
from dataclasses import dataclass, field
from typing import Any
from transformers import AutoTokenizer, AutoModelForTokenClassification
import torch


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


@dataclass
class Entity:
    label: str
    start: int
    end: int
    text: str


@dataclass
class Document:
    entities: list[Entity] = field(default_factory=list[Entity])


@dataclass
class Engine:
    model: Any
    tokenizer: Any

    def __call__(self, text: str):
        # Tokenize with offsets
        tokens = self.tokenizer(
            text,
            return_offsets_mapping=True,
            return_tensors="pt",
            truncation=True,
            is_split_into_words=False,
        )

        offsets = list(
            tokens.pop("offset_mapping")[0]
        )  # <- remove it before feeding to model

        word_ids = tokens.word_ids()

        # Run prediction
        with torch.no_grad():
            outputs = self.model(**tokens)
        logits = outputs.logits
        predictions = torch.argmax(logits, dim=2)[0].tolist()

        # Map prediction indices to labels
        id2label = self.model.config.id2label
        labels = [id2label[p] for p in predictions]

        # Extract entities with offsets
        entities = []
        current_entity = None

        for idx, (label, offset, word_id) in enumerate(zip(labels, offsets, word_ids)):
            # print(idx, label, offset, word_id)
            if offset == [0, 0] or word_id is None:
                continue  # Skip special tokens

            start, end = int(offset[0]), int(offset[1])
            word = text[start:end]

            if label.startswith("B-"):
                if current_entity:
                    entities.append(current_entity)
                current_entity = Entity(
                    label=label[2:],
                    start=start,
                    end=end,
                    text=word,
                )
            elif (
                label.startswith("I-")
                and current_entity
                and label[2:] == current_entity.label
            ):
                current_entity.end = end
                current_entity.text = text[current_entity.start : end]
            else:
                if current_entity:
                    entities.append(current_entity)
                    current_entity = None

        if current_entity:
            entities.append(current_entity)

        return Document(entities)


# # Load model and tokenizer

# # The sentence to analyse
# text = "IAEA chief expects 'very significant damage' at Iran's Fordow site."


# entities = predict_ner(text, tokenizer, model)

# # Output
# for ent in entities:
#     print(ent)


def print_entities(doc):
    """
    Display entities.
    """
    print("Entities:\n==========")
    for ent in doc.entities:
        uris[ent.label] += 1
        print(f"{ent.text} - {ent.label} ({ent.start}, {ent.end})")


@profile_it
def run(engine, text: str, fn=""):

    return engine(text)


if __name__ == "__main__":
    kwargs = dict(parse_arguments()._get_kwargs())
    model_name = kwargs["model"]
    engine = Engine(
        tokenizer=AutoTokenizer.from_pretrained(model_name),
        model=AutoModelForTokenClassification.from_pretrained(model_name),
    )
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
