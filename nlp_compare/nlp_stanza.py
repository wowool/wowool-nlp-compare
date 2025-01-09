from typing import Any
import stanza
from nlp_compare.cmp_objects import CmpItem
from nlp_compare.concept_filter import ConceptFilter
from nlp_compare.cmp_objects import NLPEngine

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


class NLPStanza(NLPEngine):
    name: str = "stanza"

    def __init__(self, cmp_idx, language_short_form, **kwargs):
        super().__init__(cmp_idx)
        self.language_short_form = language_short_form
        stanza.download(self.language_short_form)
        self.engine = stanza.Pipeline(self.language_short_form)
        self.map_table = entity_mapping_table.get(self.language_short_form, {})

    def warmup(self):
        self.engine("warmup")

    def __call__(self, text):
        return self.engine(text)

    def get_compare_data(self, other_, doc, concept_filter: ConceptFilter):
        for entity in doc.entities:

            uri = (
                self.map_table[entity.type]
                if entity.type in self.map_table
                else entity.type
            )

            if not concept_filter(uri):
                continue

            other_.data.append(
                CmpItem(
                    self.cmp_idx,
                    entity.start_char,
                    entity.end_char,
                    self.name,
                    uri,
                    entity.text,
                )
            )
            other_.counter[uri] += 1

    def get_mapping_table(self):
        return entity_mapping_table[self.language_short_form]
