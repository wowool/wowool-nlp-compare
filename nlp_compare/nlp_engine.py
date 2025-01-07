from dataclasses import dataclass
from typing import Any
from nlp_compare.mapping_tables import language_map


@dataclass
class NLPEngine:
    name: str
    engine: Any

    def __call__(self, text):
        return self.engine(text)


def get_nlp_engine(nlp_engine, language, **kwargs):

    if len(language) > 2:
        short_form = language_map[language]
    else:
        short_form = language

    if nlp_engine == "spacy":
        from nlp_compare.nlp_spacy import NLPSpacy

        return NLPSpacy(short_form, **kwargs)
    elif nlp_engine == "stanza":
        from nlp_compare.nlp_stanza import NLPStanza

        return NLPStanza(short_form, **kwargs)

    elif nlp_engine == "google":
        from nlp_compare.nlp_google import NLPGoogle

        return NLPGoogle(short_form, **kwargs)

    raise ValueError(f"Unknown nlp engine {nlp_engine}")


all_nlp_engines = ["spacy", "stanza"]
