import argparse
from pathlib import Path
from wowool.native.core import PipeLine
from wowool.error import Error
from wowool.io.provider import Factory
import subprocess
from collections import Counter
import time
from functools import cmp_to_key
from dataclasses import dataclass, field
from nlp_compare.mapping_tables import entity_mapping_table
from nlp_compare.nlp_engine import get_nlp_engine
from nlp_compare.cmp_objects import CmpItem
from logging import getLogger
from nlp_compare.log import initialize_logging_level
from tabulate import tabulate

MISSING = "**Missing**"


logger = getLogger("nlp_engine")


@dataclass
class NlpData:
    name: str
    time: float = 0
    counter: Counter = field(default_factory=Counter)
    data: list[CmpItem] = field(default_factory=list)


compare_data = {"wowool": NlpData("wowool")}


class ConceptFilter:
    def __init__(self, filter_table):
        self.filter_table = filter_table
        self.cmp_all = "all" in filter_table

    def __call__(self, c):
        if self.cmp_all:
            if c.uri == "Sentence":
                return False
            return True
        return c.uri in self.filter_table


# sentence = "I didn't worked on Thursday morning . Arthur didn't feel very good"
# sentence1 = """I worked on Thursday morning . Arthur didn't feel very good"""
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')


def get_next_valid_idx(offset_data, offset_data_len, idx):
    nidx = idx + 1
    while nidx < offset_data_len:
        if offset_data[nidx]:
            return nidx
        nidx = idx + 1

    return -1


class FileHandler:
    def __init__(self, name):
        self.fn = Path(name)
        self.name = self.fn.stem
        self.fh = open(self.fn, "w")
        self.lines_ = None
        self.rows = []

    def write(self, data):
        self.fh.write(data)

    def add_row(self, uri, begin_offset, end_offset, text: str | None = None):
        self.rows.append([uri, begin_offset, end_offset, text])

    def close(self):
        self.fh.close()

    @property
    def lines(self):
        if self.lines_ is None:
            with open(self.fn) as fh:
                self.lines_ = fh.readlines()
        return self.lines_


def get_filehandels(name: str):
    return {
        "wow": FileHandler("wowool.diff"),
        name: FileHandler(f"{name}.diff"),
    }


