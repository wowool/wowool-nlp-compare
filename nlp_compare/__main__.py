from nlp_compare.nlp_entities import compare
from nlp_compare.log import initialize_logging_level
import argparse
from pathlib import Path


def parse_arguments():
    """
    Parses the command line arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="input file", required=True)
    parser.add_argument("-e", "--nlp_engine", help="npl_engine (spacy)", required=True)
    parser.add_argument("-l", "--language", help="input language", required=True)
    parser.add_argument("-p", "--pipeline", help="input pipeline", required=True)
    parser.add_argument(
        "-a",
        "--annotations",
        help="All will display all of them. Otherwise we will lower our self to Spacy",
    )

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    initialize_logging_level()
    kwargs = dict(parse_arguments()._get_kwargs())
    compare(**kwargs)
