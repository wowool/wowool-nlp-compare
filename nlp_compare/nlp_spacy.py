from typing import Any
import spacy
from nlp_compare.cmp_objects import CmpItem


entity_mapping_table = {
    "es": {
        "Sentence": "Sentence",
        "Person": "PER",
        "Company": "ORG",
        "Organization": "ORG",
        "City": "LOC",
        "Country": "LOC",
        "Street": "LOC",
        "Facility": "FAC",
        "WorldRegion": "LOC",
        "PlaceAdj": "LOC",
        "MoneyAmount": "MONEY",
        "Event": "EVENT",
    },
    "nl": {
        "Sentence": "Sentence",
        "Person": "PER",
        "Company": "ORG",
        "Organization": "ORG",
        "City": "LOC",
        "Country": "LOC",
        "Street": "LOC",
        "Facility": "LOC",
        "WorldRegion": "LOC",
        "MoneyAmount": "MONEY",
        "Event": "EVENT",
    },
    "de": {
        "Sentence": "Sentence",
        "Person": "PER",
        "Company": "ORG",
        "Organization": "ORG",
        "City": "LOC",
        "Country": "LOC",
        "Street": "LOC",
        "Facility": "LOC",
        "WorldRegion": "LOC",
        "PlaceAdj": "LOC",
        "MoneyAmount": "MONEY",
        "Event": "EVENT",
    },
    "en": {
        "Sentence": "Sentence",
        "Person": "PERSON",
        "Company": "ORG",
        "Organization": "ORG",
        "Publisher": "ORG",
        "City": "GPE",
        "Country": "GPE",
        "Date": "DATE",
        "Street": "LOC",
        "Facility": "LOC",
        "WorldRegion": "LOC",
        "PlaceAdj": "NORP",
        "MoneyAmount": "MONEY",
        "Event": "EVENT",
        "TimePhrase": "TIME",
        "Place": "GPE",
    },
}


class NLPSpacy:
    language_short_form: str
    name: str = "spacy"
    engine: Any | None = None

    def __init__(self, language_short_form: str, **kwargs):
        self.language_short_form = language_short_form
        model_part = "core_web" if self.language_short_form == "en" else "core_news"
        if "model" in kwargs and kwargs["model"]:
            self.model_mame = kwargs["model"]
        else:
            model_size = (
                kwargs["model_size"]
                if "model_size" in kwargs and kwargs["model_size"]
                else "sm"
            )
            self.model_mame = f"{self.language_short_form}_{model_part}_{model_size}"
        try:
            self.engine = spacy.load(self.model_mame)

        except OSError:
            raise ImportError(
                f"""Please install spacy and the corresponding language model for {self.model_mame}
try:\npython -m spacy download {self.model_mame} """
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

    def get_mapping_table(self):
        return entity_mapping_table[self.language_short_form]
