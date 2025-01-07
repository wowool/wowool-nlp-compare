from pathlib import Path
from wowool.native.core import PipeLine
from wowool.error import Error
from wowool.io.provider import Factory
import subprocess
from collections import Counter
import time
from functools import cmp_to_key
from dataclasses import dataclass, field
from nlp_compare.nlp_engine import get_nlp_engine
from nlp_compare.cmp_objects import CmpItem
from logging import getLogger
from tabulate import tabulate
from nlp_compare.concept_filter import ConceptFilter
import csv

MISSING = "**Missing**"


logger = getLogger("nlp_engine")


@dataclass
class RowData:
    uri: str
    begin_offset: int
    end_offset: int
    text: str | None = None
    literal: str | None = None


@dataclass
class NlpData:
    name: str
    time: float = 0
    counter: Counter = field(default_factory=Counter)
    data: list[CmpItem] = field(default_factory=list)
    tt_time: float = 0
    tt_counter: Counter = field(default_factory=Counter)
    missing: list[CmpItem] = field(default_factory=list)
    rows: list[RowData] = field(default_factory=list)

    def add_row(
        self,
        uri,
        begin_offset,
        end_offset,
        text: str | None = None,
        literal: str | None = None,
    ):
        self.rows.append(RowData(uri, begin_offset, end_offset, text, literal))


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

    def write(self, data):
        self.fh.write(data)

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
        "wowool": FileHandler("wowool.diff"),
        name: FileHandler(f"{name}.diff"),
    }


def print_diff(offset_data: list[CmpItem], nlp_name: str):

    size_offset_data = len(offset_data)
    cmp_info = get_filehandels(nlp_name)
    wow_, other_ = cmp_info["wowool"], cmp_info[nlp_name]

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
            if "wowool" == lhs.source:
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
                    if lhs.source == "wowool":
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
                if lhs.source == "wowool":
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
            if lhs.source == "wowool":
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
    wow_, other_ = cmp_info["wowool"], cmp_info[nlp_name]

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
            if "wowool" == lhs.source:
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
                    if lhs.source == "wowool":
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
                if lhs.source == "wowool":
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
            if lhs.source == "wowool":
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

    # for k, item in cmp_info.items():
    #     item.write(f"{'='*30} {'='*30}\n")


def sort_by_offset(lhs: CmpItem, rhs: CmpItem):
    if lhs.begin_offset == rhs.begin_offset:
        return rhs.end_offset - lhs.end_offset
    return lhs.begin_offset - rhs.begin_offset


