from typing import Any
from google.cloud import language_v1
from nlp_compare.cmp_objects import CmpItem
from os import environ


entity_mapping_table = {
    "es": {
        "Person": "PERSON",
        "Company": "ORGANIZATION",
        "Organization": "ORGANIZATION",
        "City": "LOCATION",
        "Country": "LOCATION",
        "Street": "LOCATION",
        "Facility": "FAC",
        "WorldRegion": "LOCATION",
        "PlaceAdj": "LOCATION",
        "MoneyAmount": "MONEY",
        "Event": "EVENT",
    },
    "nl": {
        "Person": "PERSON",
        "Company": "ORGANIZATION",
        "Organization": "ORGANIZATION",
        "City": "LOCATION",
        "Country": "LOCATION",
        "Street": "LOCATION",
        "Facility": "LOCATION",
        "WorldRegion": "LOCATION",
        "MoneyAmount": "MONEY",
        "Event": "EVENT",
    },
    "de": {
        "Person": "PERSON",
        "Company": "ORGANIZATION",
        "Organization": "ORGANIZATION",
        "City": "LOCATION",
        "Country": "LOCATION",
        "Street": "LOCATION",
        "Facility": "LOCATION",
        "WorldRegion": "LOCATION",
        "PlaceAdj": "LOCATION",
        "MoneyAmount": "MONEY",
        "Event": "EVENT",
    },
    "en": {
        "Sentence": "Sentence",
        "Person": "PERSON",
        "Position": "Position",
        "Company": "ORGANIZATION",
        "Organization": "ORGANIZATION",
        "Publisher": "ORGANIZATION",
        "City": "GPE",
        "Country": "GPE",
        "Date": "DATE",
        "Street": "LOCATION",
        "Facility": "LOCATION",
        "WorldRegion": "LOCATION",
        "PlaceAdj": "NORP",
        "MoneyAmount": "MONEY",
        "Event": "EVENT",
        "TimePhrase": "TIME",
        "Place": "GPE",
    },
}


class NLPGoogle:
    language_short_form: str
    name: str = "google"
    engine: Any | None = None

    def __init__(self, language_short_form: str, **kwargs):
        self.language_short_form = language_short_form
        self.engine = language_v1.LanguageServiceClient()

    def __call__(self, text):
        document = language_v1.Document(
            content=text, type=language_v1.Document.Type.PLAIN_TEXT
        )

        response = self.engine.analyze_entities(
            request={
                "document": document,
                "encoding_type": language_v1.EncodingType.UTF8,
            }
        )
        return response

    def get_compare_data(self, other_, doc):

        for entity in doc.entities:
            uri = language_v1.Entity.Type(entity.type).name
            for mention in entity.mentions:
                try:
                    begin_offset = mention.text.begin_offset
                except AttributeError:
                    begin_offset = 0

                other_.data.append(
                    CmpItem(
                        begin_offset,
                        begin_offset + len(mention.text.content),
                        self.name,
                        uri,
                        mention.text.content,
                    )
                )
                other_.counter[uri] += 1

    def get_mapping_table(self):
        return entity_mapping_table[self.language_short_form]
