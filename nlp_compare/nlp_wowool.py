from nlp_compare.cmp_objects import CmpItem
from nlp_compare.concept_filter import ConceptFilter
from wowool.native.core import PipeLine
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
        "Date": "DATE",
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
        "Date": "DATE",
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
        "Date": "DATE",
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
        "Facility": "FAC",
        "WorldRegion": "LOC",
        "PlaceAdj": "NORP",
        "MoneyAmount": "MONEY",
        "Event": "EVENT",
        "TimePhrase": "TIME",
        "Place": "GPE",
        "Date": "DATE",
    },
}


class NLPWowool(NLPEngine):
    name: str = "wowool"

    def __init__(self, cmp_idx, language_short_form, **kwargs):
        super(NLPWowool, self).__init__(cmp_idx)
        self.language_short_form = language_short_form
        if "pipeline" in kwargs:
            self.engine = PipeLine(kwargs["pipeline"])
        # self.engine = stanza.Pipeline(self.language_short_form)
        self.map_table = entity_mapping_table.get(self.language_short_form, {})

    def warmup(self):
        self.engine("warmup")

    def __call__(self, text):
        return self.engine(text)

    def get_compare_data(self, wowool_, doc, concept_filter: ConceptFilter):
        for sentence in doc.analysis:
            for annotation in sentence:
                if annotation.is_token:
                    token = annotation
                    if token.has_pos("Num") and concept_filter("CARDINAL"):
                        uri = "CARDINAL"
                        wowool_.data.append(
                            CmpItem(
                                self.cmp_idx,
                                annotation.begin_offset,
                                annotation.end_offset,
                                "wowool",
                                uri,
                                token.literal,
                            )
                        )

                elif annotation.is_concept:
                    concept = annotation
                    uri = (
                        self.map_table[concept.uri]
                        if concept.uri in self.map_table
                        else concept.uri
                    )

                    if not concept_filter(uri):
                        continue

                    if uri != "Sentence":
                        wowool_.data.append(
                            CmpItem(
                                self.cmp_idx,
                                annotation.begin_offset,
                                annotation.end_offset,
                                "wowool",
                                uri,
                                concept.canonical,
                                literal=concept.literal,
                            )
                        )
                        wowool_.counter[uri] += 1
                    else:
                        wowool_.data.append(
                            CmpItem(
                                self.cmp_idx,
                                annotation.begin_offset,
                                annotation.end_offset,
                                "wowool",
                                uri,
                                sentence.text,
                            )
                        )

    def get_mapping_table(self):
        return entity_mapping_table[self.language_short_form]