class CompareContext:
    def __init__(self):
        self.exclude_missing = None

    def collect_missing_entities(
        self, document_text, sentence_text, wow_: NlpData, other_: NlpData
    ):
        if sentence_text is None:
            return
        for ll, rl in zip(wow_.rows, other_.rows):

            if ll.begin_offset == rl.begin_offset and ll.end_offset == rl.end_offset:
                if (
                    ll.literal
                    and self.exclude_missing
                    and (
                        ll.literal in self.exclude_missing
                        or (rl.text == ll.literal and rl.uri == ll.uri)
                    )
                ):
                    continue
                if ll.uri == MISSING:
                    item = {
                        f"uri_{other_.name}": rl.uri,
                        f"text_{other_.name}": rl.text,
                        f"literal_{other_.name}": rl.literal if rl.literal else "",
                        "sentence": sentence_text,
                    }
                    wow_.missing.append(item)
                elif rl.uri == MISSING:
                    if self.exclude_missing and rl.text in self.exclude_missing:
                        continue
                    item = {
                        "uri_wow": ll.uri,
                        "text_wow": ll.text,
                        "literal_wow": ll.literal if ll.literal else "",
                        "sentence": sentence_text,
                    }
                    other_.missing.append(item)
                else:
                    if ll.uri != rl.uri:
                        item = {
                            f"uri_{other_.name}": f"{ll.uri}({wow_.name})!={rl.uri}",
                            f"text_{other_.name}": rl.text,
                            f"literal_{other_.name}": rl.literal if rl.literal else "",
                            "sentence": sentence_text,
                        }
                        wow_.missing.append(item)

    def print_tabulate(self, wow_: FileHandler, other_: FileHandler):

        tabel_data = []
        for ll, rl in zip(wow_.rows, other_.rows):
            item = {
                "beg": ll.begin_offset,
                "end": ll.end_offset,
                "uri_wow": ll.uri,
                "text_wow": ll.text,
                f"uri_{other_.name}": rl.uri,
                f"text_{other_.name}": rl.text,
            }
            tabel_data.append(item)

        if tabel_data:
            # print(*tabel_data, sep="\n")
            print(tabulate(tabel_data, headers="keys", tablefmt="github"))

    def print_md_table(
        self, document_text, compare_data, offset_data: list[CmpItem], nlp_name: str
    ):

        size_offset_data = len(offset_data)
        # cmp_info = get_filehandels(nlp_name)
        cmp_info = compare_data
        wow_, other_ = compare_data["wowool"], compare_data[nlp_name]

        idx = 0
        previous_sentence = None
        while idx < size_offset_data:

            # ic(offset_data[idx])
            lhs = offset_data[idx]

            if lhs.uri == "Sentence":
                self.print_tabulate(wow_, other_)
                self.collect_missing_entities(
                    document_text, previous_sentence, wow_, other_
                )

                wow_.rows.clear()
                other_.rows.clear()
                previous_sentence = lhs.text
                print(f"\n\n`{lhs.text}`\n")
                idx += 1
                continue

            if lhs.begin_offset == None:
                idx += 1
                continue

            nidx = get_next_valid_idx(offset_data, size_offset_data, idx)
            if nidx >= size_offset_data or nidx == -1:
                cmp_info[lhs.source].add_row(
                    lhs.uri,
                    lhs.begin_offset,
                    lhs.end_offset,
                    lhs.text,
                    literal=lhs.literal,
                )
                # check to write to the other side
                if "wowool" == lhs.source:
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
                            lhs.uri,
                            lhs.begin_offset,
                            lhs.end_offset,
                            lhs.text,
                            literal=lhs.literal,
                        )
                        cmp_info[rhs.source].add_row(
                            rhs.uri,
                            rhs.begin_offset,
                            rhs.end_offset,
                            rhs.text,
                            literal=rhs.literal,
                        )
                        idx = idx + 2
                    else:
                        if lhs.source == "wowool":
                            wow_.add_row(
                                lhs.uri,
                                lhs.begin_offset,
                                lhs.end_offset,
                                lhs.text,
                                literal=lhs.literal,
                            )
                            other_.add_row(MISSING, lhs.begin_offset, lhs.end_offset)
                        else:
                            wow_.add_row(MISSING, lhs.begin_offset, lhs.end_offset)
                            other_.add_row(
                                lhs.uri,
                                lhs.begin_offset,
                                lhs.end_offset,
                                lhs.text,
                                literal=lhs.literal,
                            )
                        idx += 1
                else:
                    # print("=b , != e")
                    if lhs.source == "wowool":
                        wow_.add_row(
                            lhs.uri,
                            lhs.begin_offset,
                            lhs.end_offset,
                            lhs.text,
                            literal=lhs.literal,
                        )
                        other_.add_row(MISSING, lhs.begin_offset, lhs.end_offset)
                    else:
                        wow_.add_row(MISSING, lhs.begin_offset, lhs.end_offset)
                        other_.add_row(
                            lhs.uri,
                            lhs.begin_offset,
                            lhs.end_offset,
                            lhs.text,
                            literal=lhs.literal,
                        )
                    idx += 1
            elif lhs.begin_offset < rhs.begin_offset:
                if lhs.source == "wowool":
                    wow_.add_row(
                        lhs.uri,
                        lhs.begin_offset,
                        lhs.end_offset,
                        lhs.text,
                        literal=lhs.literal,
                    )
                    other_.add_row(MISSING, lhs.begin_offset, lhs.end_offset)
                else:
                    wow_.add_row(MISSING, lhs.begin_offset, lhs.end_offset)
                    other_.add_row(
                        lhs.uri,
                        lhs.begin_offset,
                        lhs.end_offset,
                        lhs.text,
                        literal=lhs.literal,
                    )
                idx += 1
            else:
                assert False, "Can we realy get here ?????"

        self.print_tabulate(wow_, other_)
        self.collect_missing_entities(document_text, previous_sentence, wow_, other_)

    def compare_entities(
        self,
        compare_data,
        input_provider,
        wowool_pipeline,
        nlp,
        concept_filter: ConceptFilter,
        map_table,
    ):

        text = input_provider.text
        if nlp.name not in compare_data:
            compare_data[nlp.name] = NlpData(nlp.name)

        other_: NlpData = compare_data[nlp.name]
        wowool_: NlpData = compare_data["wowool"]

        start = time.time()
        doc = nlp(text)
        end = time.time()
        other_.time += end - start
        nlp.get_compare_data(other_, doc, concept_filter)

        try:
            start = time.time()
            document = wowool_pipeline(input_provider)
            end = time.time()
            wowool_.time += end - start

            for sentence in document.analysis:
                for annotation in sentence:
                    if annotation.is_token:
                        token = annotation
                        if token.has_pos("Num") and concept_filter("CARDINAL"):
                            uri = "CARDINAL"
                            wowool_.data.append(
                                CmpItem(
                                    annotation.begin_offset,
                                    annotation.end_offset,
                                    "wowool",
                                    uri,
                                    token.literal,
                                )
                            )

                    if annotation.is_concept and concept_filter(annotation.uri):
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
                                    annotation.begin_offset,
                                    annotation.end_offset,
                                    "wowool",
                                    uri,
                                    sentence.text,
                                )
                            )

        except Error as ex:
            print(ex)

        print_timing_results(
            "", wowool_.time, other_.name, other_.time, wowool_.counter, other_.counter
        )

        offset_data = other_.data
        offset_data.extend(wowool_.data)
        offset_data = sorted(offset_data, key=cmp_to_key(sort_by_offset))

        # print_rst_table(offset_data, nlp.name)
        self.print_md_table(text, compare_data, offset_data, nlp.name)
        print_diff(offset_data, nlp.name)

        with open(f"wowool-vs-{nlp.name}-diff.txt", "a") as wfh:
            subprocess.run(
                ["diff", "-y", "wowool.diff", f"{nlp.name}.diff"], stdout=wfh
            )


