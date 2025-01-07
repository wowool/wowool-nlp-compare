from typing import Any
import stanza
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


class NLPStanza:
    language_short_form: str
    name: str = "stanza"
    engine: Any | None = None

    def __init__(self, language_short_form, **kwargs):
        self.language_short_form = language_short_form
        stanza.download(self.language_short_form)
        self.engine = stanza.Pipeline(self.language_short_form)

    def __call__(self, text):
        return self.engine(text)

    def get_compare_data(self, other_, doc):
        for entity in doc.entities:
            uri = entity.type
            other_.data.append(
                CmpItem(entity.start_char, entity.end_char, self.name, uri, entity.text)
            )
            other_.counter[uri] += 1

    def get_mapping_table(self):
        return entity_mapping_table[self.language_short_form]
