from typing import Any
from google.cloud import language_v1
from nlp_compare.cmp_objects import CmpItem
from nlp_compare.concept_filter import ConceptFilter
from nlp_compare.cmp_objects import NLPEngine
from logging import getLogger

logger = getLogger("nlp.cmp.google")
entity_mapping_table = {
    "es": {
        "ORGANIZATION": "ORG",
        "LOCATION": "GPE",
        "ADDRESS": "LOC",
    },
    "nl": {
        "ORGANIZATION": "ORG",
        "LOCATION": "GPE",
        "ADDRESS": "LOC",
    },
    "de": {
        "ORGANIZATION": "ORG",
        "LOCATION": "GPE",
        "ADDRESS": "LOC",
    },
    "en": {
        "ORGANIZATION": "ORG",
        "LOCATION": "GPE",
        "ADDRESS": "LOC",
    },
}


class NLPGoogle(NLPEngine):
    language_short_form: str
    name: str = "google"
    engine: Any | None = None

    def __init__(self, cmp_idx, language_short_form: str, **kwargs):
        super().__init__(cmp_idx)
        self.language_short_form = language_short_form
        self.engine = language_v1.LanguageServiceClient()
        self.map_table = entity_mapping_table.get(self.language_short_form, {})

    def warmup(self): ...

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

    def get_compare_data(self, other_, doc, concept_filter: ConceptFilter):

        for entity in doc.entities:
            logger.debug(f"GOOGLE: {entity}")
            original_uri = language_v1.Entity.Type(entity.type).name
            uri = (
                self.map_table[original_uri]
                if original_uri in self.map_table
                else original_uri
            )
            if not concept_filter(uri):
                continue
            # print(entity)
            first_mention = None
            for mention in entity.mentions:

                try:
                    begin_offset = mention.text.begin_offset
                except AttributeError:
                    begin_offset = 0

                if first_mention is None:
                    first_mention = mention.text.content

                other_.data.append(
                    CmpItem(
                        self.cmp_idx,
                        begin_offset,
                        begin_offset + len(mention.text.content),
                        self.name,
                        uri,
                        first_mention,
                        original_uri=original_uri,
                    )
                )
                other_.counter[uri] += 1

    def get_mapping_table(self):
        return entity_mapping_table[self.language_short_form]