def print_diff(offset_data: list[CmpItem], nlp_name: str):

    size_offset_data = len(offset_data)
    cmp_info = get_filehandels(nlp_name)
    wow_, other_ = cmp_info["wow"], cmp_info[nlp_name]

    idx = 0
    for k, item in cmp_info.items():
        item.write(f"{'-' *30} {k} {'-' *30}\n")

    while idx < size_offset_data:

        # ic(offset_data[idx])
        # print("idx", idx, offset_data[idx])
        if offset_data[idx].uri == "Sentence":
            wow_.write(f"\n{offset_data[idx].text}\n")
            other_.write(f"\n{offset_data[idx].text}\n")
            idx += 1
            continue

        lhs = offset_data[idx]
        if lhs.begin_offset == None:
            idx += 1
            continue

        nidx = get_next_valid_idx(offset_data, size_offset_data, idx)
        if nidx >= size_offset_data or nidx == -1:
            cmp_info[lhs.source].write(
                f"({lhs.begin_offset:<3},{lhs.end_offset:<3}) {lhs.uri:<30}:{lhs.text}\n"
            )
            # check to write to the other side
            if "wow" == lhs.source:
                other_.write(
                    f"({lhs.begin_offset:<3},{lhs.end_offset:<3}) {MISSING:<30}\n"
                )
            else:
                wow_.write(
                    f"({lhs.begin_offset:<3},{lhs.end_offset:<3}) {MISSING:<30}\n"
                )
            break

        rhs = offset_data[nidx]

        # check begin offsets.
        # if args.verbose:
        #     ic(lhs, rhs)
        if lhs.begin_offset == rhs.begin_offset:
            if lhs.end_offset == rhs.end_offset:
                if lhs.source != rhs.source:
                    cmp_info[lhs.source].write(
                        f"({lhs.begin_offset:<3},{lhs.end_offset:<3}) {lhs.uri:<30}:{lhs.text}\n"
                    )
                    cmp_info[rhs.source].write(
                        f"({rhs.begin_offset:<3},{rhs.end_offset:<3}) {rhs.uri:<30}:{rhs.text}\n"
                    )
                    idx = idx + 2
                else:
                    if lhs.source == "wow":
                        wow_.write(
                            f"({lhs.begin_offset:<3},{lhs.end_offset:<3}) {lhs.uri:<30}:{lhs.text}\n"
                        )
                        other_.write(
                            f"({lhs.begin_offset:<3},{lhs.end_offset:<3}) {MISSING:<30}\n"
                        )
                    else:
                        wow_.write(
                            f"({lhs.begin_offset:<3},{lhs.end_offset:<3}) {MISSING:<30}\n"
                        )
                        other_.write(
                            f"({lhs.begin_offset:<3},{lhs.end_offset:<3}) {lhs.uri:<30}:{lhs.text}\n"
                        )
                    idx += 1
            else:
                # print("=b , != e")
                if lhs.source == "wow":
                    wow_.write(
                        f"({lhs.begin_offset:<3},{lhs.end_offset:<3}) {lhs.uri:<30}:{lhs.text}\n"
                    )
                    other_.write(
                        f"({lhs.begin_offset:<3},{lhs.end_offset:<3}) {MISSING:<30}\n"
                    )
                else:
                    wow_.write(
                        f"({lhs.begin_offset:<3},{lhs.end_offset:<3}) {MISSING:<30}\n"
                    )
                    other_.write(
                        f"({lhs.begin_offset:<3},{lhs.end_offset:<3}) {lhs.uri:<30}:{lhs.text}\n"
                    )
                idx += 1
        elif lhs.begin_offset < rhs.begin_offset:
            if lhs.source == "wow":
                wow_.write(
                    f"({lhs.begin_offset:<3},{lhs.end_offset:<3}) {lhs.uri:<30}:{lhs.text}\n"
                )
                other_.write(
                    f"({lhs.begin_offset:<3},{lhs.end_offset:<3}) {MISSING:<30}\n"
                )
            else:
                wow_.write(
                    f"({lhs.begin_offset:<3},{lhs.end_offset:<3}) {MISSING:<30}\n"
                )
                other_.write(
                    f"({lhs.begin_offset:<3},{lhs.end_offset:<3}) {lhs.uri:<30}:{lhs.text}\n"
                )
            idx += 1
        else:
            assert False, "Can we realy get here ?????"

    for k, item in cmp_info.items():
        item.close()


