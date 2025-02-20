from dataclasses import dataclass
from typing import Any
from nlp_compare.mapping_tables import language_map


def get_nlp_engine(cmp_idx, nlp_engine, language, **kwargs):

    if len(language) > 2:
        short_form = language_map.get(language, language)
    else:
        short_form = language

    if nlp_engine == "wowool":
        from nlp_compare.nlp_wowool import NLPWowool

        return NLPWowool(cmp_idx, short_form, **kwargs)

    elif nlp_engine == "spacy":
        from nlp_compare.nlp_spacy import NLPSpacy

        return NLPSpacy(cmp_idx, short_form, **kwargs)
    elif nlp_engine == "stanza":
        from nlp_compare.nlp_stanza import NLPStanza

        return NLPStanza(cmp_idx, short_form, **kwargs)

    elif nlp_engine == "google":
        from nlp_compare.nlp_google import NLPGoogle

        return NLPGoogle(cmp_idx, short_form, **kwargs)

    elif nlp_engine == "google_json":
        from nlp_compare.nlp_google_json import NLPGoogle

        return NLPGoogle(cmp_idx, short_form, **kwargs)

    raise ValueError(f"Unknown nlp engine {nlp_engine}")


all_nlp_engines = ["spacy", "stanza"]
