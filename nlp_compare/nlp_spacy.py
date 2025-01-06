from dataclasses import dataclass
from typing import Any
import spacy
from nlp_compare.cmp_objects import CmpItem


class NLPSpacy:
    language_short_form: str
    name: str = "spacy"
    engine: Any | None = None

    def __init__(self, language_short_form: str, **kwargs):
        try:
            self.language_short_form = language_short_form
            if "model" in kwargs:
                self.engine = spacy.load(kwargs["model"])
            else:
                self.engine = spacy.load(f"{self.language_short_form}_core_web_sm")
        except OSError:
            raise ImportError(
                f"""Please install spacy and the corresponding language model for {self.language_short_form}
try:\npython -m spacy download {self.language_short_form}_core_web_sm"""
            )

    def __call__(self, text):
        return self.engine(text)

    def get_compare_data(self, other_, doc):
        for entity in doc.ents:
            uri = entity.label_
            other_.data.append(
                CmpItem(entity.start_char, entity.end_char, self.name, uri, entity.text)
            )
            other_.counter[uri] += 1