def print_rst_table(offset_data: list[CmpItem], nlp_name: str):

    size_offset_data = len(offset_data)
    cmp_info = get_filehandels(nlp_name)
    wow_, other_ = cmp_info["wow"], cmp_info[nlp_name]

    idx = 0
    literal = "literal"

    for k, item in cmp_info.items():
        item.write(f"{'='*30} {'='*30}\n")
        item.write(f"{k:^30} {literal:^30}\n")
        item.write(f"{'='*30} {'='*30}\n")

    while idx < size_offset_data:

        # ic(offset_data[idx])
        lhs = offset_data[idx]

        if lhs.uri == "Sentence":
            wow_.write(f"\n{lhs.text}\n")
            other_.write("\n\n")
            idx += 1
            continue

        if lhs.begin_offset == None:
            idx += 1
            continue

        nidx = get_next_valid_idx(offset_data, size_offset_data, idx)
        if nidx >= size_offset_data or nidx == -1:
            cmp_info[lhs.source].write(
                f"{lhs.uri:<30} ({lhs.begin_offset:<3},{lhs.end_offset:<3}) :{lhs.text}\n"
            )
            # check to write to the other side
            if "wow" == lhs.source:
                other_.write(
                    f"{MISSING:<30} ({lhs.begin_offset:<3},{lhs.end_offset:<3})\n"
                )
            else:
                wow_.write(
                    f"{MISSING:<30} ({lhs.begin_offset:<3},{lhs.end_offset:<3})\n"
                )
            break

        rhs = offset_data[nidx]

        # check begin offsets.
        # if args.verbose:
        #     ic(lhs, rhs)
        if lhs.begin_offset == rhs.begin_offset:
            if lhs.end_offset == rhs.end_offset:
                if lhs.source != rhs.source:
                    cmp_info[lhs.source].write(
                        f"{lhs.uri:<30} ({lhs.begin_offset:<3},{lhs.end_offset:<3}) :{lhs.text}\n"
                    )
                    cmp_info[rhs.source].write(
                        f"{rhs.uri:<30} ({rhs.begin_offset:<3},{rhs.end_offset:<3}) :{rhs.text}\n"
                    )
                    idx = idx + 2
                else:
                    if lhs.source == "wow":
                        wow_.write(
                            f"{lhs.uri:<30} ({lhs.begin_offset:<3},{lhs.end_offset:<3}) :{lhs.text}\n"
                        )
                        other_.write(
                            f"{MISSING:<30} ({lhs.begin_offset:<3},{lhs.end_offset:<3})\n"
                        )
                    else:
                        wow_.write(
                            f"{MISSING:<30} ({lhs.begin_offset:<3},{lhs.end_offset:<3})\n"
                        )
                        other_.write(
                            f"{lhs.uri:<30} ({lhs.begin_offset:<3},{lhs.end_offset:<3}) :{lhs.text}\n"
                        )
                    idx += 1
            else:
                # print("=b , != e")
                if lhs.source == "wow":
                    wow_.write(
                        f"{lhs.uri:<30}:{lhs.text} ({lhs.begin_offset:<3},{lhs.end_offset:<3}) \n"
                    )
                    other_.write(
                        f"{MISSING:<30} ({lhs.begin_offset:<3},{lhs.end_offset:<3})\n"
                    )
                else:
                    wow_.write(
                        f"{MISSING:<30} ({lhs.begin_offset:<3},{lhs.end_offset:<3}) \n"
                    )
                    other_.write(
                        f"{lhs.uri:<30} ({lhs.begin_offset:<3},{lhs.end_offset:<3}) :{lhs.text}\n"
                    )
                idx += 1
        elif lhs.begin_offset < rhs.begin_offset:
            if lhs.source == "wow":
                wow_.write(
                    f"{lhs.uri:<30} ({lhs.begin_offset:<3},{lhs.end_offset:<3}) :{lhs.text}\n"
                )
                other_.write(
                    f"{MISSING:<30} ({lhs.begin_offset:<3},{lhs.end_offset:<3})\n"
                )
            else:
                wow_.write(
                    f"{MISSING:<30} ({lhs.begin_offset:<3},{lhs.end_offset:<3})\n"
                )
                other_.write(
                    f"{lhs.uri:<30} ({lhs.begin_offset:<3},{lhs.end_offset:<3}) :{lhs.text}\n"
                )
            idx += 1
        else:
            assert False, "Can we realy get here ?????"

    for k, item in cmp_info.items():
        item.write(f"{'='*30} {'='*30}\n")

    for k, item in cmp_info.items():
        item.close()

    with open(f"wowool-vs-{nlp_name}-tbl.txt", "a") as wfh:
        for ll, rl in zip(wow_.lines, other_.lines):
            ll = ll[:-1]
            wfh.write(ll)
            line_length = len(ll)
            while line_length < 62:
                wfh.write(" ")
                line_length += 1
            wfh.write(rl)


def print_tabulate(wow_, other_):

    tabel_data = []
    for ll, rl in zip(wow_.rows, other_.rows):
        item = {
            "beg": ll[1],
            "end": ll[2],
            "uri_wow": ll[0],
            "text_wow": ll[3],
            f"uri_{other_.name}": rl[0],
            f"text_{other_.name}": rl[3],
        }
        tabel_data.append(item)

    if tabel_data:
        # print(*tabel_data, sep="\n")
        print(tabulate(tabel_data, headers="keys", tablefmt="github"))


