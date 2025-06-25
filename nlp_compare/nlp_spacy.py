from typing import Any
import spacy
from nlp_compare.cmp_objects import CmpItem
from nlp_compare.concept_filter import ConceptFilter
import re
from nlp_compare.cmp_objects import NLPEngine
from logging import getLogger

from nlp_compare.profile import nlp_profile
from memory_profiler import profile

logger = getLogger("nlp.cmp.spacy")

entity_mapping_table = {}


cleanup_table = {
    "en": [[re.compile(r"'s$|^the |^The "), ""]],
}


class NLPSpacy(NLPEngine):
    name: str = "spacy"

    def __init__(self, cmp_idx, language_short_form: str, **kwargs):
        super().__init__(cmp_idx)
        self.language_short_form = language_short_form
        model_part = "core_web" if self.language_short_form == "en" else "core_news"
        if "spacy_model" in kwargs and kwargs["spacy_model"]:
            self.model_mame = kwargs["spacy_model"]
        else:
            model_size = (
                kwargs["model_size"]
                if "model_size" in kwargs and kwargs["model_size"]
                else "sm"
            )
            self.model_mame = f"{self.language_short_form}_{model_part}_{model_size}"

        self.cleanup_table = cleanup_table.get(self.language_short_form, None)
        self.map_table = entity_mapping_table.get(self.language_short_form, {})
        try:
            self.engine = spacy.load(self.model_mame)
            self.warmup()
        except OSError:
            raise ImportError(
                f"""Please install spacy and the corresponding language model for {self.model_mame}
try:\npython -m spacy download {self.model_mame} """
            )

    def warmup(self):
        self.engine("warmup")

    def __call__(self, text):
        return self.engine(text)

    def get_compare_data(
        self, other_, doc, concept_filter: ConceptFilter, input_provider
    ):
        for entity in doc.ents:
            logger.debug(
                f"SPACY: {entity.start_char} {entity.end_char} {entity.label_} {entity.text}"
            )
            uri = (
                self.map_table[entity.label_]
                if entity.label_ in self.map_table
                else entity.label_
            )

            if concept_filter and not concept_filter(uri):
                continue

            beg_char = entity.start_char
            end_char = entity.end_char
            entity_text = entity.text

            if self.cleanup_table:
                for pattern, replace in self.cleanup_table:
                    entity_text_ = pattern.sub(replace, entity_text)
                    if entity_text_ != entity_text:
                        pos = entity_text.find(entity_text_)
                        if pos >= 0:
                            beg_char += pos
                            end_char = beg_char + len(entity_text_)
                        # entity_text = entity_text_
                        break

            other_.data.append(
                CmpItem(
                    self.cmp_idx,
                    beg_char,
                    end_char,
                    self.name,
                    uri,
                    entity_text,
                    original_uri=entity.label_,
                )
            )
            other_.counter[uri] += 1

    def get_mapping_table(self):
        return entity_mapping_table[self.language_short_form]
