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
    parser.add_argument("-m", "--model", help="input model")
    parser.add_argument(
        "-a",
        "--annotations",
        help="All will display all of them. Otherwise we will lower our self to Spacy",
    )
    parser.add_argument("--show", help="Show the output", action="store_true")

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    initialize_logging_level()
    kwargs = dict(parse_arguments()._get_kwargs())
    show = kwargs.pop("show")
    diff_files = ["wowool.diff"]
    if kwargs["nlp_engine"] == "all":
        from nlp_compare.nlp_engine import all_nlp_engines

        kwargs.pop("nlp_engine")
        for nlp_engine in all_nlp_engines:
            compare(nlp_engine=nlp_engine, **kwargs)

    else:
        compare(**kwargs)
        diff_files.append(f"{kwargs.pop('nlp_engine')}.diff")
    if show:
        print("All done: you can run the following command to see the results")
        diff_tool = environ.get("DIFF_TOOL", "meld")
        print(f"{diff_tool} {' '.join(diff_files)}")