def print_md_table(offset_data: list[CmpItem], nlp_name: str):

    size_offset_data = len(offset_data)
    cmp_info = get_filehandels(nlp_name)
    wow_, other_ = cmp_info["wow"], cmp_info[nlp_name]

    idx = 0

    while idx < size_offset_data:

        # ic(offset_data[idx])
        lhs = offset_data[idx]

        if lhs.uri == "Sentence":
            print_tabulate(wow_, other_)
            wow_.rows.clear()
            other_.rows.clear()
            print(f"\n\n`{lhs.text}`\n")
            idx += 1
            continue

        if lhs.begin_offset == None:
            idx += 1
            continue

        nidx = get_next_valid_idx(offset_data, size_offset_data, idx)
        if nidx >= size_offset_data or nidx == -1:
            cmp_info[lhs.source].add_row(
                lhs.uri, lhs.begin_offset, lhs.end_offset, lhs.text
            )
            # check to write to the other side
            if "wow" == lhs.source:
                other_.add_row(MISSING, lhs.begin_offset, lhs.end_offset)
            else:
                wow_.add_row(MISSING, lhs.begin_offset, lhs.end_offset)
            break

        rhs = offset_data[nidx]

        # check begin offsets.
        # if args.verbose:
        #     ic(lhs, rhs)
        if lhs.begin_offset == rhs.begin_offset:
            if lhs.end_offset == rhs.end_offset:
                if lhs.source != rhs.source:
                    cmp_info[lhs.source].add_row(
                        lhs.uri, lhs.begin_offset, lhs.end_offset, lhs.text
                    )
                    cmp_info[rhs.source].add_row(
                        rhs.uri, rhs.begin_offset, rhs.end_offset, rhs.text
                    )
                    idx = idx + 2
                else:
                    if lhs.source == "wow":
                        wow_.add_row(
                            lhs.uri, lhs.begin_offset, lhs.end_offset, lhs.text
                        )
                        other_.add_row(MISSING, lhs.begin_offset, lhs.end_offset)
                    else:
                        wow_.add_row(MISSING, lhs.begin_offset, lhs.end_offset)
                        other_.add_row(
                            lhs.uri, lhs.begin_offset, lhs.end_offset, lhs.text
                        )
                    idx += 1
            else:
                # print("=b , != e")
                if lhs.source == "wow":
                    wow_.add_row(lhs.uri, lhs.begin_offset, lhs.end_offset, lhs.text)
                    other_.add_row(MISSING, lhs.begin_offset, lhs.end_offset)
                else:
                    wow_.add_row(MISSING, lhs.begin_offset, lhs.end_offset)
                    other_.add_row(lhs.uri, lhs.begin_offset, lhs.end_offset, lhs.text)
                idx += 1
        elif lhs.begin_offset < rhs.begin_offset:
            if lhs.source == "wow":
                wow_.add_row(lhs.uri, lhs.begin_offset, lhs.end_offset, lhs.text)
                other_.add_row(MISSING, lhs.begin_offset, lhs.end_offset)
            else:
                wow_.add_row(MISSING, lhs.begin_offset, lhs.end_offset)
                other_.add_row(lhs.uri, lhs.begin_offset, lhs.end_offset, lhs.text)
            idx += 1
        else:
            assert False, "Can we realy get here ?????"

    print_tabulate(wow_, other_)
    # for k, item in cmp_info.items():
    #     item.write(f"{'='*30} {'='*30}\n")


def sort_by_offset(lhs: CmpItem, rhs: CmpItem):
    if lhs.begin_offset == rhs.begin_offset:
        return rhs.end_offset - lhs.end_offset
    return lhs.begin_offset - rhs.begin_offset


