from typing import Any
import stanza
from nlp_compare.cmp_objects import CmpItem
from nlp_compare.concept_filter import ConceptFilter
from nlp_compare.cmp_objects import NLPEngine
from logging import getLogger
from memory_profiler import profile
from nlp_compare.profile import nlp_profile

logger = getLogger("nlp.cmp.stanza")

entity_mapping_table = {}


class NLPStanza(NLPEngine):
    name: str = "stanza"

    @profile
    def __init__(self, cmp_idx, language_short_form, **kwargs):
        super().__init__(cmp_idx)
        self.language_short_form = language_short_form
        stanza.download(self.language_short_form)
        self.engine = stanza.Pipeline(
            self.language_short_form, processors="tokenize,ner,coref"
        )
        self.map_table = entity_mapping_table.get(self.language_short_form, {})
        self.warmup()

    def warmup(self):
        self.engine("warmup")

    @profile
    def __call__(self, text):
        return self.engine(text)

    def get_compare_data(self, other_, doc, concept_filter: ConceptFilter):
        for entity in doc.entities:
            logger.debug(
                f"STANZA: {entity.start_char} {entity.end_char} {entity.type} {entity.text}"
            )

            original_uri = entity.type
            uri = (
                self.map_table[original_uri]
                if original_uri in self.map_table
                else original_uri
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
                    original_uri=original_uri,
                )
            )
            other_.counter[uri] += 1

    def get_mapping_table(self):
        return entity_mapping_table[self.language_short_form]
