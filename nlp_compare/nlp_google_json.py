from typing import Any
from nlp_compare.cmp_objects import CmpItem
from nlp_compare.concept_filter import ConceptFilter
from nlp_compare.cmp_objects import NLPEngine
from logging import getLogger
from pathlib import Path
import json

# note: you need to set the environment variable GOOGLE_APPLICATION_CREDENTIALS with the path to your google credentials
# GOOGLE_APPLICATION_CREDENTIALS

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


def map_offsets(fn, jo):
    from wowool.sdk import Pipeline
    from wowool.document.factory import Factory

    # import json
    # from pathlib import Path

    pipeline = Pipeline("english(unicode_offsets=false)")

    doc = Factory.create(fn)
    doc = pipeline(doc)
    print(doc)

    real_offsets = [a.begin_offset for a in doc.tokens]
    real_offsets.extend([a.end_offset for a in doc.tokens])

    pipeline = Pipeline("english")

    doc = Factory.create(fn)
    doc = pipeline(doc)

    py_offsets = [a.begin_offset for a in doc.tokens]
    py_offsets.extend([a.end_offset for a in doc.tokens])

    real_2_py = {}
    for pyo, ro in zip(py_offsets, real_offsets):
        real_2_py[ro] = pyo

    for entity in jo["entities"]:
        for mention in entity["mentions"]:
            if mention["text"]["beginOffset"] not in real_2_py:
                print("not found", entity)
                exit(-1)
            mention["text"]["beginOffset"] = real_2_py[mention["text"]["beginOffset"]]
    return jo
    # Path(pyo_fn).write_text(json.dumps(jo, indent=2))


class NLPGoogle(NLPEngine):
    language_short_form: str
    name: str = "google"
    engine: Any | None = None

    def __init__(self, cmp_idx, language_short_form: str, json_results: str, **kwargs):
        super().__init__(cmp_idx)
        self.fn = Path(json_results)
        self.language_short_form = language_short_form
        self.map_table = entity_mapping_table.get(self.language_short_form, {})

    def warmup(self): ...

    def __call__(self, text):

        response = json.loads(self.fn.read_text())
        return response

    def get_compare_data(
        self, other_, doc, concept_filter: ConceptFilter, input_provider
    ):

        # print("======>>>", input_provider.id)

        # exit(-1)

        doc = map_offsets(input_provider.id, doc)
        for entity in doc["entities"]:
            logger.debug(f"GOOGLE: {entity}")
            original_uri = entity["type"]
            uri = (
                self.map_table[original_uri]
                if original_uri in self.map_table
                else original_uri
            )
            if not concept_filter(uri):
                continue
            # print(entity)
            first_mention = None
            for mention in entity["mentions"]:
                if original_uri == "PERSON" and mention["type"] == "COMMON":
                    continue
                try:
                    begin_offset = mention["text"]["beginOffset"]
                except AttributeError:
                    begin_offset = 0

                if first_mention is None:
                    first_mention = mention["text"]["content"]

                other_.data.append(
                    CmpItem(
                        self.cmp_idx,
                        begin_offset,
                        begin_offset + len(mention["text"]["content"]),
                        self.name,
                        uri,
                        first_mention,
                        original_uri=original_uri,
                    )
                )
                other_.counter[uri] += 1
        other_.data.sort(key=lambda x: x.begin_offset)

    def get_mapping_table(self):
        return entity_mapping_table[self.language_short_form]