def get_nlp_engines(nlp_engine: str, language, pipeline: str, **kwargs):
    """warming up the engines"""

    start = time.time()
    wowool_pipeline = PipeLine(f"{pipeline}")
    wowool_pipeline("test")
    end = time.time()
    startup_time = end - start
    logger.info(f"wowool startup time: {startup_time:.3f}")

    start = time.time()
    nlp = get_nlp_engine(nlp_engine, language, **kwargs)
    nlp("test")
    end = time.time()
    startup_time = end - start
    logger.info(f"{nlp_engine} startup time: {startup_time:.3f}")

    return wowool_pipeline, nlp


def get_wowool_annotation_filter(annotations, map_table):
    filter_table = set()
    if annotations:
        annotations_ = annotations.split(",")
    else:
        annotations_ = map_table.keys()

    for annotation in annotations_:
        if annotation in map_table:
            filter_table.add(map_table[annotation])
        filter_table.add(annotation)

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


def clear_intermediate_results(compare_data):
    for engine, data in compare_data.items():
        data.data.clear()
        data.counter.clear()
        data.time = 0


def print_timing_results(
    prefix, wowool_time, other_name, other_time, wowool_counter, other_counter
):
    print(f"""\n{prefix} Time: {other_name: <8}: {other_time:.3f} {other_counter}""")
    print(f"""{prefix} Time: {'Wowool':<8}: {wowool_time:.3f} {wowool_counter}""")
    word = "faster than" if wowool_time < other_time else "slower than"
    faster = round(abs((other_time / wowool_time) - 1), 1)

    if faster == 0:
        print(f""" Wowool is is as fast as {other_name}""")
    else:
        print(f""" Wowool is {faster:.3f} {word} {other_name}""")


def write_missing_entities(wowool_, other_):
    with open("missing_in_wowool.csv", "w") as csvfile:
        if wowool_.missing:
            writer = csv.DictWriter(csvfile, fieldnames=wowool_.missing[0].keys())
            writer.writeheader()
            writer.writerows(wowool_.missing)

    with open(f"missing_in_{other_.name}.csv", "w") as csvfile:
        if other_.missing:
            writer = csv.DictWriter(csvfile, fieldnames=other_.missing[0].keys())
            writer.writeheader()
            writer.writerows(other_.missing)


def compare(
    nlp_engine: str, language: str, pipeline: str, annotations: str, file: str, **kwargs
):

    cc = CompareContext()
    cleanup_result_files(nlp_engine)
    exculde_fn = Path(f"config/{language}_exculde.txt")
    if exculde_fn.exists():
        with exculde_fn.open() as fh:
            cc.exclude_missing = set()
            for line in fh:
                line = line.strip()
                if line:
                    cc.exclude_missing.add(line)

    wowool_pipeline, nlp = get_nlp_engines(nlp_engine, language, pipeline, **kwargs)
    map_table = nlp.get_mapping_table()
    concept_filter = get_wowool_annotation_filter(annotations, map_table)
    files = []
    for fn in file:
        files.extend([fn for fn in Factory.glob(Path(fn))])
    if files:
        compare_data = {"wowool": NlpData("wowool")}
        for ip in files:
            logger.info(f"Process: {ip.id}")
            clear_intermediate_results(compare_data)
            cc.compare_entities(
                compare_data, ip, wowool_pipeline, nlp, concept_filter, map_table
            )
            for engine, data in compare_data.items():
                data.tt_time += data.time
                data.tt_counter.update(data.counter)

        other_ = compare_data[nlp.name]
        wowool_ = compare_data["wowool"]
        print_timing_results(
            "Total: ",
            wowool_.tt_time,
            other_.name,
            other_.tt_time,
            wowool_.tt_counter,
            other_.tt_counter,
        )

        write_missing_entities(wowool_, other_)

    else:
        raise ValueError(f"File {file} not found")
