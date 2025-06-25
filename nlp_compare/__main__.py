from nlp_compare.nlp_entities import compare
from nlp_compare.log import initialize_logging_level
import argparse
from os import environ


def parse_arguments():
    """
    Parses the command line arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="input file", nargs="+", required=True)
    parser.add_argument("-e", "--nlp_engine", help="npl_engine (spacy)", required=True)
    parser.add_argument("-l", "--language", help="input language", required=True)
    parser.add_argument("-p", "--pipeline", help="input pipeline", required=True)
    parser.add_argument("--json_results", help="result input file.(only google_json)")
    parser.add_argument("-tm", "--transformers_model", help="input model")
    parser.add_argument("-sm", "--spacy_model", help="input model")
    parser.add_argument(
        "-g",
        "--golden_corpus_filename",
        help="filename corpus filename",
    )

    parser.add_argument(
        "-a",
        "--annotations",
        help="All will display all of them. Otherwise we will lower our self to Spacy",
    )
    parser.add_argument("--no-show", help="Show the output", action="store_false")
    parser.add_argument(
        "-r",
        "--precision_recall",
        help="calculate precision recall",
        action="store_true",
    )

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    initialize_logging_level()
    kwargs = dict(parse_arguments()._get_kwargs())
    print(kwargs)
    show = kwargs.pop("no_show")
    if kwargs["nlp_engine"] == "all":
        from nlp_compare.nlp_engine import all_nlp_engines

        kwargs.pop("nlp_engine")
        for nlp_engine in all_nlp_engines:
            compare(nlp_engine=nlp_engine, **kwargs, show=show)

    else:
        compare(**kwargs, show=show)
