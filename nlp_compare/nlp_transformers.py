from typing import Any
from nlp_compare.cmp_objects import CmpItem
from nlp_compare.concept_filter import ConceptFilter
import re
from nlp_compare.cmp_objects import NLPEngine
from logging import getLogger
from dataclasses import dataclass, field
from nlp_compare.profile import nlp_profile
from memory_profiler import profile
from transformers import AutoTokenizer, AutoModelForTokenClassification
import torch
from nlp_compare.nlp_wowool import entity_mapping_table

logger = getLogger("nlp.cmp.transformers")

# entity_mapping_table = {}


cleanup_table = {
    "en": [[re.compile(r"'s$|^the |^The "), ""]],
}


@dataclass
class Entity:
    label: str
    start: int
    end: int
    text: str


@dataclass
class Document:
    entities: list[Entity] = field(default_factory=list[Entity])


class Engine:

    def __init__(self, model_name: str):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForTokenClassification.from_pretrained(model_name)

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


class NLPTransformers(NLPEngine):
    name: str = "transformers"

    def __init__(self, cmp_idx, language_short_form: str, **kwargs):
        super().__init__(cmp_idx)
        self.language_short_form = language_short_form
        print(f"Transformers model: {kwargs}")
        self.model_mame = kwargs["transformers_model"]
        if not self.model_mame:
            raise ValueError(
                "transformers_model must be provided in arguments using --transformers_model"
            )
        self.map_table = entity_mapping_table.get(self.language_short_form, {})
        try:
            self.engine = Engine(self.model_mame)
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
        for entity in doc.entities:
            logger.debug(f"TRANS: {entity}")
            uri = (
                self.map_table[entity.label]
                if entity.label in self.map_table
                else entity.label
            )

            if concept_filter and not concept_filter(uri):
                continue

            beg_char = entity.start
            end_char = entity.end
            entity_text = entity.text

            # if self.cleanup_table:
            #     for pattern, replace in self.cleanup_table:
            #         entity_text_ = pattern.sub(replace, entity_text)
            #         if entity_text_ != entity_text:
            #             pos = entity_text.find(entity_text_)
            #             if pos >= 0:
            #                 beg_char += pos
            #                 end_char = beg_char + len(entity_text_)
            #             # entity_text = entity_text_
            #             break

            other_.data.append(
                CmpItem(
                    self.cmp_idx,
                    beg_char,
                    end_char,
                    self.name,
                    uri,
                    entity_text,
                    original_uri=entity.label,
                )
            )
            other_.counter[uri] += 1

    def get_mapping_table(self):
        return entity_mapping_table[self.language_short_form]