def process(id, wowool_pipeline, nlp, concept_filter, map_table):
    text = id.text
    if nlp.name not in compare_data:
        compare_data[nlp.name] = NlpData(nlp.name)

    other_: NlpData = compare_data[nlp.name]
    wowool_: NlpData = compare_data["wowool"]

    start = time.time()
    doc = nlp(text)
    end = time.time()
    other_.time += end - start

    nlp.get_compare_data(other_, doc)

    try:
        start = time.time()
        document = wowool_pipeline(id)
        end = time.time()
        wowool_.time += end - start

        for sentence in document.analysis:
            for annotation in sentence:
                if annotation.is_token:
                    token = annotation
                    if token.has_pos("Num"):
                        uri = "CARDINAL"
                        wowool_.data.append(
                            CmpItem(
                                annotation.begin_offset,
                                annotation.end_offset,
                                "wow",
                                uri,
                                token.literal,
                            )
                        )

                if annotation.is_concept and concept_filter(annotation):
                    concept = annotation
                    uri = (
                        map_table[concept.uri]
                        if concept.uri in map_table
                        else concept.uri
                    )

                    if uri != "Sentence":
                        wowool_.data.append(
                            CmpItem(
                                annotation.begin_offset,
                                annotation.end_offset,
                                "wow",
                                uri,
                                concept.canonical,
                            )
                        )
                        wowool_.counter[uri] += 1
                    else:
                        wowool_.data.append(
                            CmpItem(
                                annotation.begin_offset,
                                annotation.end_offset,
                                "wow",
                                uri,
                                sentence.text,
                            )
                        )

    except Error as ex:
        print(ex)

    offset_data = other_.data
    offset_data.extend(wowool_.data)

    offset_data = sorted(offset_data, key=cmp_to_key(sort_by_offset))
    # for item in offset_data:
    #     print(item)
    print(f"""Processing time of {other_.name}: {other_.time:.3f} {other_.counter}""")
    print(f"""Processing time of wowool: {wowool_.time:.3f} {wowool_.counter}""")
    word = "faster" if wowool_.time < other_.time else "slower"
    print(f"""wowool is {other_.time/wowool_.time:.3f} {word} than {other_.name}""")

    print_diff(offset_data, nlp.name)
    print_rst_table(offset_data, nlp.name)
    print_md_table(offset_data, nlp.name)

    with open(f"wowool-vs-{nlp.name}-diff.txt", "a") as wfh:
        subprocess.run(["diff", "-y", "wowool.diff", f"{nlp.name}.diff"], stdout=wfh)


def get_nlp_engines(nlp_engine: str, language, pipeline: str):
    """warming up the engines"""

    start = time.time()
    wowool_pipeline = PipeLine(f"{pipeline}")
    wowool_pipeline("test")
    end = time.time()
    startup_time = end - start
    logger.info(f"wowool startup time: {startup_time:.3f}")

    start = time.time()
    nlp = get_nlp_engine(nlp_engine, language)
    nlp("test")
    end = time.time()
    startup_time = end - start
    logger.info(f"{nlp_engine} startup time: {startup_time:.3f}")

    return wowool_pipeline, nlp


def get_mapping_table(language: str):
    return entity_mapping_table[language]


def get_wowool_annotation_filter(annotations, map_table):
    if annotations:
        filter_table = set(annotations.split(","))
    else:
        filter_table = set(map_table.keys())
    return ConceptFilter(filter_table)


def cleanup_result_files(nlp_engine: str):
    cleanup = [
        "wowool.diff",
        f"{nlp_engine}.diff",
        f"wowool-vs-{nlp_engine}-diff.txt",
        f"wowool-vs-{nlp_engine}-tbl.txt",
    ]
    for fn in cleanup:
        Path(fn).unlink(missing_ok=True)
    Path(f"wowool-vs-{nlp_engine}-tbl.txt").write_text("")


def compare(nlp_engine: str, language: str, pipeline: str, annotations: str, file: str):

    cleanup_result_files(nlp_engine)

    wowool_pipeline, nlp = get_nlp_engines(nlp_engine, language, pipeline)
    map_table = get_mapping_table(language)
    concept_filter = get_wowool_annotation_filter(annotations, map_table)

    files = [fn for fn in Factory.glob(Path(file))]
    if files:
        for ip in files:
            logger.info(f"process: {ip.id}")
            process(ip, wowool_pipeline, nlp, concept_filter, map_table)
    else:
        raise ValueError(f"File {file} not found")
